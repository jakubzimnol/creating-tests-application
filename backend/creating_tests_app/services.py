from creating_tests_app.models import QuestionBase, OpenQuestion, BooleanQuestion, ChoiceQuestion, ScaleQuestion, \
    BooleanAnswer, ScaleAnswer, OpenAnswer, ChoiceAnswer
from creating_tests_app.serializers import OpenQuestionModelSerializer, BooleanQuestionModelSerializer, \
    ChoiceOneQuestionModelSerializer, ChoiceMultiQuestionModelSerializer, ScaleQuestionModelSerializer, \
    BooleanAnswerSerializer, OpenAnswerSerializer, ScaleAnswerSerializer, ChoiceOneAnswerSerializer, \
    ChoiceMultiAnswerSerializer

question_serializer = {
    QuestionBase.BOOL: BooleanQuestionModelSerializer,
    QuestionBase.SCALE: ScaleQuestionModelSerializer,
    QuestionBase.OPEN: OpenQuestionModelSerializer,
    QuestionBase.CHOICE_ONE: ChoiceOneQuestionModelSerializer,
    QuestionBase.CHOICE_MULTI: ChoiceMultiQuestionModelSerializer,
}

question_model = {
    QuestionBase.BOOL: BooleanQuestion,
    QuestionBase.SCALE: ScaleQuestion,
    QuestionBase.OPEN: OpenQuestion,
    QuestionBase.CHOICE_ONE: ChoiceQuestion,
    QuestionBase.CHOICE_MULTI: ChoiceQuestion,
}

answer_model = {
    QuestionBase.BOOL: BooleanAnswer,
    QuestionBase.SCALE: ScaleAnswer,
    QuestionBase.OPEN: OpenAnswer,
    QuestionBase.CHOICE_ONE: ChoiceAnswer,
    QuestionBase.CHOICE_MULTI: ChoiceAnswer,
}

answer_serializer = {
    QuestionBase.BOOL: BooleanAnswerSerializer,
    QuestionBase.SCALE: ScaleAnswerSerializer,
    QuestionBase.OPEN: OpenAnswerSerializer,
    QuestionBase.CHOICE_ONE: ChoiceOneAnswerSerializer,
    QuestionBase.CHOICE_MULTI: ChoiceMultiAnswerSerializer,
}


def get_full_serialized_question_data_list(queryset_list):
    returning_data = []
    for question_base in queryset_list:
        question_object = question_model[question_base.question_type].objects.get(id=question_base.id)
        serializer = question_serializer[question_base.question_type](question_object)
        returning_data.append(serializer.data)
    return returning_data


def get_full_serialized_answer_data_list(queryset_list):
    returning_data = []
    for answer_base in queryset_list:
        answer_object = answer_model[answer_base.question.question_type].objects.get(id=answer_base.id)
        serializer = answer_serializer[answer_base.question.question_type](answer_object)
        returning_data.append(serializer.data)
    return returning_data


def get_and_check_serialized_answer_list(queryset_list):
    returning_data = []
    for answer_base in queryset_list:
        answer_object = answer_model[answer_base.question.question_type].objects.get(id=answer_base.id)
        answer_object.check()
        serializer = answer_serializer[answer_base.question.question_type](answer_object)
        returning_data.append(serializer.data)
    return returning_data


def get_full_serialized_question_data(queryset):
    data = question_model[queryset.question_type].objects.get(id=queryset.id)
    serializer = question_serializer[queryset.question_type](data)
    return serializer.data


def get_full_serialized_answer_data(queryset):
    data = answer_model[queryset.question.question_type].objects.get(id=queryset.id)
    serializer = answer_serializer[queryset.question_type](data)
    return serializer.data
