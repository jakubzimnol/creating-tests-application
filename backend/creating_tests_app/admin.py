from django.contrib import admin

from creating_tests_app.models import Test, QuestionBase, AnswerBase

admin.site.register(Test)
admin.site.register(QuestionBase)
admin.site.register(AnswerBase)
