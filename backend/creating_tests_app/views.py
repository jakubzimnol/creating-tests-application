from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from creating_tests_app.models import Test, QuestionBase, AnswerBase
from creating_tests_app.serializers import TestModelSerializer, QuestionModelSerializer, OpenQuestionModelSerializer, \
    BooleanQuestionModelSerializer, ChoiceOneQuestionModelSerializer, ChoiceMultiQuestionModelSerializer, \
    ScaleQuestionModelSerializer, BooleanAnswerSerializer
# def get_answers_full_data(queryset_list):
#     returning_data = []
#     for question_base in queryset_list:
#         data = question_model[question_base.question_type].objects.get(id=question_base.id)
#         serializer = question_serializer[question_base.question_type](data)
#         returning_data.append(serializer.data)
#     return returning_data
#
#
# def get_questions_full_data(queryset_list):
#     returning_data = []
#     for question_base in queryset_list:
#         data = question_model[question_base.question_type].objects.get(id=question_base.id)
#         serializer = question_serializer[question_base.question_type](data)
#         returning_data.append(serializer.data)
#     return returning_data
from creating_tests_app.services import get_full_serialized_answer_data, get_full_serialized_answer_data_list, \
    get_full_serialized_question_data_list, get_and_check_serialized_answer_list, answer_serializer, \
    question_user_serializer


class TestsModelViewSet(ModelViewSet):
    def get_queryset(self):
        return Test.objects.all()

    def get_serializer_class(self):
        if self.action in ['get_questions', 'get_questions_detailed']:
            return QuestionModelSerializer
        # if self.action in ['get_answers', 'get_answers_detailed']:
        #     return QuestionModelSerializer
        return TestModelSerializer

    # @action(methods=['get'], detail=True, url_path='questions')
    # def get_questions(self, request, pk):
    #     queryset = QuestionBase.objects.filter(test=pk).all()
    #     data = get_full_serialized_question_data_list(queryset)
    #     return Response(data, status.HTTP_200_OK)
    #
    # @action(methods=['get'], detail=True, url_path='questions/(?P<number>[^/.]+)')
    # def get_questions_detailed(self, request, pk, number):
    #     object = get_object_or_404(QuestionBase, test=pk, number=number)
    #     # if user is Admin:
    #     #     data = get_full_serialized_question_data(object)
    #
    #     serializer = self.get_serializer(object, many=False)
    #     return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='answers')
    def get_answers(self, request, pk):
        queryset = AnswerBase.objects.filter(question__test=pk).all()
        data = get_full_serialized_answer_data_list(queryset)
        return Response(data, status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='answers/(?P<number>[^/.]+)')
    def get_answers_detailed(self, request, pk, number):
        object = get_object_or_404(AnswerBase, question__test=pk, question__number=number)
        data = get_full_serialized_answer_data(object)
        return Response(data, status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def check(self, request, pk, number):
        queryset = AnswerBase.objects.filter(question__test=pk).all()
        user_answers_serialized = get_and_check_serialized_answer_list(queryset)
        return Response(user_answers_serialized, status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='send-email')
    def send_email(self, request, pk, number):
        object = get_object_or_404(AnswerBase, question__test=pk, question__number=number)
        data = get_full_serialized_answer_data(object)
        return Response(data, status.HTTP_200_OK)


class QuestionReadOnlyModelViewSet(ReadOnlyModelViewSet):
    def get_queryset(self):
        if self.action in ['answer', ]:
            question = QuestionBase.objects.get(id=self.kwargs['pk'])
            return question.answer
        elif self.action in ['retrieve', ]:
            return QuestionBase.objects.get(id=self.kwargs['pk]']).select_subclasses()
        elif self.action in ['list', ]:
            return QuestionBase.objects.filter(test=self.kwargs['test_id']).select_subclasses()

    def get_serializer_class(self):
        question = QuestionBase.objects.get(id=self.kwargs['pk'])
        if self.action in ['answer', '']:
            return answer_serializer[question.question_type]
        elif self.action in ['retrieve']:
            return question_user_serializer[question.question_type]
        # raise NotImplementedError()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = get_full_serialized_question_data_list(queryset)
        return Response(data, status.HTTP_200_OK)

    @action(methods=['post', ], detail=True, url_path='answer')
    def answer(self, request, pk):
        # user = User.objects.get(1)
        data = request.data
        # data['user'] = user
        data['question'] = QuestionBase.objects.get(id=self.kwargs['pk'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class OpenQuestionCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = OpenQuestionModelSerializer


class BooleanQuestionCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = BooleanQuestionModelSerializer


class ChoiceOneQuestionCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ChoiceOneQuestionModelSerializer


class ScaleQuestionCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ScaleQuestionModelSerializer


class ChoiceMultiQuestionCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ChoiceMultiQuestionModelSerializer


class BooleanAnswerCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = BooleanAnswerSerializer


class AnswerCreateRetrieveUpdateDestroyViewSet(mixins.CreateModelMixin,
                                               mixins.RetrieveModelMixin,
                                               mixins.UpdateModelMixin,
                                               mixins.DestroyModelMixin,
                                               viewsets.GenericViewSet):
    def get_queryset(self):
        if self.action in ['retrieve']:
            return AnswerBase.objects.get(id=self.kwargs['pk']).select_subclasses()

    def get_serializer_class(self):
        question = QuestionBase.objects.get(id=self.kwargs['question_id'])
        return answer_serializer[question.question_type]
