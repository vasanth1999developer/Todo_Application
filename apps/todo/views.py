
from datetime import timezone
from apps.common.views.api.base import NonAuthenticatedAPIMixin,AppAPIView
from apps.common.views.api.generic import AppModelCUDAPIViewSet, AppModelCreatePIViewSet, AppModelRetrieveAPIViewSet
from todo import serializers
from todo.models import User,Task
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.db.models import Prefetch

class LoginApi(NonAuthenticatedAPIMixin,AppAPIView):       
    """
    LoginApiView API to authenticate a user...
     Note:
        There is no need of serializers...    
     Security:
        Allow any user without authentication and Autorization...
        By inheriting NonAuthenticatedAPIMixin...
     Method:
        POST...
     Inherited Classes:
        NonAuthenticatedAPIMixin
        AppAPIView
    """              
    def post(self, request):     
        email = request.data["username"]
        password = request.data["password"]          
        user_instance = User.objects.filter(email=email.lower()).first()  
        if user_instance is None :
            return self.send_error_response(data="User Not found...Enter proper email address")
        if not user_instance.check_password(password):
            return self.send_error_response(data="Invalid password")     
        token, created = Token.objects.get_or_create(user=user_instance)        
        return self.send_response(data=token.key)
    
    
class SignUpCreatePIViewViewSet(NonAuthenticatedAPIMixin,AppModelCreatePIViewSet):
   """
     This SignUp API is used to sign up a user if an user in the application...
     for this API no login and authentication required is required...
     Note:
        it Will use UserSerializer... 
     Security:
        Allow any user without authentication and Autorization...
        By inheriting NonAuthenticatedAPIMixin...
     Method:
        POST...
     Inherited Classes:
        NonAuthenticatedAPIMixin
        AppAPIView...
   """ 
   serializer_class=serializers.UserCreateSerializer
               
               
class TaskCUDAPIViewSet(AppModelCUDAPIViewSet):
    """
    This API is used to add, retrieve, update and delete tasks...
    for this API user must be authenticated...
     Note:
        it Will use TaskSerializer...
     security:
        Allow only authenticated users to access tasks ...
        By default Django provides security...
     Method:
        POST, PUT, DELETE... 
     Operation:
        Create, Update & Delete..
     Inherited Classes:
        AppModelCUDAPIViewSet    
    """
    serializer_class=serializers.TaskCreateSerializer
    def perform_create(self, serializer):         
        """
        Override the perform_create() method provided by CreateModelMixin
        To set the user from the request...
        """
        serializer.save(created_by=self.request.user)
    def get_queryset(self):
        """
        During update...
        Insted of using the queryset...
        Override get_queryset() method provided by GenericAPIView ...
        For filtering the task based on the logged in user and their task <pk>...
        """         
        user = self.request.user
        queryset = Task.objects.filter(created_by=user,is_delete=False)
        pk = self.kwargs.get('pk')  
        if pk:
            queryset = queryset.filter(pk=pk)
        
        return queryset
     
    def destroy(self, request, *args, **kwargs):
        """
            Override the destroy() method provided by DestroyModelMixin...
            To get the Instance of the task By filtering User and PK...
        """              
        user=request.user      
        pk=kwargs.get('pk')      
        instance = Task.objects.filter(created_by=user,pk=pk).first()
        if not instance:
            return self.send_error_response(data="Task not found")
        self.perform_destroy(instance)
        return self.send_response(data="Deleted task successfully...")
     
    def perform_destroy(self, instance):
       """
            Override the perform_destroy() method provided by DestroyModelMixin...
            To do a Soft Delete by setting is_Delete=False...
       """
       instance.is_delete = True 
       instance.save()      
        
class TaskRetrieveViewSet(AppModelRetrieveAPIViewSet):
    """
    A TaskRetrieveViewSet that provides `retrieve` action...
     Note:
        it Will use TaskSerializer...
     security:
        Allow only authenticated users to access tasks ...
        By default Django provides security...
     Method:
        GET...
     Operation:
        Retrieve...
     Inherited Classes:
        AppModelRetrieveAPIViewSet       
    """ 
    serializer_class=serializers.TaskRetrieveSerializer 
    def get_queryset(self):
       """
            Insted of using the queryset...
            Override get_queryset() method provided by GenericAPIView ...
            For filtering the task based on the logged in user and their task <pk>...
       """         
       user = self.request.user
       queryset = Task.objects.filter(created_by=user)
       pk = self.kwargs.get('pk')  
       if pk:
           queryset = queryset.filter(pk=pk,is_delete=False)
        
       return queryset
                
class LogoutUserAPIView(AppAPIView):
    """Invalidate a token and logout user."""
    def post(self, *args, **kwargs):
        user = self.get_authenticated_user()
        try:
            user.auth_token.delete()
            return self.send_response()
        except Exception:
            return self.send_error_response()
            
