from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User, Otp, MailCode
from account.form import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import Group
admin.site.unregister(Group)
@admin.register(Otp, MailCode)
class Admin(admin.ModelAdmin):
    pass
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form, change_form = UserCreationForm, UserChangeForm
    list_display = ('phone', 'email', 'full_name', 'is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        ('Authentication', {'fields': ('phone', 'email', 'password',)}),
        ('personal info', {'fields': ('full_name', 'image',)}),
        ('permission', {'fields': ('is_admin', 'is_email_verify')})
    )
    add_fieldsets = (
        None, {
            'class': ('wide',),
            'fields': ('phone', 'password1', 'password2')
        }
    )
    search_fields = ordering = ('phone',)
    filter_horizontal = []