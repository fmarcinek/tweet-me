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
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url is not None and is_safe_url(next_url, allowed_hosts=settings.ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form.html', context={'form': form})


def tweet_list_view(request):
    qs = Tweet.objects.all()
    tweets_list = [
        {
            'id': q.id,
            "content": q.content,
            "likes": 12,
        }
        for q in qs
    ]
    data = {
        "response": tweets_list,
    }
    return JsonResponse(data)
