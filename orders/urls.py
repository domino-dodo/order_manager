from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.add_order, name='add_order'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('delivered/<int:order_id>/', views.mark_delivered, name='mark_delivered'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
]