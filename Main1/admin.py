from django.contrib import admin
from .models import CustomModel, Post, Profile, Comment, MessageModel, ThreadModel
from .forms import CustomCreationForm, CustomUserForm
from django.contrib.auth.admin import UserAdmin

admin.site.register(Profile)


class CustomAdmin(UserAdmin):
    add_form = CustomCreationForm
    form = CustomUserForm
    list_display = ['username', 'slug', 'email', 'age', 'gender']
    search_fields = ['email', 'username', ]
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('age', 'gender', 'slug',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('age', 'gender', 'slug',)}),)


admin.site.register(CustomModel, CustomAdmin)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(MessageModel)
admin.site.register(ThreadModel)
