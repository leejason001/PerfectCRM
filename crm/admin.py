# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from crm.models import UserProfile


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = UserProfile
        fields = ["email", "name"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ["email", "password", "name", "is_active", "is_superuser"]


class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "name", "is_superuser"]
    list_filter = ["is_superuser"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name"]}),
        ("Permissions", {"fields": ["is_active", "is_staff","is_superuser", "role", "user_permissions", "groups"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = ["role", "user_permissions", "groups"]



# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'source', 'consultant', 'contact_type','status', 'date']
    list_filter = ['source', 'consultant', 'status', 'date']
    search_fields = ['source', 'consultant__name']
    filter_horizontal = ['consult_courses', ]


# Register your models here.
admin.site.register(models.CustomerInfo, CustomerAdmin)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.ClassList)
admin.site.register(models.Course)
admin.site.register(models.Role)
admin.site.register(models.Menus)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
admin.site.register(models.Student)
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Branch)
admin.site.register(models.StudentEnrollment)
admin.site.register(models.ContractTemplate)
