import datetime

from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics, filters

from api.pagination import StandardPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers import EntrySerializer
from api.models import Entry, Vote, Vounty
from api.utils import sanitize


class EntryList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter]
    filter_fields = ['vounty__id']
    ordering_fields = ['vote_count', 'granted', 'date']
    ordering = 'date'

    def perform_create(self, serializer):
        date = datetime.datetime.utcnow()
        if 'text' in serializer.validated_data:
            text = sanitize(serializer.validated_data['text'])
            serializer.save(text=text, date=date)
        else: serializer.save(date=date)

        vounty_id = serializer.validated_data['vounty'].id
        vounty = Vounty.objects.get(id=vounty_id)
        vounty.entry_count += 1
        vounty.save()


class EntryDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def perform_update(self, serializer):
        if 'text' in serializer.validated_data:
            text = sanitize(serializer.validated_data['text'])
            serializer.save(text=text)
        else: serializer.save()

    def perform_destroy(self, instance):
        instance.vounty.entry_count -= 1
        instance.vounty.save()
        instance.delete()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_entry(request):
    entry_id = request.data.get('id')
    like = request.data.get('like')
    entry = Entry.objects.get(id=entry_id)
    vote = entry.votes.first()

    if not vote:
        date = datetime.datetime.utcnow()
        Vote(user=request.user, content_object=entry, date=date, like=like).save()
        if like: entry.vote_count += 1
        else: entry.vote_count -= 1
        entry.save()
    elif vote.like and not like:
        entry.vote_count -= 2
        entry.save()
        vote.like = like
        vote.save()
    elif not vote.like and like:
        entry.vote_count += 2
        entry.save()
        vote.like = like
        vote.save()

    serializer = EntrySerializer(entry)
    return JsonResponse(serializer.data)
