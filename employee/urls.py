from django.urls import path
from rest_framework import routers
from employee.views.employee import EmployeeViewSet

router = routers.SimpleRouter()

router.register(r'employee', EmployeeViewSet, basename="employee")

urlpatterns = router.urls 
