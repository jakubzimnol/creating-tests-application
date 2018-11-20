from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import serializers

from creating_test_project import settings
from creating_tests_app.models import Test, QuestionBase, OpenQuestion, ChoiceQuestion, BooleanQuestion, ScaleQuestion, \
    BooleanAnswer, OpenAnswer, ScaleAnswer, ChoiceAnswer, Choice, AnswerBase


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
    class Meta(BaseQuestionModelSerializer.Meta):
        model = OpenQuestion

    def create(self, validated_data):
        return self.create_and_set_question_type(validated_data, OpenQuestionModelSerializer, QuestionBase.OPEN)


class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'question_options')
        model = Choice


class OptionsQuestionSerializer(OptionsSerializer):
    class Meta(OptionsSerializer.Meta):
        read_only_fields = ('question_options',)


class ChoiceQuestionBaseSerializer(BaseQuestionModelSerializer):
    options = OptionsQuestionSerializer(many=True)
    proper_answer = OptionsQuestionSerializer(many=True)

    class Meta:
        model = ChoiceQuestion
        fields = ('question_content', 'options', 'proper_answer', 'number', 'test')

    def validate(self, data):
        if not all(elem in data['options'] for elem in data['proper_answer']):
            raise serializers.ValidationError("Proper answer must be included in options")
        return data

    def get_proper_answers(self, proper_answers_names, all_answers):
        proper_answers_objects = []
        for proper_answer in proper_answers_names:
            proper_answers_objects.append(
                next(x for x in all_answers if x.name == proper_answer['name']))
        return proper_answers_objects

    def set_question_in_options(self, options, question):
        for option in options:
            option['question_options'] = question
        return options

    def save_options(self, options):
        serializer = OptionsSerializer(data=options, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def create_and_set_type(self, validated_data, question_type):
        copy_validated_data = validated_data.copy()
        options = copy_validated_data.pop('options')
        proper_answer = copy_validated_data.pop('proper_answer')
        copy_validated_data['one_choice'] = True
        question = self.create_and_set_question_type(
            copy_validated_data, ChoiceQuestionBaseSerializer, question_type)
        self.set_question_in_options(options, question)
        options = self.save_options(options)
        question.proper_answer.set(self.get_proper_answers(proper_answer, options))
        return question


class ChoiceOneQuestionModelSerializer(ChoiceQuestionBaseSerializer):
    def validate_proper_answer(self, value):
        if len(value) > 1:
            raise serializers.ValidationError("ChoiceOneQuestion has only one proper answer, try ChoiceMultiQuestion")
        return value

    def create(self, validated_data):
        return self.create_and_set_type(validated_data, QuestionBase.CHOICE_ONE)


class ChoiceMultiQuestionModelSerializer(ChoiceQuestionBaseSerializer):
    def validate_proper_answer(self, value):
        if len(value) == 1:
            raise serializers.ValidationError(
                "ChoiceMultiQuestion has more than one proper answer, try ChoiceOneQuestion")
        return value

    def create(self, validated_data):
        return self.create_and_set_type(validated_data, QuestionBase.CHOICE_MULTI)


class BooleanQuestionModelSerializer(BaseQuestionModelSerializer):
    class Meta(BaseQuestionModelSerializer.Meta):
        model = BooleanQuestion

    def create(self, validated_data):
        return self.create_and_set_question_type(validated_data, BooleanQuestionModelSerializer, QuestionBase.BOOL)


class ScaleQuestionModelSerializer(BaseQuestionModelSerializer):
    class Meta(BaseQuestionModelSerializer.Meta):
        model = ScaleQuestion

    def create(self, validated_data):
        return self.create_and_set_question_type(validated_data, ScaleQuestionModelSerializer, QuestionBase.SCALE)


class BaseQuestionUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('question_content', 'answer', 'test', 'number')
        abstract = True


class OpenQuestionUserModelSerializer(BaseQuestionUserModelSerializer):
    class Meta(BaseQuestionUserModelSerializer.Meta):
        model = OpenQuestion


class BooleanQuestionUserModelSerializer(BaseQuestionUserModelSerializer):
    class Meta(BaseQuestionUserModelSerializer.Meta):
        model = BooleanQuestion


class ScaleQuestionUserModelSerializer(BaseQuestionUserModelSerializer):
    class Meta(BaseQuestionUserModelSerializer.Meta):
        model = ScaleQuestion


class ChoiceQuestionUserBaseSerializer(BaseQuestionUserModelSerializer):
    options = OptionsQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = ChoiceQuestion
        fields = ('question_content', 'options', 'answer', 'number', 'test')


class TestModelSerializer(serializers.ModelSerializer):
    questions = QuestionModelSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('name', 'description', 'questions')


class BaseAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerBase
        fields = ('answer', 'question', 'user', 'points')
        read_only_fields = ('points', )


class BooleanAnswerSerializer(BaseAnswerSerializer):
    class Meta(BaseAnswerSerializer.Meta):
        model = BooleanAnswer


class OpenAnswerSerializer(BaseAnswerSerializer):
    class Meta(BaseAnswerSerializer.Meta):
        model = OpenAnswer


class ScaleAnswerSerializer(BaseAnswerSerializer):
    class Meta(BaseAnswerSerializer.Meta):
        model = ScaleAnswer


class ChoiceOneAnswerSerializer(BaseAnswerSerializer):
    class Meta(BaseAnswerSerializer.Meta):
        model = ChoiceAnswer

    def validate_answer(self, value):
        if len(value) > 1:
            raise serializers.ValidationError("ChoiceOneQuestion has only one proper answer")
        return value


class ChoiceMultiAnswerSerializer(BaseAnswerSerializer):
    class Meta(BaseAnswerSerializer.Meta):
        model = ChoiceAnswer

    def validate_answer(self, value):
        if len(value) == 1:
            raise serializers.ValidationError("ChoiceMultiQuestion has more than one proper answer")
        return value


class CheckAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerBase
        fields = ('question', 'user', 'points')
        read_only_fields = ('question', 'user')


class EmailSerializer(serializers.Serializer):
    test_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def get_data_from_db(self, validated_data):
        test_id = validated_data['test_id']
        user_id = validated_data['user_id']
        test = get_object_or_404(Test, id=test_id)
        user = get_object_or_404(User, id=user_id)
        answers = AnswerBase.objects.filter(question__test=test_id, user=user_id)
        return user, answers, test

    def generate_mail_message(self, user, answers, test):
        context = {'answers': answers, 'user': user, 'test': test}
        subject, from_email = 'Exam results', settings.EMAIL_HOST_USER
        to = user.email
        html_content = render_to_string('email.html', context)
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        return msg, html_content

    def send_mail(self, validated_data):
        user, answers, test = self.get_data_from_db(validated_data)
        msg, html_content = self.generate_mail_message(user, answers, test)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def create(self, validated_data):
        self.send_mail(validated_data)
        return validated_data

    def update(self, instance, validated_data):
        self.send_mail(validated_data)
        return validated_data
