from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer


def home(request):
    return render(request, 'pages/home.html', context={}, status=200)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data)


def tweet_detail_view_pure_django(request, tweet_id):
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_view(request):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


def tweet_create_view_pure_django(request):
    if not request.user.is_authenticated:
        if request.is_ajax():
            return JsonResponse({}, status=401)  # not authenticated
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)  # 201 is for created items
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={'form': form})


@api_view(['GET'])
def tweet_list_view(request):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)


def tweet_list_view_pure_django(request):
    qs = Tweet.objects.all()
    tweets_list = [q.serialize() for q in qs]
    data = {
        "response": tweets_list,
    }
    return JsonResponse(data)
