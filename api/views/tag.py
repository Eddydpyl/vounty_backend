from rest_framework import generics, filters

from api.pagination import StandardPagination
from api.permissions import SafeMethods
from api.serializers import TagSerializer
from api.models import Tag


class TagList(generics.ListCreateAPIView):
    permission_classes = [SafeMethods]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = ['text']
    ordering_fields = ['text']
    ordering = 'text'


class TagDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [SafeMethods]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
