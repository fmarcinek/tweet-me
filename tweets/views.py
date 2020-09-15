from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from .models import Tweet
from .forms import TweetForm


def home(request):
    return render(request, 'pages/home.html', context={}, status=200)


def tweet_detail_view(request, tweet_id):
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status=status)


def tweet_create_view(request):
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)  # 201 is for created items
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={'form': form})


def tweet_list_view(request):
    qs = Tweet.objects.all()
    tweets_list = [q.serialize() for q in qs]
    data = {
        "response": tweets_list,
    }
    return JsonResponse(data)
