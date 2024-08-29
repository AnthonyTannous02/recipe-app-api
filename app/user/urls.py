"""
URL Mappings for the user API.
"""

from django.urls import path

from user import APP_NAME, CREATE_COMMAND, ME_COMMAND, TOKEN_COMMAND, views


app_name = APP_NAME

urlpatterns = [
    path(
        CREATE_COMMAND + "/",
        views.CreateUserView.as_view(),
        name=CREATE_COMMAND,
    ),
    path(
        TOKEN_COMMAND + "/",
        views.CreateTokenView.as_view(),
        name=TOKEN_COMMAND,
    ),
    path(
        ME_COMMAND + "/",
        views.ManageUserView.as_view(),
        name=ME_COMMAND,
    ),
]
