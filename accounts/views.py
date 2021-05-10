from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema

from accounts.serializers import UserSerializer, PasswordChangeSerializer
from django.contrib.auth import get_user_model

# Create your views here.

@swagger_auto_schema(operation_id='List all Users', operation_description='List of all Users',
                         request_body=UserSerializer,
                         responses={'200': UserSerializer()})
class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAdminUser, ]


class SignUpView(APIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_id='User-Creation', operation_description='Creates a new user',
                         request_body=UserSerializer,
                         responses={'200': 'User Created Successfully'})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({'message':'User Created Successfully'}, status = status.HTTP_201_CREATED)

"""
The Code below works the same as the code used except url problem

class CurrentUserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_id='User-GET', operation_description = 'fetch current user',
                            request_body = UserSerializer,
                            responses ={'200': UserSerializer()})
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @swagger_auto_schema(operation_id = 'User-PUT', operation_description = 'User update',
                            request_body = UserSerializer,
                            responses = {'200': 'User update Successful'})
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial',False)
        serializer = self.serializer_class(data=request.data, instance=request.user, partial=partial)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({'message':'User updated Successfully'})

    @swagger_auto_schema(operation_id = 'User-PATCH', operation_description = 'User partial update',
                            request_body = UserSerializer,
                            responses = {'200': 'User Partial Update Successful'})
    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.put(request, args, kwargs)
"""

class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'email'

    def get_queryset(self):
        """ Queryset filters depending on if user is staff or is current user"""
        if self.request.user.is_staff:
            return get_user_model().objects.all()
        else:
            user = get_user_model().objects.filter(email = self.request.user.email)
            return user


class UserDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'email'
    queryset = get_user_model().objects.all()
        

class UserPasswordChangeView(APIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.serializer_class(data = request.data, instance=request.user,
                                                        context={'request': request})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({'message': 'Password has been changed successfully'}, status=status.HTTP_200_OK)

'''
class UserPasswordChangeView(generics.UpdateAPIView):

    queryset = get_user_model().objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        return  Response({'message': 'Password has been changed successfully'}, status=status.HTTP_200_OK)
'''       