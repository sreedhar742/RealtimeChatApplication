from django.db import models

# Create your models here.
class ChatGroup(models.Model):
    group_name=models.CharField(max_length=128,unique=True)
    
    def __str__(self) -> str:
        return self.group_name
    
    
from django.contrib.auth.models import User
class GroupMessage(models.Model):
    group=models.ForeignKey(ChatGroup,related_name='caht_messages',on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=300)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.author.username}:{self.body}' 
    class Meta:
        ordering=['-created']