from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep

# Unregister Groups
admin.site.unregister(Group)

# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
	model = Profile

# Extend User model
class UserAdmin(admin.ModelAdmin):
	model = User
	# Only display the fields on the admin page
	fields = ['username']
	inlines = [ProfileInline]


#Unregister initial User
admin.site.unregister(User)

#Reregister initial User
admin.site.register(User, UserAdmin)
#admin.site.register(Profile) - The profile model can either be 
# standalone or integrated into User model 

# Register Meeps
admin.site.register(Meep)

