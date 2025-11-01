from django.test import TestCase, render, redirect
from .models import Project, Skill, Contact

def Home(request):
    porject=Project.objects.all()
    skill=Skill.objects.all()
    return render(request, 'index.html', {'projects':porject,'skills':skill})


