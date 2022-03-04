from django.urls import path 
from time_management_app import views 

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('new/', views.New.as_view(), name='new'),
    path('detail/<int:id>/', views.Detail.as_view(), name='detail'),
    path('detail/<int:id>/edit/', views.Edit.as_view() ,name='edit')
]