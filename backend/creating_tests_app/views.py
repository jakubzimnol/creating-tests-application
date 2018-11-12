from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from creating_tests_app.models import Test, QuestionBase
from creating_tests_app.serializers import TestModelSerializer, QuestionModelSerializer


class TestsModelViewSet(ModelViewSet):
    queryset = Test.objects.all()

    def get_serializer_class(self):
        return TestModelSerializer
    # def get_permissions(self):
    #     return


class QuestionModelViewSet(ModelViewSet):
    queryset = QuestionBase.objects.all()
    serializer_class = QuestionModelSerializer

