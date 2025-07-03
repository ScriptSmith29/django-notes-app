from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),

    # Notes
    path('notes/add/', views.add_note, name='add_note'),
    path('notes/<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('notes/<int:note_id>/toggle-important/', views.toggle_important, name='toggle_important'),
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
]