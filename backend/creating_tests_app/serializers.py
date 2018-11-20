from rest_framework import serializers

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
            copy_validated_data, ChoiceOneQuestionModelSerializer, question_type)
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
        fields = ('answer', 'question', 'user')


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

# class AnswerBaseSerializer(serializers.Serializer):
#     question = ?
#     answer = ?
#     class Meta:
#         fields = ('question', 'answer')
#
#     answer_serializer = {
#         QuestionBase.BOOL: BoolQuestionModelSerializer,
#         QuestionBase.OPEN: OpenAnswerSerializer,
#
#     }
#
#     def create(self, validated_data):
#         question = QuestionBase.objects.get_or_404(validated_data['question'])
#         nested_serializer = self.answer_serializer[question.question_type](data=validated_data)
#         nested_serializer.is_valid(raise_exception=True)
#         return nested_serializer.save()
#
#     def update(self, instance, validated_data):
#         question = QuestionBase.objects.get_or_404(validated_data['question'])
#         nested_serializer = self.answer_serializer[question.question_type](instance, data=validated_data)
#         nested_serializer.is_valid(raise_exception=True)
#         return nested_serializer.save()
#
#
# class SolveTestSerializer(serializers.Serializer):
#     answers = AnswerBaseSerializer(many=True)
#
#     def create(self, validated_data):
#         answer_base_serializer = AnswerBaseSerializer(data=validated_data)
#         answer_base_serializer.is_valid(raise_exception=True)
#         return answer_base_serializer.save()
#
#     def update(self, instance, validated_data):
#         answer_base_serializer = AnswerBaseSerializer(instance, data=validated_data)
#         answer_base_serializer.is_valid(raise_exception=True)
#         return answer_base_serializer.save()
