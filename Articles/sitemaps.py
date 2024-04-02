# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse
from .models import Article

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about_us', 'contact_us']

    def location(self, item):
        return reverse(item)

class ArticleSitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Article.objects.all()[:3]

    def lastmod(self, obj):
        return obj.pub_date
