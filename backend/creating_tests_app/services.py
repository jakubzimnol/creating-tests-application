from rest_framework.response import Response
from rest_framework import status

from creating_tests_app.models import QuestionBase
from creating_tests_app.serializers import OpenQuestionModelSerializer, BooleanQuestionModelSerializer, \
    ChoiceOneQuestionModelSerializer, ChoiceMultiQuestionModelSerializer, ScaleQuestionModelSerializer, \
    BooleanAnswerSerializer, OpenAnswerSerializer, ScaleAnswerSerializer, ChoiceOneAnswerSerializer, \
    ChoiceMultiAnswerSerializer, BooleanQuestionUserModelSerializer, ScaleQuestionUserModelSerializer, \
    OpenQuestionUserModelSerializer, ChoiceQuestionUserBaseSerializer

question_serializer = {
    QuestionBase.BOOL: BooleanQuestionModelSerializer,
    QuestionBase.SCALE: ScaleQuestionModelSerializer,
    QuestionBase.OPEN: OpenQuestionModelSerializer,
    QuestionBase.CHOICE_ONE: ChoiceOneQuestionModelSerializer,
    QuestionBase.CHOICE_MULTI: ChoiceMultiQuestionModelSerializer,
}

question_user_serializer = {
    QuestionBase.BOOL: BooleanQuestionUserModelSerializer,
    QuestionBase.SCALE: ScaleQuestionUserModelSerializer,
    QuestionBase.OPEN: OpenQuestionUserModelSerializer,
    QuestionBase.CHOICE_ONE: ChoiceQuestionUserBaseSerializer,
    QuestionBase.CHOICE_MULTI: ChoiceQuestionUserBaseSerializer,
}

answer_serializer = {
    QuestionBase.BOOL: BooleanAnswerSerializer,
    QuestionBase.SCALE: ScaleAnswerSerializer,
    QuestionBase.OPEN: OpenAnswerSerializer,
    QuestionBase.CHOICE_ONE: ChoiceOneAnswerSerializer,
    QuestionBase.CHOICE_MULTI: ChoiceMultiAnswerSerializer,
}


def create_question(self, request, *args, **kwargs):
    data = request.data.copy()
    data['test'] = kwargs['test_id']
    serializer = self.get_serializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def get_full_serialized_question_data_list(queryset_list):
    returning_data = []
    for question in queryset_list:
        serializer = question_serializer[question.question_type](question)
        returning_data.append(serializer.data)
    return returning_data


def get_full_serialized_answer_data_list(queryset_list):
    returning_data = []
    for answer in queryset_list:
        serializer = answer_serializer[answer.question.question_type](answer)
        returning_data.append(serializer.data)
    return returning_data


def get_and_check_serialized_answer_list(queryset_list):
    returning_data = []
    for answer in queryset_list:
        answer.check_answer()
        serializer = answer_serializer[answer.question.question_type](answer)
        returning_data.append(serializer.data)
    return returning_data
