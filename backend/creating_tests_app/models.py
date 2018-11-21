from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.compat import MaxValueValidator
from model_utils.managers import InheritanceManager


class QuestionBase(models.Model):
    OPEN = 'OP'
    CHOICE_ONE = 'CO'
    CHOICE_MULTI = 'CM'
    BOOL = 'BO'
    SCALE = 'SC'
    QUESTION_TYPE = (
        (OPEN, 'Open question'),
        (CHOICE_ONE, 'Choice one question'),
        (CHOICE_MULTI, 'Choice multi question'),
        (BOOL, 'Boolean question'),
        (SCALE, 'Scale question'),
    )
    question_content = models.TextField(null=False)
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='questions')
    number = models.IntegerField(validators=[MinValueValidator(1)])
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPE, default=OPEN)
    objects = InheritanceManager()

    def __str__(self):
        return self.question_content

    class Meta:
        ordering = ['number']


class OpenQuestion(QuestionBase):
    proper_answer = models.TextField(null=True)


class ChoiceQuestion(QuestionBase):
    one_choice = models.BooleanField(default=False)


class BooleanQuestion(QuestionBase):
    proper_answer = models.BooleanField()


class ScaleQuestion(QuestionBase):
    proper_answer = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


class Test(models.Model):
    user = models.ForeignKey('auth.User', related_name='tests', blank=True, null=True, on_delete=models.CASCADE)
    user_answered = models.ManyToManyField('auth.User')
    name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return " ".join((str(self.pk), self.name))


class Grade(models.Model):
    points = models.FloatField(default=0)
    grade = models.FloatField(default=0)
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE, related_name='grades')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='grades')

    def count_points(self):
        self.points = sum(
            [answer.points for answer in self.user.answers.filter(question__test=self.test).select_subclasses()])

    def count_grade(self):
        if self.test.questions.count():
            self.grade = self.points / self.test.questions.count()

    def update_grade(self):
        self.count_points()
        self.count_grade()


class AnswerBase(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(QuestionBase, on_delete=models.CASCADE, related_name='answer')
    points = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], default=0)
    objects = InheritanceManager()

    def check_answer(self):
        if self.answer == QuestionBase.objects.get_subclass(id=self.question.id).proper_answer:
            self.points = 1
        else:
            self.points = 0
        self.save()
        return self.points


class BooleanAnswer(AnswerBase):
    answer = models.BooleanField


class ChoiceAnswer(AnswerBase):
    def check_answer(self):
        user_proper_answer_amount = sum([answer in self.question.proper_answer for answer in self.answer])
        user_bad_answer_amount = sum([answer not in self.question.proper_answer for answer in self.answer])
        proper_answer_amount = len(self.question.proper_answer)
        self.points = user_proper_answer_amount/(proper_answer_amount+user_bad_answer_amount*2)
        return self.points


class Choice(models.Model):
    name = models.TextField()
    question_options = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE, related_name='options')
    question_user_answer = models.ForeignKey(ChoiceAnswer, on_delete=models.CASCADE,
                                             related_name='answer', null=True)
    question_proper_answer = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE,
                                               related_name='proper_answer', null=True)

    def __str__(self):
        return self.name


class ScaleAnswer(AnswerBase):
    answer = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


class OpenAnswer(AnswerBase):
    answer = models.TextField()
