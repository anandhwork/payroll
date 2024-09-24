from django.db import models

class EmployeeLeaveRequestHistory(models.Model):
    leave_request_history_id = models.AutoField(primary_key=True)
    leave_request_id = models.IntegerField(default=0)
    note = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(default=0)
    updated_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField()
   
    
    class Meta:
        managed = False
        db_table = 'leave_request_history'