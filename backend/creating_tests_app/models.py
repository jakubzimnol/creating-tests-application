from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.compat import MaxValueValidator


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

    def __str__(self):
        return self.question_content

    class Meta:
        ordering = ['number']


class OpenQuestion(QuestionBase):
    user_answer = models.TextField(null=True)
    proper_answer = models.TextField(null=True)


class ChoiceQuestion(QuestionBase):
    one_choice = models.BooleanField(default=False)


class Choice(models.Model):
    choice_name = models.TextField()
    question_options = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE, related_name='options')
    question_user_answer = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE,
                                             related_name='user_answer', null=True)
    question_proper_answer = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE, related_name='proper_answer')


class BoolQuestion(QuestionBase):
    user_answer = models.BooleanField(null=True)
    proper_answer = models.BooleanField()


class ScaleQuestion(QuestionBase):
    user_answer = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    proper_answer = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


class Test(models.Model):
    user = models.ForeignKey('auth.User', related_name='tests', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.name
