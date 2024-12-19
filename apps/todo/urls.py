from apps.common.routers import AppSimpleRouter
from todo import views
from django.urls import include, path

API_URL_PREFIX = "v1/todo/"
router = AppSimpleRouter()
router.register(f"{API_URL_PREFIX}tasks",views.TaskCUDAPIViewSet)
router.register(f"{API_URL_PREFIX}signup",views.SignUpCreatePIViewViewSet)
router.register(f"{API_URL_PREFIX}tasks-retrieve",views.TaskRetrieveViewSet)


urlpatterns = [
    path(f"{API_URL_PREFIX}login/",views.LoginApi.as_view()),
    path(f"{API_URL_PREFIX}logout/",views.LogoutUserAPIView.as_view()),
 
]+ router.urls
