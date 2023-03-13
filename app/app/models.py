from django.db import models
from django.conf import settings
from django.urls import reverse


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    video = models.CharField(max_length=255, default='C-ktxCmfTOs')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'pk': self.video})


    def get_likes(self):
        return self.like_set.filter(like=1).count()

    def get_dislikes(self):
        return self.like_set.filter(dislike=1).count()


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


class Like(models.Model):
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        default=1
    )

    class Meta:
        unique_together = ('video', 'user')


class History(models.Model):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        default=1
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')
