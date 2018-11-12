from rest_framework import serializers

from creating_tests_app.models import Test, QuestionBase


class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class QuestionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBase
        fields = '__all__'
