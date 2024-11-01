from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your models here.

class UserRegistrationModel(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()


    def get_profile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        if self.gender == 'Male':
            return static('default_male_avatar.png')
        elif self.gender == 'Female':
            return static('default_female_avatar.png')
        else:
            return static('default_other_avatar.png')

    def __str__(self):
        return f"{self.user.username} - {self.full_name}"


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    max_attendees = models.PositiveIntegerField(default=0)
    booked_count = models.PositiveIntegerField(default=0)

    def is_fully_booked(self):
        return self.booked_count >= self.max_attendees

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)