from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Project, BlogPost, Certificate, Resume, Skill, Contact, Education, Photo, Album
import os
from django.contrib.auth.decorators import user_passes_test
from .forms import ResumeForm
from django.http import JsonResponse

def home(request):
    projects = Project.objects.order_by('-created')[:6]
    skills = Skill.objects.all()
    educations = Education.objects.order_by('-order')
    photos = Photo.objects.order_by('-created')[:12]  # show latest 12 in home preview

    # background images - up to 10
    bg_dir = os.path.join(settings.MEDIA_ROOT, 'home_bg')
    bg_urls = []
    if os.path.exists(bg_dir):
        for f in sorted(os.listdir(bg_dir))[:10]:
            bg_urls.append(settings.MEDIA_URL + 'home_bg/' + f)

    profile_path = os.path.join(settings.MEDIA_ROOT, 'profile','me.jpg')
    profile = settings.MEDIA_URL + 'profile/me.jpg' if os.path.exists(profile_path) else ''

    context = {
        'projects': projects,
        'skills': skills,
        'bg_urls': bg_urls,
        'profile': profile,
        'educations': educations,
        'photos_preview': photos,
    }
    return render(request, 'home.html', context)

def projects(request):
    items = Project.objects.order_by('-created')
    return render(request, 'projects.html', {'projects': items})

def project_detail(request, pk):
    p = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': p})

def blog_list(request):
    posts = BlogPost.objects.order_by('-published')
    return render(request, 'blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog_detail.html', {'post': post})

@user_passes_test(lambda u: u.is_superuser)   # Only admin can upload
def upload_resume(request):
    form = ResumeForm()
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            Resume.objects.all().delete()  # remove old resume
            form.save()
    return render(request, 'resume.html', {'form': form})


"""def resume_view(request):
    r = Resume.objects.order_by('-uploaded').first()
    return render(request, 'resume.html', {'resume': r})
"""

def certificates(request):
    certs = Certificate.objects.order_by('-id')
    return render(request, 'certificates.html', {'certs': certs})



def photography(request):
    photos = Photo.objects.order_by('-created')
    albums = Album.objects.all().order_by('-id')
    insta_username = "_abhi_shek_1004" 

    context = {
        'photos': photos,
        'albums': albums,
        'insta_username': insta_username,
    } 
    return render(request, 'photography.html', context)

def get_album_photos(request, album_id):
    """AJAX endpoint to get photos from a specific album"""
    try:
        album = Album.objects.get(id=album_id)
        photos = album.photos.all()
        
        photos_data = [{
            'id': photo.id,
            'title': photo.title,
            'description': photo.description,
            'image': photo.image.url,
        } for photo in photos]
        
        return JsonResponse({
            'success': True,
            'photos': photos_data,
            'album_title': album.title
        })
    except Album.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Album not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def contact_submit(request):
    if request.method == 'POST':
        Contact.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        return redirect('main:home')
    return redirect('main:home')
