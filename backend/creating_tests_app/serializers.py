from rest_framework import serializers

from creating_tests_app.models import Test, QuestionBase, OpenQuestion, ChoiceQuestion, BoolQuestion, ScaleQuestion


class BaseQuestionModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('question_content', 'proper_answer', 'test', 'number')
        abstract = True

    def create_and_set_question_type(self, validated_data, self_class, question_type):
        copy_validated_data = validated_data.copy()
        copy_validated_data['question_type'] = question_type
        return super(self_class, self).create(copy_validated_data)


class QuestionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionBase
        fields = '__all__'


class OpenQuestionModelSerializer(BaseQuestionModelSerializer):
    class Meta:
        model = OpenQuestion
        fields = BaseQuestionModelSerializer.Meta.fields

    def create(self, validated_data):
        return self.create_and_set_question_type(validated_data, OpenQuestionModelSerializer, QuestionBase.OPEN)


class ChoiceOneQuestionModelSerializer(BaseQuestionModelSerializer):
    class Meta:
        model = ChoiceQuestion
        fields = BaseQuestionModelSerializer.Meta.fields

    def create(self, validated_data):
        return self.create_and_set_question_type(
            validated_data, ChoiceOneQuestionModelSerializer, QuestionBase.CHOICE_ONE)


class ChoiceMultiQuestionModelSerializer(BaseQuestionModelSerializer):
    class Meta:
        model = ChoiceQuestion
        fields = BaseQuestionModelSerializer.Meta.fields

    def create(self, validated_data):
        return self.create_and_set_question_type(
            validated_data, ChoiceMultiQuestionModelSerializer, QuestionBase.CHOICE_MULTI)


class BoolQuestionModelSerializer(BaseQuestionModelSerializer):
    class Meta:
        model = BoolQuestion
        fields = BaseQuestionModelSerializer.Meta.fields

    def create(self, validated_data):
        return self.create_and_set_question_type(validated_data, BoolQuestionModelSerializer, QuestionBase.BOOL)


class ScaleQuestionModelSerializer(BaseQuestionModelSerializer):
    class Meta:
        model = ScaleQuestion
        fields = BaseQuestionModelSerializer.Meta.fields

    def create(self, validated_data):
        return self.create_and_set_question_type(validated_data, ScaleQuestionModelSerializer, QuestionBase.SCALE)


class TestModelSerializer(serializers.ModelSerializer):
    questions = QuestionModelSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('name', 'description', 'questions')
