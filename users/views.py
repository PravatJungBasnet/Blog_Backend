from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserRegisterSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        serializer_mapping = {"create": UserRegisterSerializer, "list": UserSerializer}
        return serializer_mapping.get(self.action, UserSerializer)
