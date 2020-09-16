"""tweetme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tweets import views as tweets_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tweets_view.home),
    path('create-tweet', tweets_view.tweet_create_view),
    path('tweets', tweets_view.tweet_list_view),
    path('tweets/<int:tweet_id>', tweets_view.tweet_detail_view),
    path('api/tweets/action', tweets_view.tweet_action_view),
    path('api/tweets/<int:tweet_id>/delete', tweets_view.tweet_delete_view),
    path('api/tweets/', include('tweets.urls'))
]
