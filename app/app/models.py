from django.db import models
from django.conf import settings
from django.urls import reverse

from pytube import extract


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    video = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.video = extract.video_id(self.video)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'pk': self.video})

    def get_likes(self):
        return self.interaction_set.filter(interaction_type='LIKE').count()

    def get_dislikes(self):
        return self.interaction_set.filter(interaction_type='DISLIKE').count()

    def save_like(self, user, interaction):
        if self.interaction_set.filter(user=user).exists():
            like = self.interaction_set.get(user=user)
            like.interaction_type = interaction
            like.save()
        else:
            like = self.interaction_set.create(interaction_type=interaction, user=user)
            like.save()

    def save_history(self, user, actual_date):
        if self.history_set.filter(user=user).exists():
            history = self.history_set.get(user=user)
            history.date = actual_date
            history.save()
        else:
            history = self.history_set.create(user=user)
            history.save()

    def like_score(self):
        return self.interaction_set.filter(interaction_type="LIKE").count() * 10

    def dislike_score(self):
        return self.interaction_set.filter(interaction_type="DISLIKE").count() * -5

    def comment_score(self):
        return self.comment_set.count() * 1

    class Meta:
        indexes = [
            models.Index(fields=['video'])
        ]


class Comment(models.Model):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=140)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('video_list')

    def get_user(self):
        return self.user

    class Meta:
        indexes = [
            models.Index(fields=['video', 'user'])
        ]


class Interaction(models.Model):
    interactions = (
        ("LIKE", "Like"),
        ("DISLIKE", "Dislike"),
    )
    interaction_type = models.CharField(default="LIKE", choices=interactions, max_length=7)
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        default=1
    )

    class Meta:
        unique_together = ('video', 'user')
        indexes = [
            models.Index(fields=['interaction_type'])
        ]

    def __str__(self):
        return self.interaction_type


class History(models.Model):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')
        indexes = [
            models.Index(fields=['user', 'video'])
        ]
