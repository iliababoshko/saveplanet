from django.contrib import admin
from .models import Tests, Questions, AnswersVariant, TestAge, ThemeTest, Results, Student, AnswerStudent

# Register your models here.

admin.site.register(TestAge)

admin.site.register(ThemeTest)
admin.site.register(AnswerStudent)
admin.site.register(Results)


@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin):
    list_display = ('themetest', 'agedef')


#@admin.register(UserPay)
#class UserPayAdmin(admin.ModelAdmin):
#    list_display = ('user')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'user', 'test')


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question', 'test')


@admin.register(AnswersVariant)
class AnswersVariantAdmin(admin.ModelAdmin):
    list_display = ('varAnswer', 'correctAnswer', 'question')