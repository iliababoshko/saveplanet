from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from .models import Tests, Questions, AnswersVariant, ThemeTest, TestAge, Results, Student, AnswerStudent
from users.models import CustomUser
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from fpdf import FPDF
from io import BytesIO
from django.urls import reverse

# Create your views here.



def index(request):
    num_tests = Tests.objects.all().count()
    return render(request, 'index.html',
                  context={'num_tests': num_tests},)


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff


class CreateTest(StaffRequiredMixin, generic.TemplateView):
    template_name = "createtest.html"
    def get_context_data(self, **kwargs):
        context = super(CreateTest, self).get_context_data(**kwargs)
        context['agegroups'] = TestAge.objects.all()
        context['themetests'] = ThemeTest.objects.all()
        return context
    def post(self, request):
        user = request.user
        print("ID пользователя:", user)
        themetestid = request.POST.get("tematest")
        if themetestid == "na":
            themetest = request.POST.get("themetest")
            print("Тематика теста:", themetest)
            fromdate = request.POST.get("fromdate")
            tilldate = request.POST.get("tilldate")
            print("Период проведения теста: с", fromdate, "по", tilldate)
            TT = ThemeTest()
            TT.name = themetest
            TT.fromdate = fromdate
            TT.tilldate = tilldate
            TT.save(force_insert=True)
            test = ThemeTest.objects.latest('id')
        else:
            test = ThemeTest.objects.get(id=themetestid)
        agegroupid = request.POST.get("agegroups")
        print("Возрастная группа:", agegroupid)
        agedef = TestAge.objects.get(id=agegroupid)
        TestDB = Tests()
        TestDB.themetest = test
        TestDB.agedef = agedef
        TestDB.save(force_insert=True)
        q = request.POST.get("q1", None)
        i = 1
        LastTest = Tests.objects.latest('id')
        Question = Questions()
        AnswerVar = AnswersVariant()

        while q != None:

            print(q)
            Question.test = LastTest
            Question.question = q
            Question.save(force_insert=True)
            Question.pk = None
            LastQuestion = Questions.objects.latest('id')
            print("LastQuestion", LastQuestion)
            j = 1
            a = request.POST.get("a"+str(i)+str(j), None)

            while a != None:
                print("Ответ", a)
                AnswerVar.question = LastQuestion
                AnswerVar.varAnswer = a
                t = request.POST.get("t"+str(i)+str(j), None)
                if t != None:
                    AnswerVar.correctAnswer = True
                    print("Правильный")
                else:
                    AnswerVar.correctAnswer = False
                AnswerVar.save(force_insert=True)
                AnswerVar.pk = None
                j += 1
                a = request.POST.get("a"+str(i)+str(j), None)

            i += 1
            q = request.POST.get("q"+str(i), None)

        return HttpResponse("Тест создан")

#@login_required
#def createtest(request):
#    agedef = TestAge.objects.all()
#    return render(request, 'createtest.html',
#                  context={'agedef': agedef},)


class TestsListView(LoginRequiredMixin, generic.ListView):
    model = Tests

    def get_context_data(self, **kwargs):
        context = super(TestsListView, self).get_context_data(**kwargs)
        context['themetest'] = ThemeTest.objects.all()
        return context


class ResultsListView(LoginRequiredMixin, generic.ListView):
    model = Results

    def get_context_data(self, **kwargs):
        context = super(ResultsListView, self).get_context_data(**kwargs)
        tests_id = list(Results.objects.filter(student__user=self.request.user).values_list("test", flat=True).distinct())
        context['tests'] = Tests.objects.filter(pk__in=tests_id)
        return context

    def get_queryset(self):
        return Results.objects.filter(student__user=self.request.user)

    @register.filter
    def in_result(self, test):
        return self.filter(test=test)

class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        context['test'] = Tests.objects.get(id=self.kwargs['pk'])
        context['results'] = Results.objects.filter(test__id=self.kwargs['pk']).filter(student__user=self.request.user).values_list("student", flat=True)
        return context

    def get_queryset(self):
        return Student.objects.filter(test__id=self.kwargs['pk']).filter(user=self.request.user)

    def post(self, request, **kwargs):
        user = request.user
        test = Tests.objects.get(id=self.kwargs['pk'])
        surname = request.POST.get("surname")
        name = request.POST.get("name")
        print(test)
        student = Student()
        student.surname = surname
        student.name = name
        student.test = test
        student.user = user
        student.save(force_insert=True)

        return HttpResponseRedirect('../../students/'+self.kwargs['pk']+'/')


class TestDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tests


            #return response

    def get_context_data(self, **kwargs):
        context = super(TestDetailView, self).get_context_data(**kwargs)
        context['answersvariant'] = AnswersVariant.objects.all()
        #Publisher.objects.annotate(num_books=Count('book', distinct=True)).filter(book__rating__gt=3.0)
        context['trueanswers'] = Questions.answer_true
        sid = self.request.GET.get('sid')
        print(sid)
        if sid != None:
            context['student'] = Student.objects.get(id=sid)

        context['students'] = Student.objects.filter(test__id=self.kwargs['pk']).filter(user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        sid = self.request.GET.get('sid')
        pdf = self.request.GET.get('pdf')
        if pdf != None:
            pdf = FPDF()
            pdf.add_font("Sans", style="", fname="tests/static/fonts/NotoSans-Regular.ttf", uni=True)
            # подключаем жирный шрифт "Sans"
            pdf.add_font("Sans", style="B", fname="tests/static/fonts/NotoSans-Bold.ttf", uni=True)
            # подключаем наклонный шрифт "Sans"
            pdf.add_font("Sans", style="I", fname="tests/static/fonts/NotoSans-Italic.ttf", uni=True)
            # подключаем жирный-наклонный шрифт "Sans"
            pdf.add_font("Sans", style="BI", fname="tests/static/fonts/NotoSans-BoldItalic.ttf", uni=True)
            pdf.add_font("SanSym", style="", fname="tests/static/fonts/NotoSansSymbols2-Regular.ttf", uni=True)
            pdf.add_page()
            pdf.set_font("Sans", size=20)
            test = Tests.objects.get(id=self.kwargs['pk'])
            print(test)
            pdf.write(5, test.themetest.name + " (" + test.agedef.agedef + ")")
            stud = Student.objects.get(id=sid)
            pdf.write(5, stud.surname + " " + stud.name)
            outpdf = BytesIO(pdf.output())
            #response = HttpResponse(outpdf, content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="' + stud.surname + " " + stud.name + " " + test.themetest.name + " (" + test.agedef.agedef + ")" +'.pdf"'
            #response = FileResponse(open('test.pdf', 'rb'))
            #response['Content-Disposition'] = 'attachment; filename="test.pdf"'
            #response['X-Sendfile'] = 'test.pdf'
            outpdf.seek(0)
            return FileResponse(outpdf, as_attachment=True, filename=stud.surname + " " + stud.name + " " + test.themetest.name + " (" + test.agedef.agedef + ")"+'.pdf')
        else:
            return super().get(request, *args, **kwargs)

class UserResult(LoginRequiredMixin, generic.ListView):
    model = AnswerStudent


    def get_context_data(self, **kwargs):
        context = super(UserResult, self).get_context_data(**kwargs)
        context['test'] = Tests.objects.get(id=self.kwargs['pk1'])
        context['student'] = Student.objects.get(id=self.kwargs['pk2'])
        context['questions'] = Questions.objects.filter(test__id=self.kwargs['pk1'])
        questions_id = list(
            Questions.objects.filter(test__id=self.kwargs['pk1']).values_list("id", flat=True).distinct())
        QAdict = {}
        for q in questions_id:
            qobj = Questions.objects.get(id=q)

            answers = AnswerStudent.objects.filter(question__id=q).filter(student=self.kwargs['pk2'])
            i = 0
            j = 0
            for answer in answers:
                trueanswer=AnswersVariant.objects.filter(question__id=q).filter(varAnswer=answer.answerstud).filter(correctAnswer=True).count()
                if trueanswer == 0:
                    j += 1
                i = i + trueanswer
            if len(answers) == qobj.answer_true and i == qobj.answer_true:
                QAdict.update({q: 'Верно'})
            elif i == 0:
                QAdict.update({q: 'Неверно'})
            elif i > 0 and j == 0:
                QAdict.update({q: 'Неполный ответ'})
            else:
                QAdict.update({q: 'Некоторые ответы неверные'})
        context['qadict'] = QAdict
        return context


    def get_queryset(self):
        print(self.kwargs['pk1'])
        questions_id = list(Questions.objects.filter(test__id=self.kwargs['pk1']).values_list("id", flat=True).distinct())
        print(questions_id)
        return AnswerStudent.objects.filter(question__id__in=questions_id).filter(student__user=self.request.user).filter(student=self.kwargs['pk2'])


def answerstudent(student, question, answer):
    answerstud = AnswerStudent()
    answerstud.student = student
    answerstud.question = question
    answerstud.answerstud = answer
    answerstud.save()


@login_required
def results(request):
    user = request.user
    tests = Tests.objects.all()
    res = {}
    for test in tests:

        questions = test.questions_in_test
        q_count = test.questions_count

        u = Student.objects.filter(user=user)
        studsintest = list(set(AnswerStudent.students(test, user)))
        if len(studsintest) > 0:
            print(test)
            print("Количество вопросов в данном тесте:", q_count)
            res.update({test.themetest.name + " (" + test.agedef.agedef + ")": []})
            for i in range(len(studsintest)):
                q_right_answers = 0
                student = Student.objects.get(id=studsintest[i])
                studlist = res[test.themetest.name + " (" + test.agedef.agedef + ")"]

                print(student.surname, "отвечал на данный тест")
                for question in questions:
                    print("-", question)
                    studanswers = AnswerStudent.objects.filter(question=question).filter(student=student)
                    varanswers = AnswersVariant.objects.filter(question=question)
                    count_correct_answers_in_question = AnswersVariant.objects.filter(question=question).filter(
                        correctAnswer=True).count()
                    print("Кол-во правильных ответов на этот вопрос:", count_correct_answers_in_question)
                   # studanswers = question.answerstudent_set.order_by('surname')
                    z = 0
                    for studanswer in studanswers:


                        analize_answers = AnswersVariant.objects.filter(question=question).filter(varAnswer=studanswer.answerstud).filter(correctAnswer=True).count()
                        z = z + analize_answers

                        print("--", studanswer.student.surname, studanswer.answerstud)
                        print(analize_answers)
                    if z == count_correct_answers_in_question:
                        print(studanswer.student.surname, "ответил полностью правильно на этот вопрос")
                        print("q_right_answers", q_right_answers)
                        q_right_answers += 1
                mesto = q_count - q_right_answers
                print(studanswer.student.surname, "ответил правильно на", q_right_answers, "вопроса данного теста из", q_count)
                studlist.append({student.surname+" "+student.name: mesto})
                res[test.themetest.name + " (" + test.agedef.agedef + ")"] = studlist
                if mesto == 0:
                    print(studanswer.student.surname, "занял 1 место")
                elif mesto == 1 or mesto == 2:
                    print(studanswer.student.surname, "занял 2 место")
                elif mesto == 3:
                    print(studanswer.student.surname, "занял 3 место")
                else:
                    print(studanswer.student.surname, "не занял призовых мест")
    print(res)
    return render(request, 'results.html',
                  context={'results': res}, )

#@login_required
#def buytest(request):
#    if request.method == "GET":
#        uid = request.GET.get('uid')
#        tid = request.GET.get('tid')
#        test = Tests.objects.get(id=tid)
#        user = CustomUser.objects.get(id=uid)
#        user.tests_set.add(test)
#        return HttpResponseRedirect(reverse('tests'))


@login_required
def answer(request):
    if request.method == "POST":
        studentid = request.POST.get("student")
        print("studentid", studentid)
        test = Tests.objects.get(id=request.POST.get("test"))
        student = Student.objects.get(id=studentid)
        qcount = int(request.POST.get("qcount"))
        print("Кол-во вопросов", qcount)
        for i in range(qcount):
            questionid = int(request.POST.get("questionid"+str(i)))
            question = Questions.objects.get(id=questionid)
            print("ID вопроса", questionid)
            countanswers = int(request.POST.get("countanswers" + str(i)))
            print("Кол-во ответов", countanswers)
            countanswertrue = int(request.POST.get("countanswertrue"+str(i)))
            print("Кол-во правльных ответов", countanswertrue)
            if countanswertrue == 1:
                answer = request.POST.get('answerrad'+str(i))
                if answer == None:
                    answer = ""
                    print(answer)
                answerstudent(student, question, answer)
            else:
                answer = request.POST.getlist('answerchk'+str(i))
                if answer == []:
                    answer = ""
                    print(answer)
                    answerstudent(student, question, answer)
                else:
                    for j in range(len(answer)):
                        print(answer[j])
                        answerstudent(student, question, answer[j])
        qs = test.questions_in_test
        q_count = test.questions_count
        q_right_answers = 0
        for q in qs:
            studanswers = AnswerStudent.objects.filter(question=q).filter(student=student)
            count_correct_answers_in_question = AnswersVariant.objects.filter(question=q).filter(
                correctAnswer=True).count()
            z = 0
            for studanswer in studanswers:
                analize_answers = AnswersVariant.objects.filter(question=q).filter(
                    varAnswer=studanswer.answerstud).filter(correctAnswer=True).count()
                z = z + analize_answers

                print("--", studanswer.student.surname, studanswer.answerstud)
                print(analize_answers)
            if z == count_correct_answers_in_question:
                print(studanswer.student.surname, "ответил полностью правильно на этот вопрос")
                print("q_right_answers", q_right_answers)
                q_right_answers += 1
        mistakes = q_count - q_right_answers
        resDB = Results()
        resDB.test = test
        resDB.student = student
        resDB.mistakes = mistakes
        resDB.save(force_insert=True)
        #author.first_name = request.POST.get("first_name")
        #author.last_name = request.POST.get("last_name")
        #author.date_of_birth = request.POST.get("date_of_birth")
        #author.date_of_death = request.POST.get("date_of_death")
        #author.save()
        return HttpResponse("Ответ принят")
