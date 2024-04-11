from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views
from . views import ProfileInfo, PriorityChoiceViewset

router= DefaultRouter()
router.register('list', views.TodoView)
router.register('users', ProfileInfo)
router.register('priority_choice', PriorityChoiceViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationApiView.as_view() , name='register'),
    path('login/', views.UserLoginApiView.as_view() , name='login'),
    path('logout/', views.UserLogoutView.as_view() , name='logout'),
    path('active/<uid64>/<token>/', views.activate, name='activate'),
    path('delete/<int:id>/', views.delete_todo, name='delete'),
]
