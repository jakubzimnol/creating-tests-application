from rest_framework.routers import DefaultRouter

from creating_tests_app.views import TestsModelViewSet, QuestionReadOnlyModelViewSet, OpenQuestionCreateViewSet, \
    BooleanQuestionCreateViewSet, ChoiceOneQuestionCreateViewSet, ChoiceMultiQuestionCreateViewSet, \
    ScaleQuestionCreateViewSet, AnswerModelViewSet

app_name = 'tests_urls'

router = DefaultRouter()

router.register('tests',
                TestsModelViewSet,
                base_name='tests')
router.register('tests/(?P<test_id>[^/.]+)/questions/open',
                OpenQuestionCreateViewSet,
                base_name='open_question')
router.register('tests/(?P<test_id>[^/.]+)/questions/choice_one',
                ChoiceOneQuestionCreateViewSet,
                base_name='choice_one_question')
router.register('tests/(?P<test_id>[^/.]+)/questions/choice_multi',
                ChoiceMultiQuestionCreateViewSet,
                base_name='choice_multi_question')
router.register('tests/(?P<test_id>[^/.]+)/questions/boolean',
                BooleanQuestionCreateViewSet,
                base_name='boolean_question')
router.register('tests/(?P<test_id>[^/.]+)/questions/scale',
                ScaleQuestionCreateViewSet,
                base_name='scale_question')
router.register('tests/(?P<test_id>[^/.]+)/questions',
                QuestionReadOnlyModelViewSet,
                base_name='questions')
router.register('tests/(?P<test_id>[^/.]+)/questions/(?P<question_id>[^/.]+)/answer',
                AnswerModelViewSet,
                base_name='answer')
urlpatterns = router.urls
