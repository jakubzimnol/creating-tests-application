from rest_framework.routers import DefaultRouter

from creating_tests_app.views import TestsModelViewSet, QuestionReadOnlyModelViewSet, OpenQuestionViewSet, \
    BoolQuestionViewSet, ChoiceOneQuestionViewSet, ChoiceMultiQuestionViewSet, ScaleQuestionViewSet

app_name = 'tests_urls'

router = DefaultRouter()

router.register('tests', TestsModelViewSet, base_name='Tests')
router.register('questions/open', OpenQuestionViewSet, base_name='OpenQuestion')
router.register('questions/choice_one', ChoiceOneQuestionViewSet, base_name='ChoiceOneQuestion')
router.register('questions/choice_multi', ChoiceMultiQuestionViewSet, base_name='ChoiceMultiQuestion')
router.register('questions/boolean', BoolQuestionViewSet, base_name='BooleanQuestion')
router.register('questions/scale', ScaleQuestionViewSet, base_name='ScaleQuestion')
router.register('questions', QuestionReadOnlyModelViewSet, base_name='Questions')
urlpatterns = router.urls
