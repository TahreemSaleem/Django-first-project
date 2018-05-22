
from .models import User ,Task, Milestone
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

admin.register(Milestone)
admin.register(Task)
admin.register(User)

class UserAdmin(DjangoUserAdmin):
  
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('email')}),
         (_('Permissions'), {'fields': ( 'groups', 'user_permissions')}),
        (_('Important dates'), ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ( 'email',)
    list_filter = ()
    search_fields = ( 'email')
    ordering = ('email',) 

