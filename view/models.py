from django.db import models
from django.utils import timezone

class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, blank=True)
    def __str__(self): return self.name

class Education(models.Model):
    institute = models.CharField(max_length=250)
    degree = models.CharField(max_length=250)
    start_year = models.CharField(max_length=20, blank=True)
    end_year = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-order', 'start_year']

    def __str__(self):
        return f"{self.degree} — {self.institute}"

class Project(models.Model):
    title = models.CharField(max_length=200)
    short_desc = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    live = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    cover = models.ImageField(upload_to='blog/', blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class Certificate(models.Model):
    title = models.CharField(max_length=250)
    issuer = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to='certificates/')
    year = models.CharField(max_length=10, blank=True)
    def __str__(self): return self.title

class Resume(models.Model):
    name = models.CharField(max_length=150, default='Resume')
    file = models.FileField(upload_to='resume/')
    uploaded = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Photo(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=300, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title or f"Photo {self.pk}"

class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.name} - {self.email}"
