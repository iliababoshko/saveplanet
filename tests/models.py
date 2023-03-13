from django.db import models
from django.urls import reverse
from users.models import CustomUser
from datetime import date
# Create your models here.



class ThemeTest(models.Model):
    name = models.CharField(max_length=255,
                            help_text="Введите название цикла тестов",
                            verbose_name="Цикл тестов")

    fromdate = models.DateField(null=True, blank=True, help_text="Введите дату начала теста",
                      verbose_name="Дата начала теста")
    tilldate = models.DateField(null=True, blank=True, help_text="Введите дату окончания теста",
                      verbose_name="Дата окончания теста")
    class Meta:
        ordering = ['fromdate']
        verbose_name = 'Тематика тестов'
        verbose_name_plural = 'Тематика тестов'

    @property
    def is_overdue(self):
        if self.tilldate and date.today() > self.tilldate:
            return True
        return False


    @property
    def is_notbegin(self):
        if self.fromdate and date.today() < self.fromdate:
            return True
        return False

    @property
    def is_begin(self):
        if self.fromdate and self.tilldate and date.today() >= self.fromdate and date.today() <= self.tilldate:
            return True
        return False



    def __str__(self):
        return self.name


class TestAge(models.Model):
    agedef = models.CharField(max_length=255,
                            help_text="Введите возрастную группу",
                            verbose_name="Возрастная группа")
    class Meta:
        ordering = ['agedef']
        verbose_name = 'Возрастные группы'
        verbose_name_plural = 'Возрастные группы'

    def __str__(self):
        return self.agedef


class Tests(models.Model):
    themetest = models.ForeignKey('ThemeTest', on_delete=models.CASCADE,
                             help_text="Выберите тематику теста",
                             verbose_name="Тематика теста", null=True)
    agedef = models.ForeignKey('TestAge', on_delete=models.CASCADE,
                                  help_text="Выберите возрастную группу для теста",
                                  verbose_name="Возрастная группа", null=True)
    #userpay = models.ManyToManyField(CustomUser,
     #                                help_text="Выберите покупателей",
      #                               verbose_name="Покупатели", null=True)


    @property
    def questions_count(self):
        qcount = self.questions_set.count()
        return qcount

    @property
    def questions_in_test(self):
        questions = self.questions_set.all()
        return questions

   # @property
   # def students(self):
   #     u = Student.objects.filter(user=self._students)
   #     print(u)
   #     questions = self.questions_set.all()
   #     for question in questions:
   #         studanswers  = AnswerStudent.objects.filter(question=question)
   #         count_correct_answers_in_question = AnswersVariant.objects.filter(question=question).filter(
   #             correctAnswer=True).count()
   #         print("Кол-во правильных ответов на этот вопрос:", count_correct_answers_in_question)
   #     return questions

  #  @students.setter
  #  def students(self, value):
  #      self._students = value

 #   def display_userpay(self):
 #       return ', '.join([userpay.email for userpay in self.userpay.all()])
 #   display_userpay.short_description = 'Покупатели'

    def get_absolute_url(self):
        return reverse('tests-detail', args=[str(self.id)])

    class Meta:
        ordering = ['agedef']
        verbose_name = 'Тесты'
        verbose_name_plural = 'Тесты'


    def __str__(self):
        return '%s %s' % (str(self.themetest.name), str(self.agedef.agedef))



class Questions(models.Model):
    question = models.TextField(help_text="Введите вопрос",
                            verbose_name="Вопрос")
    test = models.ForeignKey('Tests', on_delete=models.CASCADE,
                             help_text="Выберите тест, к которому относится вопрос",
                             verbose_name="Тест", null=True)


    class Meta:
        verbose_name = 'Вопросы'
        verbose_name_plural = 'Вопросы'

    @property
    def answer_true(self):
        answer_true_answersvariant = self.answersvariant_set.filter(correctAnswer=True).count()
        return answer_true_answersvariant

    @property
    def answers_count(self):
        acount = self.answersvariant_set.count()
        return acount


    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('question-detail', args=[str(self.id)])


class AnswersVariant(models.Model):
    varAnswer = models.CharField(max_length=255,
                            help_text="Введите вариант ответа",
                            verbose_name="Вариант ответа")

    correctAnswer = models.BooleanField(help_text="Этот ответ правильный?",
                                        verbose_name="Ответ правильный?")
    question = models.ForeignKey('Questions', on_delete=models.CASCADE,
                             help_text="Выберите вопрос, к которому относится этот вариант ответа",
                             verbose_name="Вопрос", null=True)

    class Meta:
        verbose_name = 'Варианты ответов'
        verbose_name_plural = 'Варианты ответов'


    def __str__(self):
        return self.varAnswer

    def get_absolute_url(self):
        return reverse('answer-detail', args=[str(self.id)])


class AnswerStudent(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE,
                                 help_text="Выберите ученика",
                                 verbose_name="Ученик", null=True)

    question = models.ForeignKey('Questions', on_delete=models.CASCADE,
                                 help_text="Выберите вопрос, к которому относится этот ответ",
                                 verbose_name="Вопрос", null=True)
    answerstud = models.CharField(max_length=255,
                            verbose_name="Ответ ученика")

    class Meta:
        verbose_name = 'Ответы учеников'
        verbose_name_plural = 'Ответы учеников'


    def students(test, user):
        s = AnswerStudent.objects.filter(question__test__exact=test).filter(student__user=user).values_list("student", flat=True)
        return s


    @property
    def tematest(self):
        return self.question.test

    @property
    def count_student_answers(self):
        count = AnswerStudent.objects.filter(question=self.question).filter(student=self.student).count()
        return count

    @property
    def count_student_right_answers(self):
        right_answers = AnswersVariant.objects.filter(question=self.question).filter(correctAnswer=True).values_list("varAnswer", flat=True)
        print("right_answers",right_answers)
        count = AnswerStudent.objects.filter(question=self.question).filter(student=self.student).filter(answerstud__in=right_answers).count()
        return count

    @property
    def surn(self):

        return self.surname

    @property
    def count_right_answers(self):
        count = self.question.answersvariant_set.filter(correctAnswer=True).count()
        return count

    @property
    def is_answer_right(self):
        analize_answers = self.question.answersvariant_set.filter(varAnswer=self.answerstud).filter(correctAnswer=True).count()
        print(analize_answers)
        print("кол-во вопросов", self.question.test.questions_set.all().count())
        print("Вопрос", self.question)
        print("Ответ ученика", self.answerstud)
        print("Кол-во ответов на данный вопрос", self.question.answersvariant_set.filter(question=self.question).count()) #Всего ответов на данный вопрос
        print("Кол-во правильных ответов на данный вопрос",
              self.question.answersvariant_set.filter(question=self.question).filter(correctAnswer=True).count())
        if analize_answers == 0:
            return False
        else:
            return True


class Student(models.Model):
    surname = models.CharField(max_length=255,
                                 help_text="Введите фамилию ученика",
                                 verbose_name="Фамилия ученика")
    name = models.CharField(max_length=255,
                                 help_text="Введите имя ученика",
                                 verbose_name="Имя ученика")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Учитель')
    test = models.ForeignKey('Tests', on_delete=models.CASCADE,
                                 help_text="Выберите тест, в котором будет участвовать ученик",
                                 verbose_name="Тест", null=True)

    class Meta:
        verbose_name = 'Ученики'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return self.surname


class Results(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE,
                                help_text="Выберите ученика",
                                verbose_name="Ученик", null=True)
    test = models.ForeignKey('Tests', on_delete=models.CASCADE,
                             help_text="Выберите тест, к которому относится вопрос",
                             verbose_name="Тест", null=True)
    mistakes = models.PositiveSmallIntegerField(help_text="Количество ошибок при ответе на тест",
                                                verbose_name="Ошибки")

    class Meta:
        verbose_name = 'Ошибки'
        verbose_name_plural = 'Ошибки'


    def __str__(self):
        return self.student.surname + " " + self.test.themetest.name + " (" + self.test.agedef.agedef + ")"