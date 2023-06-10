from django.db import models
from PIL import Image
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name='Image')
    bio = models.CharField(max_length=100, default='what is your bio')
    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
