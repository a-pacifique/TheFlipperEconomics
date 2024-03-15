from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('create_article/', views.create_article, name='create_article'),
    path('articles/<slug:article_slug>/', views.view_article, name='view_article'),
    path('search/', views.search, name='search'),
    path('about-us/', views.about, name='about'),
    path('contact-us/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy, name='privacy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)