from django.db import models

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField()
    nationality = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    ni_number = models.CharField(max_length=64, blank=True, null=True)
    telephone = models.IntegerField(unique=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(default=0)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
   
    
    class Meta:
        managed = False
        db_table = 'employee'