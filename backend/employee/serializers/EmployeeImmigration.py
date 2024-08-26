from rest_framework import serializers
from employee.models.EmployeeImmigration import EmployeeImmigration
import os

class EmployeeImmigrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeImmigration
        fields = '__all__'

    def validate_passport_doc(self, value):
        return self.validate_file(value)
    
    def validate_brp_doc(self, value):
        return self.validate_file(value)

    def validate_file(self, value):
    # Get the file extension
        ext = os.path.splitext(value.name)[1].lower()
        # List of valid file extensions
        valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        
        if ext not in valid_extensions:
            raise serializers.ValidationError('Unsupported file type. Only PDF and image files are allowed.')
        return value