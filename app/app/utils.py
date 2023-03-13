import random
import pytz

from app.models import History, Interaction, Comment
from datetime import datetime, date


def get_actual_date():
    return datetime.now(pytz.utc)


def get_random(list_obj, n=5):
    list_obj = list(list_obj)
    if len(list_obj) >= n:
        return random.sample(list_obj, n)
    else:
        return random.sample(list_obj, len(list_obj))


def video_score(video):
    score = video.like_score() + video.dislike_score() + video.comment_score()
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
