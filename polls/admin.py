from django.contrib import admin
from polls.models import Question, Choice, UserProfile, UserVotes
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

# Inline Classes
class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 1

class UserProfileInline(admin.StackedInline):
	model = UserProfile



# Question class Admin
class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		('Question Information', {'fields': ['question_text', 'published_by']}),
		('Date Information', {'fields': ['published_on', 'updated_on']}),
	]
	inlines = [ChoiceInline]
	list_display = ('question_text', 'published_by', 'published_on', 'updated_on', 'total_votes')
	readonly_fields=('published_on', 'updated_on')
	list_filter = ['published_on', 'updated_on', ]
	search_fields = ['question_text', 'published_by']
	list_per_page = 20

admin.site.register(Question, QuestionAdmin)



# UserProfile class Admin
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'anonymous']
	list_filter = ['anonymous']
	list_per_page = 20

admin.site.register(UserProfile, UserProfileAdmin)


# User class Admin
class MyUserAdmin(UserAdmin):
	inlines = [UserProfileInline]
	model = UserProfile
	list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'anonymous']
	# list_filter = ['username', 'first_name', 'last_name']
	def anonymous(self, obj):
		return obj.userprofile.anonymous

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


# Choice class Admin
class ChoiceAdmin(admin.ModelAdmin):
	fieldsets = [
		('Choice Information', {'fields': ['question', 'choice_text', 'votes']}),
	]
	list_display = ['question', 'choice_text', 'votes']

admin.site.register(Choice, ChoiceAdmin)


# UserVotes class Admin
class UserVotesAdmin(admin.ModelAdmin):
	fieldsets = [
		('User Information', {'fields': ['user']}),
		('Choice Information', {'fields': ['choice']}),
		('Question Information', {'fields': ['question']}),
	]
	list_display = ['user', 'choice', 'question']
	search_fields = ['user', 'choice', 'question']

admin.site.register(UserVotes, UserVotesAdmin)