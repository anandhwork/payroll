from rest_framework import serializers
from employee.models.EmployeeLeaveType import EmployeeLeaveType

class EmployeeLeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeaveType
        fields = '__all__'

    