import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters

from api.pagination import StandardPagination
from api.permissions import SafeMethods
from api.serializers import FundSerializer
from api.models import Fund, Vounty


class FundList(generics.ListCreateAPIView):
    permission_classes = [SafeMethods]
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter]
    filter_fields = ['user__id', 'vounty__id']
    ordering_fields = ['date', 'amount']
    ordering = 'date'

    def perform_create(self, serializer):
        date = datetime.datetime.utcnow()
        serializer.save(date=date)

        vounty_id = serializer.validated_data['vounty'].id
        amount = serializer.validated_data['amount']
        vounty = Vounty.objects.get(id=vounty_id)
        vounty.fund_count += 1
        vounty.prize += amount
        vounty.save()


class FundDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [SafeMethods]
    queryset = Fund.objects.all()
    serializer_class = FundSerializer

    def perform_destroy(self, instance):
        instance.vounty.fund_count -= 1
        instance.vounty.prize -= instance.amount
        instance.vounty.save()
        instance.delete()
