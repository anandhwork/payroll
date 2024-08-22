from django.urls import path
from rest_framework import routers
from employee.views.employee import EmployeeViewSet
from employee.views.EmployeeImmigration import EmployeeImmigrationViewSet

router = routers.SimpleRouter()

router.register(r'employee', EmployeeViewSet, basename="employee")
router.register(r'immigration', EmployeeImmigrationViewSet, basename="immigration")

urlpatterns = router.urls 
