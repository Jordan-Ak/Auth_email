
from django.urls import path
from accounts.views import ListUsersView, CurrentUserView

app_name = 'accounts'

urlpatterns = [
    path('', ListUsersView.as_view(), name = 'list-users'),
    path('@me', CurrentUserView.as_view(), name = 'current-user'),
]