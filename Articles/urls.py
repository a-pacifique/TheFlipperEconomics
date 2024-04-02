from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, ArticleSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'articles': ArticleSitemap,
}

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('create_article/', views.create_article, name='create_article'),
    path('articles/<slug:article_slug>/', views.view_article, name='view_article'),
    path('search/', views.search, name='search'),
    path('about-us/', views.about, name='about'),
    path('contact-us/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('ads.txt', views.ads_txt, name='ads_txt'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
