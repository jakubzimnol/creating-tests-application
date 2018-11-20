import factory

from creating_tests_app.models import Test, QuestionBase, OpenQuestion, AnswerBase, OpenAnswer, ChoiceAnswer, \
    ScaleAnswer, BooleanAnswer, BooleanQuestion, ScaleQuestion, ChoiceQuestion, Choice


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Choice

    name = "abc choice"


class TestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Test

    name = "test1"
    description = "description"


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AnswerBase
        abstract = True

    user = factory.SelfAttribute('question.test.user')


class OpenAnswerFactory(AnswerFactory):
    class Meta:
        model = OpenAnswer

    answer = "123"


class ChoiceAnswerFactory(AnswerFactory):
    class Meta:
        model = ChoiceAnswer


class ScaleAnswerFactory(AnswerFactory):
    class Meta:
        model = ScaleAnswer

    answer = 1


class BooleanAnswerFactory(AnswerFactory):
    class Meta:
        model = BooleanAnswer

    answer = True


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuestionBase
        abstract = True

    question_content = "question"
    test = factory.SubFactory(TestFactory)
    number = 1


class OpenQuestionFactory(QuestionFactory):
    class Meta:
        model = OpenQuestion

    question_type = QuestionBase.OPEN


class ChoiceOneQuestionFactory(QuestionFactory):
    class Meta:
        model = ChoiceQuestion

    question_type = QuestionBase.CHOICE_ONE


class ChoiceMultiQuestionFactory(QuestionFactory):
    class Meta:
        model = ChoiceQuestion

    question_type = QuestionBase.CHOICE_MULTI


class ScaleQuestionFactory(QuestionFactory):
    class Meta:
        model = ScaleQuestion

    proper_answer = 1
    question_type = QuestionBase.SCALE


class BooleanQuestionFactory(QuestionFactory):
    class Meta:
        model = BooleanQuestion

    proper_answer = False
    question_type = QuestionBase.BOOL
