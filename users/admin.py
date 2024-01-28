from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreationForm(forms.ModelForm):
    """Class for create user through admin."""

    class Meta:
        model = User
        fields = ('email', 'first_name')

    def save(self, commit=True):
        """Override save method for add user password in hashed format."""
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUser(UserAdmin):
    """Class for update user instance."""
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')

    # These override the definitions on the base CustomUser
    # that reference specific fields on auth.User.
    fieldsets = (
        (None, {'fields': (
            'email', 'password', 'first_name', 'last_name'
        )}),
        (_('Permissions'), {
            'fields': ('groups', 'user_permissions', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. CustomUser
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password', 'first_name', 'last_name', 'role', 'country', 'nationality',
                'mobile', 'status', 'is_superuser', 'is_staff', 'is_active'
            ),
        }
         ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, CustomUser)