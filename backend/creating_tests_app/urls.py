from rest_framework.routers import DefaultRouter

from creating_tests_app.views import TestsModelViewSet, QuestionReadOnlyModelViewSet, OpenQuestionCreateViewSet, \
    BooleanQuestionCreateViewSet, ChoiceOneQuestionCreateViewSet, ChoiceMultiQuestionCreateViewSet, \
    ScaleQuestionCreateViewSet, AnswerCreateRetrieveUpdateDestroyViewSet

app_name = 'tests_urls'

router = DefaultRouter()

router.register('tests',
                TestsModelViewSet,
                base_name='Tests')
router.register('tests/(?P<test_id>[^/.]+)/questions',
                QuestionReadOnlyModelViewSet,
                base_name='Questions')
router.register('tests/(?P<test_id>[^/.]+)/questions/open',
                OpenQuestionCreateViewSet,
                base_name='OpenQuestion')
router.register('tests/(?P<test_id>[^/.]+)/questions/choice_one',
                ChoiceOneQuestionCreateViewSet,
                base_name='ChoiceOneQuestion')
router.register('tests/(?P<test_id>[^/.]+)/questions/choice_multi',
                ChoiceMultiQuestionCreateViewSet,
                base_name='ChoiceMultiQuestion')
router.register('tests/(?P<test_id>[^/.]+)/questions/boolean',
                BooleanQuestionCreateViewSet,
                base_name='BooleanQuestion')
router.register('tests/(?P<test_id>[^/.]+)/questions/scale',
                ScaleQuestionCreateViewSet,
                base_name='ScaleQuestion')
router.register('tests/(?P<test_id>[^/.]+)/questions/?P<question_id>[^/.]+/answer',
                AnswerCreateRetrieveUpdateDestroyViewSet,
                base_name='Answer')
urlpatterns = router.urls
