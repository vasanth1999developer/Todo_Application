from apps.common.routers import AppSimpleRouter
from todo import views
from django.urls import include, path

API_URL_PREFIX = "v1/todo/"

router = AppSimpleRouter(
    
)

#API Router for Signup.
router.register(f"{API_URL_PREFIX}signup",views.SignUpCreatePIViewViewSet)

# API Router for Task.
router.register(f"{API_URL_PREFIX}tasks",views.TaskCUDAPIViewSet)
router.register(f"{API_URL_PREFIX}tasks-retrieve",views.TaskRetrieveViewSet)
router.register(f"{API_URL_PREFIX}list-tasks",views.TaskListViewSet)


urlpatterns = [
    path(f"{API_URL_PREFIX}login/",views.LoginApi.as_view()),
    path(f"{API_URL_PREFIX}logout/",views.LogoutUserAPIView.as_view()),
 
]+ router.urls
