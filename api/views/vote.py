import datetime

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from api.pagination import StandardPagination
from api.serializers import VoteSerializer
from api.models import Vote


class VoteList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        date = datetime.datetime.utcnow()
        serializer.save(date=date)


class VoteDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
