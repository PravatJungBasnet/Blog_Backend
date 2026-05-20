from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        serializer_mapping = {"create": UserRegisterSerializer, "list": UserSerializer}
        return serializer_mapping.get(self.action, UserSerializer)

    @action(detail=False, methods=["get", "put", "patch"])
    def profile(self, request):
        user = request.user
        print(user.email)
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
