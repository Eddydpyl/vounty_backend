import datetime

from rest_framework import generics

from api.pagination import StandardPagination
from api.permissions import SafeMethods
from api.serializers import VoteSerializer
from api.models import Vote


class VoteList(generics.ListCreateAPIView):
    permission_classes = [SafeMethods]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        date = datetime.datetime.utcnow()
        serializer.save(date=date)


class VoteDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [SafeMethods]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
