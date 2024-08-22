from django.db import models

class EmployeeEmergency(models.Model):
    employee_emergency_id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_person = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_number = models.IntegerField(default=0)
    emergency_contact_relationship = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_email_address = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_home_address = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'employee_emergency'