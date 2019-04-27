from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list),
    path('blog/<int:pk>/', views.post_details),
    path('base', views.render_base),
    path('manage/add_blog', views.add_blog),

]
