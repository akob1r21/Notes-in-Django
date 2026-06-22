from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import User



class Notes(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'{self.title} --> {self.user.username}'
    
    
