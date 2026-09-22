from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import Signal
import datetime
from django.utils import timezone
# A new user has registered.exit
user_registered = Signal(providing_args=["user", "request"])

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE)
    user_type = models.CharField(max_length=8, default='Usuario')
    phone = models.CharField(max_length=50, blank=True)
    failds = models.IntegerField(default=0)
    block = models.CharField(max_length=2, default="no")
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=250, blank=True)
    registered = models.BooleanField(default=True )
    active = models.BooleanField(default=True)
    validado = models.BooleanField(default=False)
    thumb = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
    created_at = models.DateTimeField(editable=False,blank=False, null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(UserProfile, self).save(*args, **kwargs)    

def assure_user_profile_exists(pk):
    """
    Creates a user profile if a User exists, but the
    profile does not exist.  Use this in views or other
    places where you don't have the user object but have the pk.
    """
    user = User.objects.get(pk=pk)
    try:
        # fails if it doesn't exist
        userprofile = user.userprofile
    except UserProfile.DoesNotExist:
        userprofile = UserProfile(user=user)
        userprofile.save()
    return

def create_user_profile(**kwargs):
    UserProfile.objects.get_or_create(user=kwargs['user'])

user_registered.connect(create_user_profile)
