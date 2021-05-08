
from django.urls import path
from accounts.views import (ListUsersView, CurrentUserView,
                            SignUpView,)

app_name = 'accounts'

urlpatterns = [
    path('', ListUsersView.as_view(), name = 'list-users'),
    path('signup/', SignUpView.as_view(), name = 'sign-up'),
    path('@me', CurrentUserView.as_view(), name = 'current-user'),
]