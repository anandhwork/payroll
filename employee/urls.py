from django.urls import path
from rest_framework import routers
from employee.views.employee import EmployeeViewSet, EmployeeEmergencyViewSet

router = routers.SimpleRouter()

router.register(r'employee', EmployeeViewSet, basename="employee")
router.register(r'employeeemergency', EmployeeEmergencyViewSet, basename="employeeemergency")

urlpatterns = router.urls 
