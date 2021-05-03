import datetime

from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics, filters

from api.pagination import StandardPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers import CommentSerializer
from api.models import Comment, Vote


class CommentList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter]
    filter_fields = ['vounty__id']
    ordering_fields = ['vote_count', 'date']
    ordering = 'date'

    def perform_create(self, serializer):
        date = datetime.datetime.utcnow()
        serializer.save(date=date)


class CommentDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_comment(request):
    comment_id = request.data.get('id')
    like = request.data.get('like')
    comment = Comment.objects.get(id=comment_id)
    vote = comment.votes.first()

    if not vote:
        date = datetime.datetime.utcnow()
        Vote(user=request.user, content_object=comment, date=date, like=like).save()
        if like: comment.vote_count += 1
        else: comment.vote_count -= 1
        comment.save()
    elif vote.like and not like:
        comment.vote_count -= 2
        comment.save()
        vote.like = like
        vote.save()
    elif not vote.like and like:
        comment.vote_count += 2
        comment.save()
        vote.like = like
        vote.save()

    serializer = CommentSerializer(comment)
    return JsonResponse(serializer.data)
