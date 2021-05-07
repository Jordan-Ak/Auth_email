
from django.urls import path
from accounts.views import ListUsersView

app_name = 'accounts'

urlpatterns = [
    path('', ListUsersView.as_view(), name = 'list-users')
]