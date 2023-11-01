import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    pp = models.ImageField(upload_to="profile_images",)
    bg = models.ImageField(upload_to="bg_images",)
    location = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id =  models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)

    image = models.ImageField(upload_to="post_images")
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0,)



class Like(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    
    
class FollowersCount(models.Model):
    #the person who follows user field
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

#   user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user