import datetime

from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters

from api.pagination import StandardPagination
from api.permissions import SafeMethods, IsOwner
from api.serializers import EntrySerializer
from api.models import Entry, Vote


class EntryList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated or SafeMethods]
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filter_fields = ['vounty__id']
    search_fields = ['text']
    ordering_fields = ['vote_count', 'granted', 'date']
    ordering = 'date'

    def perform_create(self, serializer):
        date = datetime.datetime.utcnow()
        serializer.save(date=date)


class EntryDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner or SafeMethods]
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_entry(request):
    entry_id = request.data.get('id')
    like = request.data.get('like')

    entry = Entry.objects.get(id=entry_id)

    try:
        vote = Vote.objects.get(content_object=entry)
        if vote.like and not like:
            entry.vote_count -= 2
            entry.save()
            vote.like = like
            vote.save()
        elif not vote.like and like:
            entry.vote_count += 2
            entry.save()
            vote.like = like
            vote.save()
    except:
        date = datetime.datetime.utcnow()
        vote = Vote(user=request.user, content_object=entry, date=date, like=like)
        vote.save()

        if like: entry.vote_count += 1
        else: entry.vote_count -= 1
        entry.save()

    serializer = EntrySerializer(entry)
    return JsonResponse(serializer.data)
