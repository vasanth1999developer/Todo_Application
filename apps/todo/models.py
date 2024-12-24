from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.todo.Choice import StatusChoices
from apps.common.managers import UserManager
from apps.common.models import AppImageModel
from apps.common.models.base import COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG, COMMON_CHAR_FIELD_MAX_LENGTH, BaseCreationModel, BaseModel, COMMON_NON_NULLABLE_FIELD_CONFIG

class User(AbstractUser,AppImageModel,BaseModel):
    """
        It is a User model for the application...
        
    ********************************  Model Fields ********************************
    pk                  - id
    charField           - username,password
    DateTimeField       - created_at,modified_at
    ImageField          - image
    EmailField          - email      
    """   
        
    date_joined=None
    is_staff=None
    last_name=None
    first_name=None
    is_superuser=None
    last_login=None
    username=models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH,**COMMON_NON_NULLABLE_FIELD_CONFIG,)
    email = models.EmailField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, unique=True)    
     
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = [] 
     
    objects = UserManager()
    
    def __str__(self):       
        return self.username
             
               
    
class Task(AppImageModel,BaseCreationModel):
    """
        It is a Task model for the Application...
        
    ********************************  Model Fields ********************************
    pk                  - id
    charField           - title
    TextField           - description
    DateTimeField       - created_at,modified_at
    ImageField          - image
    """       
    
    title = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, choices=StatusChoices, default='pending',)
    task_date = models.DateField(blank=False)
    task_time = models.TimeField(blank=False)
    is_complete = models.BooleanField(default=False)
    is_delete=models.BooleanField(default=False)
    user = models.ForeignKey(to=User,related_name="get_user",**COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,on_delete=models.CASCADE)  
        
    def __str__(self):       
        return self.title
    
    
  
    
    
    