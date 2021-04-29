import datetime
import json
import os

import stripe

from django.http import JsonResponse
from rest_framework import generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.pagination import StandardPagination
from api.permissions import SafeMethods
from api.serializers import VountySerializer
from api.models import Vounty, Fund, Tag


class VountyList(generics.ListCreateAPIView):
    permission_classes = [SafeMethods]
    queryset = Vounty.objects.all()
    serializer_class = VountySerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filter_fields = ['user__id', 'featured', 'tags__id']
    search_fields = ['title', 'subtitle']
    ordering_fields = ['fund_count', 'date', 'prize']
    ordering = 'date'

    def perform_create(self, serializer):
        date = datetime.datetime.utcnow()
        serializer.save(date=date)


class VountyDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [SafeMethods]
    queryset = Vounty.objects.all()
    serializer_class = VountySerializer

    def perform_update(self, serializer):
        if 'image' in serializer.validated_data:
            serializer.instance.image.delete()
        serializer.save()

    def perform_destroy(self, instance):
        instance.image.delete()
        instance.delete()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_vounty(request):
    token = request.data.get('token')
    amount = request.data.get('amount')

    stripe.api_key = os.environ.get('STRIPE_KEY')
    charge = stripe.Charge.create(amount=amount * 100,
                                  currency='eur',
                                  source=token['id'])

    title = request.data.get('title')
    subtitle = request.data.get('subtitle')
    image = request.data.get('image')
    date = datetime.datetime.utcnow()

    vounty = Vounty(user=request.user, title=title, subtitle=subtitle,
                    image=image, fund_count=1, date=date, prize=amount)
    vounty.save()

    tags = request.data.get('tags')
    for tag_id in [tag['id'] for tag in tags]:
        tag = Tag.objects.get(id=tag_id)
        vounty.tags.add(tag)

    fund = Fund(user=request.user, vounty=vounty, date=date,
                amount=amount, charge=json.dumps(charge))
    fund.save()

    serializer = VountySerializer(vounty)
    return JsonResponse(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fund_vounty(request):
    token = request.data.get('token')
    vounty_id = request.data.get('id')
    amount = request.data.get('amount')

    stripe.api_key = os.environ.get('STRIPE_KEY')
    charge = stripe.Charge.create(amount=amount * 100,
                                  currency='eur',
                                  source=token['id'])

    vounty = Vounty.objects.get(id=vounty_id)
    vounty.fund_count += 1
    vounty.prize += amount
    vounty.save()

    date = datetime.datetime.utcnow()
    fund = Fund(user=request.user, vounty=vounty, date=date,
                amount=amount, charge=json.dumps(charge))
    fund.save()

    serializer = VountySerializer(vounty)
    return JsonResponse(serializer.data)
