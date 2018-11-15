from rest_framework.routers import DefaultRouter

from creating_tests_app.views import TestsModelViewSet, QuestionReadOnlyModelViewSet, OpenQuestionViewSet, \
    BoolQuestionViewSet, ChoiceOneQuestionViewSet, ChoiceMultiQuestionViewSet, ScaleQuestionViewSet, \
    OpenAnswerModelViewSet, BooleanAnswerModelViewSet, ChoiceOneAnswerModelViewSet, ChoiceMultiAnswerModelViewSet,\
    ScaleAnswerModelViewSet

app_name = 'tests_urls'

router = DefaultRouter()

router.register('tests', TestsModelViewSet, base_name='Tests')
router.register('questions/open', OpenQuestionViewSet, base_name='OpenQuestion')
router.register('questions/choice_one', ChoiceOneQuestionViewSet, base_name='ChoiceOneQuestion')
router.register('questions/choice_multi', ChoiceMultiQuestionViewSet, base_name='ChoiceMultiQuestion')
router.register('questions/boolean', BoolQuestionViewSet, base_name='BooleanQuestion')
router.register('questions/scale', ScaleQuestionViewSet, base_name='ScaleQuestion')
router.register('questions', QuestionReadOnlyModelViewSet, base_name='Questions')
router.register('answers/boolean', BooleanAnswerModelViewSet, base_name='BooleanAnswer')
router.register('answers/open', OpenAnswerModelViewSet, base_name='OpenAnswer')
router.register('answers/choice_one', ChoiceOneAnswerModelViewSet, base_name='BooleanAnswer')
router.register('answers/choice_multi', ChoiceMultiAnswerModelViewSet, base_name='OpenAnswer')
router.register('answers/scale', ScaleAnswerModelViewSet, base_name='OpenAnswer')

#router.register('choices', ChoiceModelViewSetSerializer, base_name='Choices')
#router.register('test/<id>/questions', QuestionsTestReadOnlyModelViewSet, base_name='TestQuestions')
#router.register('test/<id>/answers', AnswersTestModelViewSet, base_name='TestAnswers')
urlpatterns = router.urls
