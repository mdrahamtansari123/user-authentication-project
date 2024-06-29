from rest_framework_nested import routers
from django.urls import path, include
from .views import RegisterView,LoginView, AdminView,Market_UserViewSet,CheckUserRoleView

router = routers.SimpleRouter()

router.register('market_user', Market_UserViewSet, basename='market_user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin', AdminView.as_view(), name='admin-view'),
    path('check-user-role/', CheckUserRoleView.as_view(), name='check-user-role'),
   
    
]