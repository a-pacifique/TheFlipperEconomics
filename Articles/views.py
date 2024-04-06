from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, UserLoginForm, ArticleForm, ContactForm
from .models import Article
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponse
import hashlib
from django.db.models import Count

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('admin_articles')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_articles')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    new_articles = Article.objects.filter(published=True)
    top_articles = Article.objects.filter(published=True).order_by('-views')[:5]

    paginator = Paginator(new_articles, 10)
    page_number = request.GET.get('page')
    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'articles': articles, 'top_articles': top_articles})

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})



@login_required
def admin_articles(request):
    articles = Article.objects.all()
    unpublished_articles = articles.filter(published=False)
    published_articles = articles.filter(published=True)
    action = request.GET.get('action')
    article_id = request.GET.get('article_id')

    if action and article_id:
        article = get_object_or_404(Article, pk=article_id)

        if action == 'edit' and (article.author == request.user or request.user.is_superuser):
            if request.method == 'POST':
                form = ArticleForm(request.POST, request.FILES, instance=article)
                if form.is_valid():
                    form.save()
                    return redirect('admin_articles')
            else:
                form = ArticleForm(instance=article)
            return render(request, 'edit_article.html', {'form': form, 'article': article})

        elif action == 'delete' and (article.author == request.user or request.user.is_superuser):
            return render(request, 'delete_article.html', {'article': article})

        elif action == 'publish' and (article.author == request.user or request.user.is_superuser):
            if not article.published:
                article.published = True
                article.save()
                return redirect('admin_articles')

    return render(request, 'admin_articles.html', {
        'unpublished_articles': unpublished_articles,
        'published_articles': published_articles
    })


@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if article.author != request.user and not request.user.is_superuser:
        return redirect('admin_articles')

    if request.method == 'POST':
        article.delete()
        return redirect('admin_articles')

    return render(request, 'articles/delete_article.html', {'article': article})

def view_article(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug, published=True)
    article.views += 1
    article.save()

    # Get suggested articles by the same author
    suggested_articles = Article.objects.filter(author=article.author) \
                                         .exclude(slug=article_slug) \
                                         .order_by('-date_written')[:3]

    return render(request, 'article_detail.html', {'article': article, 'suggested_articles': suggested_articles})


def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query),
            published=True
        ).distinct()

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    try:
        results = paginator.page(page_number)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, 'search_results.html', {'results': results, 'query': query})

def about(request):
    return render(request, 'about.html')

def privacy(request):
    return render(request, 'privacy.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Here, you can send the contact message via email or save it to a database
            # For simplicity, we'll just display a success message
            messages.success(request, 'Thank you for your message!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def ads_txt(request):
    content = "google.com, pub-1335840781247344, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type="text/plain")

