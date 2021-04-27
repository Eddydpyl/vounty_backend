from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics, filters

from api.models import User
from api.permissions import IsUser, SafeMethods
from api.pagination import StandardPagination
from api.serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_joined']
    ordering = 'date_joined'


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUser or SafeMethods]
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
