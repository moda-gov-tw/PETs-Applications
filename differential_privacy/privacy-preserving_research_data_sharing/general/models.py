from django.db import models

class FileModel(models.Model):
	file = models.FileField(upload_to = 'upload')
    
class ExecuteModel(models.Model):
    user_name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    caller = models.CharField(max_length=255, default='caller')
    log = models.CharField(max_length=255, default='')
    num_progress = models.IntegerField(default=0)
    skip = models.BooleanField(default=False)
    finish = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user_name