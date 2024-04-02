# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse
from .models import Article

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about', 'contact', 'search']

    def location(self, item):
        return reverse(item)

class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Article.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.date_written.strftime('%Y-%m-%d')




