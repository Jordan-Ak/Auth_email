
from django.urls import path
from accounts.views import (ListUsersView, CurrentUserView, PasswordResetConfirmView, PasswordResetSendView,
                            SignUpView, UserDeleteView, UserPasswordChangeView,
                            UserEmailVerificationView,
                            UserResendEmailVerificationView)

app_name = 'accounts'

urlpatterns = [
    path('', ListUsersView.as_view(), name = 'list-users'),
    path('signup/', SignUpView.as_view(), name = 'sign-up'),
    path('@me/<str:email>/', CurrentUserView.as_view(), name = 'current-user'),
    path('destroy/<str:email>/', UserDeleteView.as_view(), name = 'user-delete'),
    path('password/change/<str:id>/', UserPasswordChangeView.as_view(), name = 'password-change'),
    path('verify_mail/<str:email_verification_token>/', UserEmailVerificationView.as_view(),
                                                    name = 'email-verify'),
    path('resend_mail/<str:id>/', UserResendEmailVerificationView.as_view(),
                                                   name = 'email-resend'), 
    path('password/reset/', PasswordResetSendView.as_view(), name = 'password-reset'),
    path('password/reset/<str:password_reset_token>/', PasswordResetConfirmView.as_view(),
                                                        name = 'password-reset-confirm'), 
    ]