from django.contrib import admin
from .models import *

admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(BlogPost)
admin.site.register(Certificate)
admin.site.register(Resume)
admin.site.register(Photo)
admin.site.register(Contact)

admin.site.register(Album)  # Register the Album model in admin