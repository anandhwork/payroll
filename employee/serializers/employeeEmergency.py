from rest_framework import serializers
from employee.models.employeeEmergency import EmployeeEmergency

class EmployeeEmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeEmergency
        fields = '__all__'