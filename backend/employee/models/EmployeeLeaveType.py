from django.db import models

class EmployeeLeaveType(models.Model):
    leave_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.IntegerField(default=0)
    
    
    class Meta:
        managed = False
        db_table = 'leave_type'