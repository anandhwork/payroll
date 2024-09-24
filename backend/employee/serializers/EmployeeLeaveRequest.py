from rest_framework import serializers
from employee.models.EmployeeLeaveRequest import EmployeeLeaveRequest

class EmployeeLeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeaveRequest
        fields = '__all__'

    