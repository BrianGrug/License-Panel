from django.contrib import admin

from polls.models import Question, Reponse

admin.site.register(Question)
admin.site.register(Reponse)
