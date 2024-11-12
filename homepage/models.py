from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Members(models.Model):
    #liked_by = models.ManyToManyField(User, related_name="liked_quotes")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    #address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    #zip = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    date_joined = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return(f"{self.first_name} {self.last_name}")

gender_choices = (
    ('Female','Female'),
    ('Male','Male'),
    ('Prefer not to say','Prefer not to say'))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    gender = models.CharField(max_length=30, choices=gender_choices, default='Female')
    image = models.ImageField(blank=True, upload_to='images/', default='images/profilepicture.jpg', null=True)
    resume = models.FileField(blank=True, upload_to='resumes/', null=True)
    date_updated = models.DateField(auto_now=True)
    last_seen = models.DateField(auto_now=True)

    
    def __str__(self):
        return(f"{self.user}")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
career_stage_choices = (
    ('Student', 'Student'),
    ('1 - 3 years', '1 - 3 years'),
    ('4 - 6 years', '4 - 6 years'),
    ('7 - 9 years', '7 - 9 years'),
    ('10+ years', '10+ years'),
)
    
class Profession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    linkedin = models.URLField(max_length=200)
    industry = models.CharField(max_length=30)
    career_stage = models.CharField(max_length=30, choices=career_stage_choices, default='Student')
    company = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    industry_interest = models.CharField(max_length=30)
    school = models.CharField(max_length=30)
    major_minor = models.CharField(max_length=30)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    graduation_year = models.IntegerField(max_length=4)
    volunteer_interest = models.CharField(max_length=30)
    date_updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return(f"{self.user}")