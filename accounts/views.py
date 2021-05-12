from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics, serializers
from rest_framework.generics import get_object_or_404

from drf_yasg.utils import swagger_auto_schema


from accounts.serializers import (PasswordResetConfirmSerializer, 
                                  PasswordResetSerializer, 
                                  UserSerializer, 
                                  PasswordChangeSerializer)

from accounts.serializers import email_verification_flow
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

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
        return Response({'message':'User Created Successfully, verify your email'},
                                                     status = status.HTTP_201_CREATED)

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
    '''
    Only first_name and last name are subjected to patch request
    due to overidden update method on serializer
    attempt to override anything else silently fails.
    '''
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'email'

    def get_queryset(self) -> get_user_model():
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


    #@swagger_auto_schema(operation_id = 'User-PUT', operation_description = 'User password change',
     #                       request_body = PasswordChangeSerializer,
      #                      responses = {'200': 'User Password change successful'})
    def put(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(),id = kwargs['id'])
        user_id = user.id
       
        if user_id != request.user.id: #Code to ensure the correct user can change the password
           return Response({'message': 'Not Correct user for endpoint'}, status=status.HTTP_400_BAD_REQUEST)

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
    lookup_url_kwarg = 'id'

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        return  Response({'message': 'Password has been changed successfully'}, status=status.HTTP_200_OK)
'''

class UserEmailVerificationView(APIView):
    permission_classes = [permissions.AllowAny]

    #@swagger_auto_schema(operation_id = 'User-GET', operation_description = 'User password change',
     #                       request_body = 'UserEmailVerificationView',
      #                      responses = {'200': 'User email verified successfully'})
    def get(self, request, *args, **kwargs):
        #user = self.request.user
        user= get_object_or_404(get_user_model(),
                                    email_verification_token = kwargs['email_verification_token'])
        if user:
            if user.has_email_verification_token_expired():
             return Response({'error': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)

            elif user.is_verified:
                return Response({'Error' : ' User is already verified'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                user.confirm_email()
                return  Response({'message': 'Your email has been verified.'}, status=status.HTTP_200_OK)

class UserResendEmailVerificationView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    #@swagger_auto_schema(operation_id = 'User-POST', operation_description = 'User resend email verification',
     #                       request_body = 'UserResendEmailVerificationView',
      #                      responses = {'200': 'Verification mail sent successfully'})
    def post(self, request, *args, **kwargs):
        
        user = get_object_or_404(get_user_model(), id = kwargs['id'])        
        user_id = user.id
        
        if user_id != request.user.id: #Code to ensure the correct user can resend email verification
            return Response({'message': 'Not Correct user for endpoint'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_verified:
            return Response({'message': 'User Already Verified'}, status = status.HTTP_400_BAD_REQUEST)

        user.email_verification_token = None
        user.email_token_sent_at = None
        email_verification_flow(user)
        return Response({'message':'Email Verification Re-sent'},
                                                     status = status.HTTP_200_OK)


class PasswordResetSendView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        user = get_object_or_404(get_user_model(),email = data['email'])
        
        if not user:
            return Response({'message': "Email does not exist."})
    
        user.generate_password_reset_token()
        mail_message = 'This is your Password Reset link'
        send_mail(
        'Password Reset at AUTH',
        f'{mail_message}  http://127.0.0.1:8000/accounts/password/reset/{user.password_reset_token}/',
        'from admin@email.com',
        [f'{user.email}'],
        fail_silently = False,)

        return Response({'message':'Password Reset sent successfully'},
                                                     status = status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]


    #@swagger_auto_schema(operation_id = 'User-GET', operation_description = 'User password reset confirm',
     #                       request_body = PasswordChangeSerializer,
      #                      responses = {'200': 'Fill in password reset fields'})
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(),
                                    password_reset_token = kwargs['password_reset_token'])
        if user:
            return Response({'message': 'Fill-in new password fields'})
    
    #@swagger_auto_schema(operation_id = 'User-PUT', operation_description = 'User password reset confirm',
     #                       request_body = PasswordChangeSerializer,
      #                      responses = {'200': 'User Password reset change successful'})
    def put(self, request, *args, **kwargs):
        user= get_object_or_404(get_user_model(),
                                    password_reset_token = kwargs['password_reset_token'])
        if user:
            if user.has_password_reset_token_expired():
                return Response({'error': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)
       
            else:
                serializer = self.serializer_class(data = request.data, instance=user,
                                                        context={'request': request})
                serializer.is_valid(raise_exception = True)
                serializer.save()
                user.confirm_reset()
                return  Response({'message': 'Your Password has been reset.'}, status=status.HTTP_200_OK)
