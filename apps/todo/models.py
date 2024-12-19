from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.common.managers import UserManager
from apps.common.models import AppImageModel
from apps.common.models.base import COMMON_CHAR_FIELD_MAX_LENGTH, BaseCreationModel, BaseModel, COMMON_NON_NULLABLE_FIELD_CONFIG

class User(AbstractUser,AppImageModel,BaseModel):
    """
        It is a User model for the application... 
    Inherited:
        AbstractUser,
        AppImageModel,
        BaseModel
    Used:
        used for Signup purpose Only....            
    """       
    username=models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH,**COMMON_NON_NULLABLE_FIELD_CONFIG,)
    email = models.EmailField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, unique=True)     
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = []  
    objects = UserManager()
    def __str__(self):       
        return self.username
             
               
    
class Task(AppImageModel,BaseCreationModel):
    """
        It is a Task model for the Application....
        Inherited:
            AppImageModel,
            BaseCreationModel,
        Used:
            used for Task CRUD operations...
        ForeignKey:
            created_by         
    """       
    STATUS_CHOICES = [('pending', 'Pending'),('completed', 'Completed'),]
    
    title = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, choices=STATUS_CHOICES, default='pending',)
    task_date = models.DateField(blank=False)
    task_time = models.TimeField(blank=False)
    is_complete = models.BooleanField(default=False)
    is_delete=models.BooleanField(default=False)
    reminder_time = models.DateTimeField(blank=True, null=True)      
    def __str__(self):       
        return self.title
    
    
  
    
    
    