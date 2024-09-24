from rest_framework import serializers
from employee.models.EmployeeLeaveRequestHistory import EmployeeLeaveRequestHistory

class EmployeeLeaveRequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeaveRequestHistory
        fields = '__all__'

    