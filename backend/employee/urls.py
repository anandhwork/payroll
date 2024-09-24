from django.urls import path
from rest_framework import routers
from employee.views.employee import EmployeeViewSet
from employee.views.EmployeeImmigration import EmployeeImmigrationViewSet
from employee.views.EmployeeLeave import EmployeeLeaveViewSet

router = routers.SimpleRouter()

router.register(r'employee', EmployeeViewSet, basename="employee")
router.register(r'immigration', EmployeeImmigrationViewSet, basename="immigration")
router.register(r'leave', EmployeeLeaveViewSet, basename="leave")

urlpatterns = router.urls 
