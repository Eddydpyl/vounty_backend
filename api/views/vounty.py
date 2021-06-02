import datetime
import json
import os

import praw
import stripe
from django.core.mail import mail_admins

from django.http import JsonResponse
from rest_framework import generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.pagination import StandardPagination
from api.permissions import SafeMethods
from api.serializers import VountySerializer
from api.models import Vounty, Fund, Tag, Subscription
from api.utils import handle_image, sanitize, send_email
from vounty_backend.settings import DEBUG


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
    ordering_fields = ['comment_count', 'entry_count',
                       'fund_count', 'date', 'prize']
    ordering = 'date'

    def perform_create(self, serializer):
        date = datetime.datetime.utcnow()
        if 'description' in serializer.validated_data:
            description = sanitize(serializer.validated_data['description'])
            serializer.save(description=description, date=date)
        else: serializer.save(date=date)


class VountyDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [SafeMethods]
    queryset = Vounty.objects.all()
    serializer_class = VountySerializer

    def perform_update(self, serializer):
        if 'image' in serializer.validated_data:
            serializer.instance.image.delete()
        if 'description' in serializer.validated_data:
            description = sanitize(serializer.validated_data['description'])
            serializer.save(description=description)
        else: serializer.save()

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
    description = sanitize(request.data.get('description'))
    image = handle_image(request.data.get('image'))
    date = datetime.datetime.utcnow()

    vounty = Vounty(user=request.user, title=title, subtitle=subtitle,
                    description=description, image=image, fund_count=1,
                    date=date, prize=amount)
    vounty.save()

    tags = request.data.get('tags')
    for tag_id in [tag['id'] for tag in tags]:
        tag = Tag.objects.get(id=tag_id)
        vounty.tags.add(tag)

    Fund(user=request.user, vounty=vounty, date=date,
         amount=amount, charge=json.dumps(charge)).save()

    Subscription(user=request.user, vounty=vounty, new_comment=True,
                 new_entry=True, new_fund=True).save()

    if not DEBUG and 'REDDIT_CLIENT_ID' in os.environ:
        url = 'https://vounty.io/vounty?id=' + str(vounty.id)
        reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                             client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                             user_agent=os.environ.get('REDDIT_USERAGENT'),
                             username=os.environ.get('REDDIT_USERNAME'),
                             password=os.environ.get('REDDIT_PASSWORD'))
        response = reddit.subreddit('Vounty').submit(vounty.title, url=url)
        vounty.reddit = 'https://www.reddit.com' + response.permalink
        vounty.save()

    # While there are few users in the platform, keep tabs on everything.
    message = 'A new vounty has been created!\n\nCheck it out: https://vounty.io/vounty?id=' + str(vounty.id)
    mail_admins('New Activity in Vounty', message, fail_silently=True)

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
    Fund(user=request.user, vounty=vounty, date=date,
         amount=amount, charge=json.dumps(charge)).save()

    subscriptions = Subscription.objects.filter(vounty=vounty, new_fund=True)
    subject = 'Someone has contributed some money to a vounty you\'re subscribed to!'
    send_email(vounty, request.user, subscriptions, subject, None)

    serializer = VountySerializer(vounty)
    return JsonResponse(serializer.data)
