from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.compat import MaxValueValidator


class QuestionBase(models.Model):
    question_content = models.TextField(null=False)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    number = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.question_content

    class Meta:
        ordering = ['user', 'number']


class OpenQuestion(QuestionBase):
    user_answer = models.TextField()
    proper_answer = models.TextField()


class ChoiceQuestion(QuestionBase):
    pass


class Choice(models.Model):
    choice_name = models.TextField()
    question_options = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE, related_name='options')
    question_user_answer = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE, related_name='user_answer')
    question_proper_answer = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE, related_name='proper_answer')


class BoolQuestion(QuestionBase):
    user_answer = models.BooleanField()
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
