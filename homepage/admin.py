from django.contrib import admin
from .models import Profile, Profession

# Register your models here.
#admin.site.register(Members)
admin.site.register(Profile)
admin.site.register(Profession)
admin.site.site_header = 'LIF CRM Administration'
admin.site.site_title = 'Latinos In Finance'
admin.site.index_title = 'Welcome to the Latinos In Finance'