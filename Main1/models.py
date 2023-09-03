from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from uuid import uuid4


def name_length(value):
    if len(value) < 3:
        raise ValidationError(
            _("%s(value) is not valid,it's too short! "),
            params={"value": value},
        )


CHoices = (('F', 'Female'), ('M', 'Male'),)


class CustomModel(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=100, choices=CHoices, default='Male')
    REQUIRED_FIELDS = ['email', ]
    slug = models.SlugField(max_length=300, default=uuid4, null=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Your name', validators=[name_length])
    slug = models.SlugField(max_length=200, default=uuid4, null=False)
    created = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', default='avatar/female/girl_teen.png',
                              verbose_name='Profile picture')
    follow = models.ManyToManyField(CustomModel, related_name='other_user', symmetrical=False, blank=True,
                                    null=True)

    def __str__(self):
        return str(self.name)


class Post(models.Model):
    user = models.ForeignKey(CustomModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Post\'s name')
    body = models.TextField(verbose_name='Post\'s body')
    picture = models.FileField(upload_to='file/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_now = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomModel, related_name='post_like', blank=True, null=True)
    slug = models.SlugField(max_length=200, default=uuid4, null=False)

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post_connected=self).count()

    def __str__(self):
        return (f'{self.user} \'s {self.title}')


class Comment(models.Model):
    post_connected = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(CustomModel, on_delete=models.CASCADE, blank=True, null=True)
    receiver = models.TextField(verbose_name='comments', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    response = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return (f'{self.receiver} by {self.sender}')


class ThreadModel(models.Model):
    user = models.ForeignKey(CustomModel, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(CustomModel, on_delete=models.CASCADE, related_name='+')
    has_unread = models.BooleanField(default=False)


class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(CustomModel, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(CustomModel, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

