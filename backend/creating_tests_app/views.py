from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from creating_tests_app.models import Test, QuestionBase, OpenQuestion, BoolQuestion, ChoiceQuestion, ScaleQuestion
from creating_tests_app.serializers import TestModelSerializer, QuestionModelSerializer, OpenQuestionModelSerializer, \
    BoolQuestionModelSerializer, ChoiceOneQuestionModelSerializer, ChoiceMultiQuestionModelSerializer, \
    ScaleQuestionModelSerializer


class TestsModelViewSet(ModelViewSet):
    queryset = Test.objects.all()

    def get_serializer_class(self):
        return TestModelSerializer


class QuestionReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = QuestionBase.objects.all()
    serializer_class = QuestionModelSerializer


class OpenQuestionViewSet(ModelViewSet):
    queryset = OpenQuestion.objects.all()
    serializer_class = OpenQuestionModelSerializer


class BoolQuestionViewSet(ModelViewSet):
    queryset = BoolQuestion.objects.all()
    serializer_class = BoolQuestionModelSerializer


class ChoiceOneQuestionViewSet(ModelViewSet):
    queryset = ChoiceQuestion.objects.filter(one_choice=True).all()
    serializer_class = ChoiceOneQuestionModelSerializer


class ScaleQuestionViewSet(ModelViewSet):
    queryset = ScaleQuestion.objects.all()
    serializer_class = ScaleQuestionModelSerializer


class ChoiceMultiQuestionViewSet(ModelViewSet):
    queryset = ChoiceQuestion.objects.filter(one_choice=False).all()
    serializer_class = ChoiceMultiQuestionModelSerializer
