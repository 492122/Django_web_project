from django.contrib import admin

# Register your models here.
from app.models import Like, Question,Answer,Tag,User,Profile
# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Like)
