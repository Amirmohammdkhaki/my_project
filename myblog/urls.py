from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.post_detail_view, name='blog_detail'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/emoji/', views.add_emoji_reaction, name='add_emoji_reaction'),
    path('post/<int:pk>/emoji/remove/', views.remove_emoji_reaction, name='remove_emoji_reaction'),
    path('post/new/', views.post_create_view, name='post_create'),
    path('post/<int:pk>/edit/', views.post_update_view, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete_view, name='post_delete'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('about/', views.about_me_view, name='about_me'),
    path('projects/', views.projects_view, name='projects'),
    path('computer-vision-codes/', views.computer_vision_code_view, name='computer_vision_codes'),
    path('python/',views.computer_python_view,name='computer_python'),
    path('django/',views.coputer_djngo,name='coputer_djngo'),
    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline'),

]