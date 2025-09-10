from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.text import slugify
from django.core.files import File
import os
import re
from .models import Post, ContactMessage, AboutPage, Category, Subscriber
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

# Homepage
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'blog_title': "Latest Post",
        'post_date': timezone.now(),
        'page_obj': page_obj,
    }
    return render(request, 'blog/index.html', context)

# Post detail
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(category=post.category).exclude(pk=post.pk)[:3]

    context = {
        'post': post,
        'related_posts': related_posts,
        'post_date': timezone.now()
    }
    return render(request, 'blog/detail.html', context)

# Update a post (example)
def update_post(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id) if post_id else Post.objects.first()
        if not post:
            return HttpResponse("No post found to update.")

        post.title = "ARUN POST"
        post.content = "This is new content updated through the browser using a view function."

        image_path = os.path.join(settings.MEDIA_ROOT, 'blog_images', 'athe.jpeg')
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                post.image.save('athe.jpeg', File(f), save=False)

        post.save()
        return HttpResponse("Post updated successfully.")
    except Post.DoesNotExist:
        return HttpResponse("Post not found.")

# Latest posts
def latest_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/latest_post.html', {'page_obj': page_obj})

# About page
def about(request):
    about_page = AboutPage.objects.first()
    return render(request, 'blog/about.html', {'about_page': about_page})

# Contact form
def contact_view(request):
    name = email = message = ''
    success_message = ''
    errors = {}

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not name:
            errors['name'] = 'Name is required.'
        if not email:
            errors['email'] = 'Email is required.'
        if not message:
            errors['message'] = 'Message is required.'

        if not errors:
            default_category = Category.objects.first()
            if default_category:
                ContactMessage.objects.create(
                    name=name,
                    email=email,
                    message=message,
                    category=default_category
                )
                success_message = "Thank you for contacting us!"
                name = email = message = ''
            else:
                errors['category'] = "Default category not found."

    context = {
        'name': name,
        'email': email,
        'message': message,
        'success_message': success_message,
        'errors': errors,
        'post_date': timezone.now()
    }
    return render(request, 'blog/contact.html', context)

# Subscribe form
def subscribe_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()

        if not name or not email:
            messages.error(request, 'Please fill in all fields.')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, 'Invalid email format.')
        elif Subscriber.objects.filter(email=email).exists():
            messages.warning(request, 'You are already subscribed.')
        else:
            Subscriber.objects.create(name=name, email=email)
            messages.success(request, 'Subscription successful!')
            return redirect('blog1:subscribe')

    return render(request, 'blog/subscribe.html')

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            # Generate slug if missing
            if not post.slug:
                base_slug = slugify(post.title)
                slug = base_slug
                counter = 1
                while Post.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                post.slug = slug

            # Assign default category if none
            if not post.category:
                default_category = Category.objects.first()
                if default_category:
                    post.category = default_category
                else:
                    messages.error(request, "No category found. Please add one in admin.")
                    return redirect('blog1:create_post')

            post.save()  # Save post to MySQL
            messages.success(request, "✅ Your post has been published successfully!")
            return redirect('blog1:create_post')  # Redirect to same page to show message
        else:
            messages.error(request, "Form contains errors. Please fix them below.")
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})


# Create + View + Update + Delete in single page
@login_required(login_url='blog1:login')
def create_post(request):
    posts = Post.objects.all().order_by('-created_at')  # For listing posts

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            # Generate unique slug if missing
            if not post.slug:
                base_slug = slugify(post.title)
                slug = base_slug
                counter = 1
                while Post.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                post.slug = slug

            # Assign default category if none selected
            if not post.category:
                default_category = Category.objects.first()
                if default_category:
                    post.category = default_category
                else:
                    messages.error(request, "No category found. Please add one in admin.")
                    return redirect('blog/create_post.html')

            post.save()
            messages.success(request, "✅ Your post has been published successfully!")
            return redirect('blog1:create_post')
        else:
            messages.error(request, "Form contains errors. Please fix them below.")
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {
        'form': form,
        'posts': posts,
        'page_title': "Manage Your Blog Posts"  # Default title
    })


# Update Post
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Post updated successfully!")
            return redirect('blog1:create_post')
    else:
        form = PostForm(instance=post)

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/create_post.html', {
        'form': form,
        'posts': posts,
        'edit_post': post,
        'page_title': "Edit Your Blog Post"  # Title for edit mode
    })


# Delete Post
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "🗑️ Post deleted successfully!")
    return redirect('blog1:create_post')


# Intermediate page before create post

def create_blog_page(request):
    if request.user.is_authenticated:  # direct access if already logged in
        return render(request, 'blog/create_blog.html')

# Static / test pages
def new_url(request):
    return render(request, 'blog/new_url.html')

def old_url(request):
    return render(request, 'blog/old_url.html')

def go(request):
    return render(request, 'blog/go.html')

def redirect_to_go(request):
    return redirect('blog1:go_page')

def join_community(request):
    return render(request, 'blog/join_community.html')

def share_story(request):
    return render(request, 'blog/share_story.html')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect to 'next' if exists, else home
            next_url = request.GET.get('next') or '/'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'blog/login.html', {'form': form})



def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! Please log in.")
            return redirect('blog1:login')  # change to your login URL name
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})