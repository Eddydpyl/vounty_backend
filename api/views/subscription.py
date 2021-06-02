from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from api.pagination import StandardPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers import SubscriptionSerializer
from api.models import Subscription


class SubscriptionList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user__id', 'vounty__id']


class SubscriptionDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
