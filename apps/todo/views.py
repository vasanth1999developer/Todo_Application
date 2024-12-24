
from datetime import timezone
from apps.common.views.api.base import NonAuthenticatedAPIMixin,AppAPIView
from apps.common.views.api.generic import AppModelCUDAPIViewSet, AppModelCreatePIViewSet, AppModelListAPIViewSet, AppModelRetrieveAPIViewSet
from todo import serializers
from todo.models import User,Task
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.db.models import Prefetch

class LoginApi(NonAuthenticatedAPIMixin,AppAPIView):       
    """LoginApiView API to authenticate a user.."""    
              
    def post(self, request):     
        email = self.get_request().data["username"]
        password = self.get_request().data["password"]          
        user_instance = User.objects.filter(email=email.lower()).first()  
        if user_instance is None :
            return self.send_error_response(data="User Not found...Enter proper email address")
        if not user_instance.check_password(password):
            return self.send_error_response(data="Invalid password")     
        token, created = Token.objects.get_or_create(user=user_instance)        
        return self.send_response(data=token.key)
    
    
class SignUpCreatePIViewViewSet(NonAuthenticatedAPIMixin,AppModelCreatePIViewSet):
   """This SignUp API is used to sign up a user in the application..""" 
   
   serializer_class=serializers.UserCreateSerializer
               
               
class TaskCUDAPIViewSet(AppModelCUDAPIViewSet):
    """This API is used to add, retrieve, update and delete tasks.."""
    
    serializer_class=serializers.TaskCreateSerializer

    def get_queryset(self):
        """
        Override get_queryset() method provided by GenericAPIView ..
        For filtering the task based on the logged in user and their task <pk>..
        """ 
                
        user = self.get_user()
        queryset = Task.objects.filter(user=user,is_delete=False)   
        return queryset
     
    def destroy(self, request, *args, **kwargs):
        """
            Override the destroy() .To get the Instance of the task By filtering User and PK..
        """   
                   
        user=self.get_user()     
        pk=kwargs.get('pk')      
        instance = Task.objects.filter(user=user,pk=pk).first()
        if not instance:
            return self.send_error_response(data="Task not found")
        self.perform_destroy(instance)
        return self.send_response(data="Deleted task successfully..")
     
    def perform_destroy(self, instance):
       """
            Override the perform_destroy().To do a Soft Delete by setting is_Delete=True..
       """
       
       instance.is_delete = True 
       instance.save()      
        
class TaskRetrieveViewSet(AppModelRetrieveAPIViewSet):
    """
    A TaskRetrieveViewSet that provides `retrieve` action..
     
    """ 
    
    serializer_class=serializers.TaskRetrieveSerializer 
    def get_queryset(self):
       """
            Override get_queryset() method provided by GenericAPIView .
            For filtering the task based on the logged in user and their task <pk>..
       """    
            
       user = self.get_user()
       queryset = Task.objects.filter(user=user)
       return queryset
    
class TaskListViewSet(AppModelListAPIViewSet):       
    """
    A TaskListViewSet that provides `list` action...
    """
    
    serializer_class=serializers.TaskRetrieveSerializer 

    
    def get_queryset(self):
        """
            Override get_queryset() method provided by GenericAPIView .
            For filtering the tasks based on the logged in user and their task <pk>..
        """                     
        user = self.get_user()
        queryset = Task.objects.filter(user=user,is_delete=False)
        return queryset        
        
       
    
                
class LogoutUserAPIView(AppAPIView):
    """Invalidate a token and logout user."""
    
    def post(self, *args, **kwargs):
        """ handle the post request"""      
        user = self.get_authenticated_user()
        try:
            user.auth_token.delete()
            return self.send_response()
        except Exception:
            return self.send_error_response()
            
