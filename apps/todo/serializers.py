from django.forms import ValidationError
from rest_framework import serializers
from apps.common.managers import UserManager
from apps.common.serializers import AppCreateModelSerializer, AppModelSerializer, AppReadOnlyModelSerializer, AppWriteOnlyModelSerializer
from todo.models import User,Task
from .models import User
class UserCreateSerializer(AppCreateModelSerializer):
    """
    This is CUD Serializer for User model.
    """
     
    class Meta(AppCreateModelSerializer.Meta):
        model = User
        fields = ('username', 
                  'email',
                  'password',
                  'image')

        
    def validate_email(self, value):
        """ 
        convert the Email into a Lowercase
        """
        
        return value.lower()   
        
    def validate_password(self, password):   
        """ 
        validate the password....
        By  length of password
        and presence of at least one uppercase letter, 
        one lowercase letter, 
        one digit and 
        one special character.
        """ 
                   
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char in '!@#$%&*()+=_-;:?/><[]{},.' for char in password):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return password
    def validate_username(self,userName):
        """
        Validate username ...
        it Should not contain any special characters and should not contain numbers...
        """
               
        if not userName or not userName.strip():
            raise serializers.ValidationError("Username cannot be empty or null.")        
        if any(char in '!@#$%^&*()_+{}:"<>?/.,;[]=-1234567890' for char in userName):
            raise serializers.ValidationError("Username cannot contain special characters and numbers.")
        return userName.lower()   
                 
    def create(self,validated_data): 
        """
        By this method password hashing is implemented....
        """
        
        password = validated_data.pop('password')
        email = validated_data.get('email')
        username = validated_data.pop('username', None)
        image = validated_data.pop('image',None)
        user = User.objects.create_user(password=password,**validated_data)
        if username:
            user.username = username
        user.save()
        if image:
            user.image = image  
        user.save()
        return user
   
class TaskCreateSerializer(AppWriteOnlyModelSerializer):
    """
    This is CUD Serializer for Task model...
    """
    
    due_date = serializers.DateTimeField(required=False)
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Task   
        fields= ('title'
                 ,'description'
                 ,'due_date'
                 ,'task_date'
                 ,'task_time'
                 ,'image'
                 ,'status'
                 ,'created_by')
        extra_kwargs = {
            'due_date': {'required': False},
            'created_by': {'read_only': True},
            'user': {'required': False},
            }
        
    def create(self,validated_data):
        """
        This method is used to create a new task...
        """
        
        user = self.get_user()
        task = Task.objects.create(created_by=user,user=user,**validated_data)
        return task
        
        
        
class TaskRetrieveSerializer(AppReadOnlyModelSerializer):
    """
    This is retrive Serializer for Task Model...
    """       
    
    class Meta(AppReadOnlyModelSerializer.Meta):
        model = Task
        fields=('id'
                 , 'title'
                 ,'description'
                 ,'due_date'
                 ,'task_date'
                 ,'task_time'
                 ,'status'
                 ,'image')
