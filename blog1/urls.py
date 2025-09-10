from django.urls import path
from blog1 import views
from django.contrib.auth import views as auth_views

app_name = 'blog1'

urlpatterns = [
    path('', views.index, name='index'),

    # About page
    path('about/', views.about, name='about'),

    # Posts
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('latest-posts/', views.latest_posts, name='latest_posts'),

    # Contact & subscribe
    path('contact/', views.contact_view, name='contact'),
    path('subscribe/', views.subscribe_view, name='subscribe'),

    # Static pages
    path('join-community/', views.join_community, name='join_community'),
    path('share-story/', views.share_story, name='share_story'),

    # Blog creation workflow
    path('create-blog/', views.create_blog_page, name='create_blog'),   # intermediate page
    path('create-post/', views.create_post, name='create_post'),        # actual form

    # Manage posts: update & delete
    path('update-post/<int:post_id>/', views.update_post, name='update_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),

    # Login & Logout
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Optional test & redirect URLs (if needed)
    path('new_something_url/', views.new_url, name='new_url'),
    path('old_url/', views.old_url, name='old_url'),
    path('go/', views.go, name='go_page'),
    path('redirect_to_gopage/', views.redirect_to_go, name='redirect_to_go'),
    path('signup/', views.signup_view, name='signup'),

]
