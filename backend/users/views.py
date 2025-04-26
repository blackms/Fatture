from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, UserCreateSerializer,
    UserUpdateSerializer, PasswordChangeSerializer
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_accountant:
            # Accountants can see their own profile and their clients
            return User.objects.filter(
                Q(id=user.id) | Q(id__in=user.clients.all())
            )
        else:
            # Clients can only see their own profile and their accountants
            return User.objects.filter(
                Q(id=user.id) | Q(id__in=user.accountants.all())
            )

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def assign_client(self, request, pk=None):
        if not request.user.is_accountant:
            return Response(
                {"detail": "Only accountants can assign clients."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        client = self.get_object()
        if not client.is_client:
            return Response(
                {"detail": "Can only assign clients to accountants."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.clients.add(client)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def remove_client(self, request, pk=None):
        if not request.user.is_accountant:
            return Response(
                {"detail": "Only accountants can remove clients."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        client = self.get_object()
        request.user.clients.remove(client)
        return Response(status=status.HTTP_204_NO_CONTENT) 