from django.db import models

class EmployeeLeaveRequest(models.Model):
    leave_request_id = models.AutoField(primary_key=True)
    leave_type_id = models.IntegerField(default=0)
    leave_option = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    note = models.CharField(max_length=255, blank=True, null=True)
    notify = models.CharField(max_length=64, blank=True, null=True)
    status = models.IntegerField(default=0)
    created_by = models.IntegerField(default=0)
    created_on = models.DateTimeField()
    updated_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField()
   
    
    class Meta:
        managed = False
        db_table = 'leave_request'