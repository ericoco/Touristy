from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

class Favorite(models.Model):
    user_profile = models.ForeignKey(User)
    place_name = models.CharField(max_length=100)
    lat = models.CharField(max_length=30)
    lng = models.CharField(max_length=30)
    content_string = models.CharField(max_length=200)
 
    def __unicode__(self):
        return self.place_name


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    history = models.TextField(blank=True)
    favorites = models.ManyToManyField(Favorite, related_name='favorited_by')

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


