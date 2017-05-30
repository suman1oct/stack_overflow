from django.contrib import admin

from authentication.models import User
from forum.models import Question, Answer 

#admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('user_id','username', 'first_name', 'last_name','email', 'image', 'date_of_birth')
	search_fields = ('first_name',)
	list_filter=['first_name',]

#admin.site.register(Question)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ('ques_id','user', 'ques_title', 'ques_description','created_date','updated_date')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ('question','ans_description','user', 'created_date', 'updated_date')
