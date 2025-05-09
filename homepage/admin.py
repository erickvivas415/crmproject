from django.contrib import admin
from django.contrib.auth.models import User  # Import the User model
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Profession, Job

# Register your custom models
admin.site.register(Profile)
admin.site.register(Profession)
admin.site.register(Job)

# Admin site header and titles
admin.site.site_header = 'LIF CRM Administration'
admin.site.site_title = 'Latinos In Finance'
admin.site.index_title = 'Welcome to the Latinos In Finance'

class CustomUserAdmin(UserAdmin):
    # Add 'id' to the list of fields to display
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'date_joined')

    # Optional: Add the id to search fields (if needed)
    search_fields = ('id', 'username', 'email')

# Unregister the default User model and register it with the custom UserAdmin
admin.site.unregister(User)  # Unregister the original User model
admin.site.register(User, CustomUserAdmin)  # Register it with our custom admin class

