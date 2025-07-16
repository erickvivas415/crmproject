from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator

# Create your models here.

gender_choices = (
    ('Female','Female'),
    ('Male','Male'),
    ('Non-Binary','Non-Binary'),
    ('Transgender','Transgender'),
    ('Not Listed','Not Listed'),
    ('Prefer not to say','Prefer not to say'))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=True)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    gender = models.CharField(max_length=30, choices=gender_choices, default='Prefer not to say')
    image = models.ImageField(blank=True, upload_to='images/', default='images/profilepicture.jpg', null=True)
    resume = models.FileField(blank=True, upload_to='resumes/', null=True)
    file_url = models.URLField(max_length=255, blank=True)
    date_updated = models.DateField(auto_now=True)
    last_seen = models.DateField(auto_now=True)

    
    def __str__(self):
        return(f"{self.user}")
    
    def save(self, *args, **kwargs):
            super().save(*args, **kwargs)
            
            # Check if there is an image and it's not the default one
            if self.image and self.image.name != 'images/profilepicture.jpg':
                # Open the image file directly from the storage
                img = Image.open(self.image)

                # Resize the image if it's larger than 300x300
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    
                    # Save the image back to the storage
                    img_io = BytesIO()
                    img.save(img_io, format='JPEG')
                    img_io.seek(0)
                    
                    # Save the modified image back to the field
                    self.image.save(self.image.name, img_io, save=False)
            
            super().save(*args, **kwargs)
    
career_stage_choices = (
    ('Student', 'Student'),
    ('1 - 3 years', '1 - 3 years'),
    ('4 - 6 years', '4 - 6 years'),
    ('7 - 9 years', '7 - 9 years'),
    ('10+ years', '10+ years'),
)
    
class Profession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profession",null=True)
    linkedin = models.URLField(max_length=200)
    industry = models.CharField(max_length=30)
    career_stage = models.CharField(max_length=30, choices=career_stage_choices, default='Student')
    company = models.CharField(max_length=60)
    position = models.CharField(max_length=60)
    industry_interest = models.CharField(max_length=30)
    school = models.CharField(max_length=60)
    major_minor = models.CharField(max_length=30)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=False, default=0.00)
    graduation_year = models.IntegerField(default=1900)
    volunteer_interest = models.CharField(max_length=30)
    date_updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return(f"{self.user}")

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    employer = models.CharField(max_length=100)
    description = models.TextField()
    industry = models.CharField(max_length=50)
    application_link = models.URLField(max_length=500)
    application_deadline = models.DateField()
    employer_logo = models.ImageField(
        upload_to='employer_logos/',
        default='employer_logos/default_logo.jpg',
        blank=True
    )
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employer} - {self.industry}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Automatically resize the logo if it's too large
        if self.employer_logo and self.employer_logo.name != 'employer_logos/default_logo.jpg':
            img = Image.open(self.employer_logo)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                
                # Save the resized image
                img_io = BytesIO()
                img.save(img_io, format='JPEG')
                img_io.seek(0)
                self.employer_logo.save(self.employer_logo.name, img_io, save=False)
            
        super().save(*args, **kwargs)


class Scholarship(models.Model):
    HEARD_ABOUT_CHOICES = [
        ('LinkedIn', 'LinkedIn'),
        ('Facebook', 'Facebook'),
        ('Instagram', 'Instagram'),
        ('LIF Website', 'LIF Website'),
        ('Other', 'Other'),
    ]

    GRADE_YEAR_CHOICES = [
        ('Freshman', 'Freshman'),
        ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="scholarship", null=True)
    heard_about = models.CharField(max_length=50, choices=HEARD_ABOUT_CHOICES, default='LIF Website')
    address = models.CharField(max_length=255)
    area_of_study = models.CharField(max_length=255)
    resilience_growth = models.TextField()
    career_vision_strategy = models.TextField()
    passion_for_finance = models.TextField()
    optional_additonal_info = models.TextField(blank=True, null=True)
    transcript = models.FileField(blank=True, upload_to='transcripts/', null=True)
    award_letter = models.FileField(blank=True, upload_to='award_letters/', null=True)


    def __str__(self):
        return(f"{self.user}")

    class Meta:
        verbose_name = "Scholarship Application"
        verbose_name_plural = "Scholarship Applications"
        ordering = ["user"]