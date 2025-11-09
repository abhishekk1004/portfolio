from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('resume/', views.upload_resume, name='resume'),
    path('certificates/', views.certificates, name='certificates'),
    path('photography/', views.photography, name='photography'),
    path('get-album-photos/<int:album_id>/', views.get_album_photos, name='get_album_photos'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    # alias so templates can post to 'main:contact'
    path('contact/', views.contact_submit, name='contact'),
]
