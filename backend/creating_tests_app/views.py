from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from creating_tests_app.models import Test, QuestionBase, OpenQuestion, BooleanQuestion, ChoiceQuestion, ScaleQuestion, \
    BooleanAnswer, AnswerBase, ScaleAnswer, OpenAnswer, ChoiceAnswer, Choice
from creating_tests_app.serializers import TestModelSerializer, QuestionModelSerializer, OpenQuestionModelSerializer, \
    BooleanQuestionModelSerializer, ChoiceOneQuestionModelSerializer, ChoiceMultiQuestionModelSerializer, \
    ScaleQuestionModelSerializer, BooleanAnswerSerializer, OpenAnswerSerializer, ScaleAnswerSerializer, \
    ChoiceAnswerSerializer, OptionsSerializer, ChoiceOneAnswerSerializer, ChoiceMultiAnswerSerializer

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
from creating_tests_app.services import get_full_serialized_answer_data, get_full_serialized_question_data, \
    get_full_serialized_answer_data_list, get_full_serialized_question_data_list, get_and_check_serialized_answer_list


class TestsModelViewSet(ModelViewSet):
    def get_queryset(self):
        return Test.objects.all()

    def get_serializer_class(self):
        if self.action in ['get_questions', 'get_questions_detailed']:
            return QuestionModelSerializer
        # if self.action in ['get_answers', 'get_answers_detailed']:
        #     return QuestionModelSerializer
        return TestModelSerializer

    @action(methods=['get'], detail=True, url_path='questions')
    def get_questions(self, request, pk):
        queryset = QuestionBase.objects.filter(test=pk).all()
        data = get_full_serialized_question_data_list(queryset)
        return Response(data, status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='questions/(?P<number>[^/.]+)')
    def get_questions_detailed(self, request, pk, number):
        object = get_object_or_404(QuestionBase, test=pk, number=number)
        # if user is Admin:
        #     data = get_full_serialized_question_data(object)

        serializer = self.get_serializer(object, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

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
    queryset = QuestionBase.objects.all()
    serializer_class = QuestionModelSerializer


class OpenQuestionViewSet(ModelViewSet):
    queryset = OpenQuestion.objects.all()
    serializer_class = OpenQuestionModelSerializer


class BoolQuestionViewSet(ModelViewSet):
    queryset = BooleanQuestion.objects.all()
    serializer_class = BooleanQuestionModelSerializer


class ChoiceOneQuestionViewSet(ModelViewSet):
    queryset = ChoiceQuestion.objects.filter(one_choice=True).all()
    serializer_class = ChoiceOneQuestionModelSerializer


class ScaleQuestionViewSet(ModelViewSet):
    queryset = ScaleQuestion.objects.all()
    serializer_class = ScaleQuestionModelSerializer


class ChoiceMultiQuestionViewSet(ModelViewSet):
    queryset = ChoiceQuestion.objects.filter(one_choice=False).all()
    serializer_class = ChoiceMultiQuestionModelSerializer


class BooleanAnswerModelViewSet(ModelViewSet):
    queryset = BooleanAnswer.objects.all()
    serializer_class = BooleanAnswerSerializer


class OpenAnswerModelViewSet(ModelViewSet):
    queryset = BooleanAnswer.objects.all()
    serializer_class = OpenAnswerSerializer


class ScaleAnswerModelViewSet(ModelViewSet):
    queryset = BooleanAnswer.objects.all()
    serializer_class = ScaleAnswerSerializer


class ChoiceOneAnswerModelViewSet(ModelViewSet):
    queryset = BooleanAnswer.objects.all()
    serializer_class = ChoiceOneAnswerSerializer


class ChoiceMultiAnswerModelViewSet(ModelViewSet):
    queryset = BooleanAnswer.objects.all()
    serializer_class = ChoiceMultiAnswerSerializer

# class ChoiceModelViewSet(ModelViewSet):
#     queryset = Choice.objects.all()
#     serializer_class = OptionsSerializer



# class UserTestModelViewSet(ModelViewSet):
#     common_user = User.objects.get_or_404(1)  # Mock
#     test = Test.objects.get_or_404(1)  # Mock
#     queryset = Test.objects.filter(user=common_user, test=test)
#
#     # serializer_class =
#
#     @action(methods=['get', ], detail=False, url_path='get-tests-answers')
#     def get_tests_with_answers(self, request):
#         data = AnswerBase.objects.filter()
#         serializer = SolveTestSerializer(data=request.data)
#         return
#
#     @action(methods=['post', ], detail=False, url_path='solve')
#     def solve_test(self, request):
#         serializer = SolveTestSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#
# class QuestionsTestReadOnlyModelViewSet(ReadOnlyModelViewSet):
#     queryset = QuestionBase.objects.filter('test' ==)

# class SolveTestView(ModelViewSet):
#     def get_serializer_class(self):
#         if self.action in ['create', '']:
#             return QuestionsWithAnswersSerializer
#
#     def get_queryset(self):
#         if self.action in ['get', '']:
#             return An
#
#     #@action(methods=['get'], detail=False, url
#     def retrieve(self):
#         pass
