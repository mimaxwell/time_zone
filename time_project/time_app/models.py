from django.db import models

class Unix(models.Model):
    class Meta:
        db_table = 'Unix'
    created = models.DateTimeField(auto_now_add=True)

class TimeZone(models.Model):
    class Meta:
        db_table = 'TimeZone'
    name = models.CharField(max_length=3)
    description = models.CharField(max_length=50)
    utc_offset = models.CharField(max_length=8)

    def __str__(self):
        return self.name