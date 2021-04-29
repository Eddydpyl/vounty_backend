from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics, filters

from api.models import User
from api.permissions import IsUserOrReadOnly
from api.pagination import StandardPagination
from api.serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_joined']
    ordering = 'date_joined'


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUserOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        if 'image' in serializer.validated_data:
            serializer.instance.image.delete()
        serializer.save()

    def perform_destroy(self, instance):
        instance.image.delete()
        instance.delete()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
