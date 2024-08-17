from django.urls import path
from rest_framework import routers
from auth.views.User import UserViewSet
from auth.views.UpdateUserPasswordView import UpdateUserPasswordView

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename="user")

# Define URL patterns
urlpatterns = [
    path('userpassword/',UpdateUserPasswordView.as_view(), name='user-password'),
]


urlpatterns += router.urls 

