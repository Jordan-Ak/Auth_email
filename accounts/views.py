from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics

from accounts.serializers import UserSerializer

from django.contrib.auth import get_user_model

# Create your views here.


class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAdminUser, ]

    #def get(self, request, *args, **kwargs):
        #""" Returns list of all users."""
        #serializer = self.serializer_class()
        #users = get_user_model().objects.all()
       # return Response(serializer.data)