from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema

from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model

# Create your views here.

@swagger_auto_schema(operation_id='List all Users', operation_description='List of all Users',
                         request_body=UserSerializer,
                         responses={'200': UserSerializer()})
class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAdminUser, ]


class CurrentUserView(APIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_id='User-Creation', operation_description='Creates a new user',
                         request_body=UserSerializer,
                         responses={'200': 'User Created Successfully'})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({'message':'User Created Successfully'}, status = status.HTTP_201_CREATED)

        