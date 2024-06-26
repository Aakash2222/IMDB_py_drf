from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

# Create your models here.

class StreamPlatform(models.Model):

    name = models.CharField(max_length=50)
    about = models.CharField(max_length=100)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name

class WatchList(models.Model):

    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=100)
    platform = models.ForeignKey(StreamPlatform,on_delete=models.CASCADE, related_name='watchlist')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

class Review(models.Model):
    
    rating  = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    desc    = models.CharField(max_length=50)
    watchlist= models.ForeignKey(WatchList, on_delete= models.CASCADE, related_name='reviews')
    active  = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        string = str(self.rating) + " " + str(self.watchlist.title)
        return string
    
    class Meta:
        ordering = ['-created']