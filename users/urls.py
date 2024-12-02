from django.urls import path
from users import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # path('', views.users_list),
    # path('<int:pk>', views.user_detail),
    path('', views.AddUsers.as_view()),
    path('<int:pk>/', views.UserDetail.as_view()),
    path('add-users/', views.UserList.as_view()),
    path('update-users/<int:pk>/', views.UserUpdate.as_view()),
    path('delete-users/<int:pk>/', views.UserDelete.as_view()),
]