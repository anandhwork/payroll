from rest_framework import serializers
from employee.models.EmployeeImmigration import EmployeeImmigration

class EmployeeImmigrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeImmigration
        fields = '__all__'