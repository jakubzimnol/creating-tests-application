from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from creating_tests_app.models import Test, QuestionBase, AnswerBase, Grade
from creating_tests_app.permissions import permission_or, IsOwner, IsAdmin, ReadOnly, IsTestOwner, IsQuestionTestOwner
from creating_tests_app.serializers import TestModelSerializer, OpenQuestionModelSerializer, \
    BooleanQuestionModelSerializer, ChoiceOneQuestionModelSerializer, ChoiceMultiQuestionModelSerializer, \
    ScaleQuestionModelSerializer, EmailSerializer, CheckAnswerSerializer, RankingSerializer
from creating_tests_app.services import get_full_serialized_question_data_list, get_and_check_serialized_answer_list, \
    answer_serializer, question_user_serializer, get_full_serialized_answer_data_list, create_question, create_grade


class TestsModelViewSet(ModelViewSet):
    filter_fields = ('user', 'user_answered')

    def get_queryset(self):
        if self.action in ['ranking']:
            return Grade.objects.filter(test_id=self.kwargs['pk']).order_by('-points')[:10]
        return Test.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'automated_check', 'answers', 'send_email', 'approve_answers', 'ranking']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permission_or(IsOwner, IsAdmin)]
        else:
            permission_classes = [ReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['send_email', ]:
            return EmailSerializer
        if self.action in ['ranking']:
            return RankingSerializer
        return TestModelSerializer

    @action(methods=['get'], detail=True, url_path='answers')
    def get_answers(self, request, pk):
        queryset = AnswerBase.objects.filter(question__test=pk).select_subclasses()
        data = get_full_serialized_answer_data_list(queryset)
        return Response(data, status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='approve-answers', url_name="approve")
    def approve_answers(self, request, pk):
        test = Test.objects.get(id=pk)
        if request.user in test.user_answered.all():
            return Response("You approved your answers", status.HTTP_403_FORBIDDEN)
        test.user_answered.add(request.user)
        create_grade(request.user, test)
        return Response('', status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='automated-check', url_name="check")
    def automated_check(self, request, pk):
        test = Test.objects.get(id=pk)
        if request.user not in test.user_answered.all():
            return Response("You must approve answers first", status.HTTP_403_FORBIDDEN)
        queryset = AnswerBase.objects.filter(question__test=pk).all().select_subclasses()
        user_answers_serialized = get_and_check_serialized_answer_list(queryset)
        grade = get_object_or_404(Grade, test=test, user=request.user)
        if grade:
            grade.update_grade()
        return Response(user_answers_serialized, status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='send-email', url_name="email")
    def send_email(self, request, pk):
        data = {'user_id': request.user.id, 'test_id': pk}
        serializer = EmailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def ranking(self, request, pk):
        grades = self.get_queryset()
        data = [{"user_id": grade.user.id, "points": grade.points} for grade in grades]
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status.HTTP_200_OK)


class AnswersModelViewSet(viewsets.ReadOnlyModelViewSet):
    filter_fields = {'points': ['lt', 'gt', 'exact'],
                     'question': ['exact', ]}

    def get_permissions(self):
        permission_classes = [permission_or(IsQuestionTestOwner, IsAdmin)]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action in ['check']:
            return AnswerBase.objects.get_subclass(id=self.kwargs['pk'])
        return AnswerBase.objects.filter(question=self.kwargs['question_id']).select_subclasses()

    def get_serializer_class(self):
        if self.action in ['check']:
            return CheckAnswerSerializer
        question = QuestionBase.objects.get(id=self.kwargs['question_id'])
        return answer_serializer[question.question_type]

    @action(methods=['put'], detail=True, url_path='check')
    def check(self, request, *args, **kwargs):
        test = Test.objects.get(id=kwargs['test_id'])
        if request.user not in test.user_answered.all():
            return Response("Answers must be approved first", status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)
        instance = self.get_queryset() #get_object_or_404(
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class QuestionMixinGenericViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                                  mixins.UpdateModelMixin, viewsets.GenericViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permission_or(IsTestOwner, IsAdmin)]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return QuestionBase.objects.filter(test=self.kwargs['test_id']).select_subclasses()

    def get_serializer_class(self):
        question = QuestionBase.objects.get(id=self.kwargs['pk'])
        if self.action in ['retrieve', 'destroy', 'update', 'partial_update']:
            return question_user_serializer[question.question_type]
        if self.action in ['answers']:
            return answer_serializer[question.question_type]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = get_full_serialized_question_data_list(queryset)
        return Response(data, status.HTTP_200_OK)


class OpenQuestionCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTestOwner, ]

    def create(self, request, *args, **kwargs):
        return create_question(self, request, *args, **kwargs)

    serializer_class = OpenQuestionModelSerializer


class BooleanQuestionCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTestOwner, ]

    def create(self, request, *args, **kwargs):
        return create_question(self, request, *args, **kwargs)

    serializer_class = BooleanQuestionModelSerializer


class ChoiceOneQuestionCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTestOwner, ]

    def create(self, request, *args, **kwargs):
        return create_question(self, request, *args, **kwargs)

    serializer_class = ChoiceOneQuestionModelSerializer


class ChoiceMultiQuestionCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTestOwner, ]

    def create(self, request, *args, **kwargs):
        return create_question(self, request, *args, **kwargs)

    serializer_class = ChoiceMultiQuestionModelSerializer


class ScaleQuestionCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTestOwner, ]

    def create(self, request, *args, **kwargs):
        return create_question(self, request, *args, **kwargs)

    serializer_class = ScaleQuestionModelSerializer


class AnswerModelViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        test = Test.objects.get(id=self.kwargs['test_id'])
        if self.request.user in test.user_answered.all():
            permission_classes = [ReadOnly, ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        question = QuestionBase.objects.get(id=self.kwargs['question_id'])
        return answer_serializer[question.question_type]

    def get_queryset(self):
        return AnswerBase.objects.filter(question=self.kwargs['question_id'],
                                         user=self.request.user.id).select_subclasses()

    def get_data_with_added_user_and_question(self, request, kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        data['question'] = kwargs['question_id']
        return data

    def create(self, request, *args, **kwargs):
        if self.get_queryset():
            return Response('You can not post more answers', status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=self.get_data_with_added_user_and_question(request, kwargs))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(self.get_queryset())
        serializer = self.get_serializer(instance,
                                         data=self.get_data_with_added_user_and_question(request, kwargs),
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset())
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), id=65874)
        if instance is not None:
            instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
