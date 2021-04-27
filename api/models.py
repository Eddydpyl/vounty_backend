from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='image', blank=True)
    about = models.TextField(blank=True)


class Tag(models.Model):
    text = models.SlugField(max_length=50)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    date = models.DateTimeField(db_index=True)
    like = models.BooleanField()


class Vounty(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='image', blank=True)
    featured = models.BooleanField(default=False)
    fund_count = models.IntegerField(default=0)
    date = models.DateTimeField(db_index=True)
    prize = models.FloatField(default=0.0)
    tags = models.ManyToManyField(Tag)


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vounty = models.ForeignKey(Vounty, on_delete=models.CASCADE)
    votes = GenericRelation(Vote, related_query_name='entry')
    vote_count = models.IntegerField(default=0)
    granted = models.BooleanField(default=False)
    date = models.DateTimeField(db_index=True)
    text = models.TextField()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vounty = models.ForeignKey(Vounty, on_delete=models.CASCADE)
    votes = GenericRelation(Vote, related_query_name='comment')
    vote_count = models.IntegerField(default=0)
    date = models.DateTimeField(db_index=True)
    text = models.TextField()


class Fund(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vounty = models.ForeignKey(Vounty, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(db_index=True)
    amount = models.FloatField(db_index=True)
    charge = models.TextField()
