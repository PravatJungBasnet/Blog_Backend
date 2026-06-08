from rest_framework.viewsets import ModelViewSet
from google.oauth2 import id_token
from google.auth.transport import requests

from blogs.serializers import BlogSerializer
from .models import User, Follow
from .serializers import (
    UserRegisterSerializer,
    UserSerializer,
    UserDetailSerializer,
    FollowSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from rest_framework import status
from blogs.models import Blog
from rest_framework.views import APIView
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        serializer_mapping = {
            "create": UserRegisterSerializer,
            "list": UserSerializer,
            "retrieve": UserDetailSerializer,
        }
        return serializer_mapping.get(self.action, UserSerializer)

    @action(detail=False, methods=["get", "put", "patch"])
    def profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def my_blogs(self, request):
        user = request.user
        blogs = Blog.objects.filter(created_by=user)
        serializer = BlogSerializer(blogs, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def my_bookmarks(self, request):
        user = request.user
        blogs = Blog.objects.filter(
            bookmarks__created_by=user, bookmarks__is_bookmarked=True
        )
        serializer = BlogSerializer(blogs, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GoogleLogin(APIView):
    def post(self, request):
        token = request.data.get("id_token")
        if not token:
            return Response(
                {"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.SOCIALACCOUNT_PROVIDERS["google"]["APP"]["client_id"],
            )

            email = idinfo["email"]
            first_name = idinfo.get("given_name", "")
            last_name = idinfo.get("family_name", "")

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "is_active": True,
                },
            )

            # Create JWT
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            )

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class FollowView(ListCreateAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        id = self.kwargs.get("id")
        user = get_object_or_404(User, id=id)
        return Follow.objects.filter(following=user, is_followed=True)

    def create(self, request, *args, **kwargs):
        id = self.kwargs.get("id")
        user = get_object_or_404(User, id=id)
        if user == self.request.user:
            return Response(
                {"error": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        following, created = Follow.objects.get_or_create(
            following=user, follower=self.request.user
        )
        if not created:
            following.is_followed = not following.is_followed
            following.save(update_fields=["is_followed", "updated_at"])
        serializer = self.get_serializer(following)
        return Response(serializer.data, status=status.HTTP_200_OK)
