from rest_framework.routers import DefaultRouter

from creating_tests_app.views import TestsModelViewSet, QuestionModelViewSet

app_name = 'tests_urls'

router = DefaultRouter()

router.register('tests', TestsModelViewSet, base_name='Tests')
router.register('questions', QuestionModelViewSet, base_name='Questions')
urlpatterns = router.urls
