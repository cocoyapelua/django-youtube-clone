import random
from datetime import datetime, date
import pytz

from app.models import History, Like, Comment


def get_actual_date():
    return datetime.now(pytz.utc)


def get_random(list_obj, n=5):
    list_obj = list(list_obj)
    if len(list_obj) >= n:
        return random.sample(list_obj, n)
    else:
        return random.sample(list_obj, len(list_obj))


def save_history(video, user, actual_date):
    if user.is_authenticated:
        if History.objects.filter(video=video, user=user).exists():
            history = History.objects.get(video=video, user=user)
            history.date = actual_date
            history.save()
        else:
            history = History.objects.create(video=video, user=user)
            history.save()


def save_like(video, user, action):
    if action == 'dislike':
        if Like.objects.filter(video=video, user=user).exists():
            like = Like.objects.get(video=video, user=user)
            like.dislike = 1
            like.like = 0
            like.save()
        else:
            like = Like.objects.create(video=video, user=user, like=0, dislike=1)
            like.save()
    elif action == 'like':
        if Like.objects.filter(video=video, user=user).exists():
            like = Like.objects.get(video=video, user=user)
            like.dislike = 0
            like.like = 1
            like.save()
        else:
            like = Like.objects.create(video=video, user=user, like=1, dislike=0)
            like.save()


def comments_score(video):
    return Comment.objects.filter(video=video).count() * 1


def dislikes_score(video):
    return Like.objects.filter(video=video, dislike=1).count() * -5


def likes_score(video):
    return Like.objects.filter(video=video, like=1).count() * 10


def video_score(video):
    score = likes_score(video) + dislikes_score(video) + comments_score(video)
    video = video.date.strftime('%Y-%m-%d')
    today = date.today().strftime('%Y-%m-%d')
    if video == today:
        score += 100
    return score


def get_popular_videos(videos):
    list_popularity = []
    for video in videos:
        list_popularity.append({'video': video, 'popularity': video_score(video), 'date': video.date.month})

    total_list = [total_list for total_list in list_popularity if
                  total_list['popularity'] == list_popularity[0]['popularity']]

    if list(filter(lambda x: x['date'] == date.today().month, list_popularity)):
        if len(list_popularity) != len(total_list):
            list_popularity = list(sorted(list_popularity, key=lambda x: x['popularity'], reverse=True))
            return list_popularity[:5]
        else:
            return get_random(list_popularity)
    else:
        return get_random(list_popularity)
