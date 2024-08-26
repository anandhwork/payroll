from django.db import models

class EmployeeImmigration(models.Model):
    employee_immigration_id = models.AutoField(primary_key=True)
    employee_id = models.IntegerField(default=0)
    visa_type = models.CharField(max_length=255, blank=True, null=True)
    passport_number = models.IntegerField(default=0)
    passport_valid_from = models.DateField()
    passport_valid_to = models.DateField()
    brp_number = models.IntegerField(default=0)
    brp_valid_from = models.DateField(default=None)
    brp_valid_to = models.DateField(default=None)
    share_code = models.IntegerField(default=0)
    ecs_report = models.IntegerField(default=0)
    reminder_duration = models.IntegerField(default=0)
    passport_doc = models.FileField(upload_to='documents/')
    brp_doc = models.FileField(upload_to='documents/')
    
    class Meta:
        managed = False
        db_table = 'employee_immigration'