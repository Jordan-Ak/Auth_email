
from django.urls import path
from accounts.views import (ListUsersView, CurrentUserView,
                            SignUpView,UserDeleteView, UserPasswordChangeView)

app_name = 'accounts'

urlpatterns = [
    path('', ListUsersView.as_view(), name = 'list-users'),
    path('signup/', SignUpView.as_view(), name = 'sign-up'),
    path('@me/<str:email>/', CurrentUserView.as_view(), name = 'current-user'),
    path('destroy/<str:email>/', UserDeleteView.as_view(), name = 'user-delete'),
    path('password/change/<str:id>/', UserPasswordChangeView.as_view(), name = 'password-change')
]