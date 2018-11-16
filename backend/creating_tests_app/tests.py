from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from creating_tests_app.models import Test, QuestionBase, OpenQuestion


class EndpointsAccessAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User(username='testuser', email='test@test.com')
        cls.user.set_password("randompassword")
        cls.user.save()
        cls.user2 = User(username='testuser2', email='test2@test.com')
        cls.user2.set_password("randompassword2")
        cls.user2.save()
        cls.my_admin = User.objects.create_superuser(
            'superuser', 'test@test.com', 'randompassword')
        cls.test = Test(user=cls.user, name="test1", description="description")
        cls.test.save()
        cls.question_open = OpenQuestion(
            question_content="question", test=cls.test, number=1, question_type=QuestionBase.OPEN)
        cls.question_open.save()
        cls.test_data = {"name": "some_name", "description": "description2"}
        cls.empty_data = {}
        cls.delete_data = {'id': 1}
        cls.url_tests_list = reverse("tests:tests-list")
        cls.url_tests_details = reverse("tests:tests-detail", kwargs={'pk': cls.test.pk})
        cls.url_questions_list = reverse("tests:questions-list", kwargs={'test_id': cls.test.pk})
        cls.url_questions_detail = reverse(
            "tests:questions-detail", kwargs={'test_id': cls.test.pk, 'pk': cls.question_open.pk})
        cls.url_answer = reverse(
            "tests:answer-list", kwargs={'test_id': cls.test.pk, 'question_id': cls.question_open.pk})

    def setUp(self):
        super().setUp()

    def check_method(self, method, url, data, status_code):
        response = method(url, data=data)
        self.assertEqual(response.status_code, status_code)
        self.tearDown()
        self.setUp()

    def check_authenticated_method(self, method, url, data, status_code):
        self.client.force_login(self.user2)
        self.check_method(method, url, data, status_code)

    def check_author_authenticated_method(self, method, url, data, status_code):
        self.client.force_login(self.user)
        self.check_method(method, url, data, status_code)

    def check_admin_authenticated_method(self, method, url, data, status_code):
        self.client.force_login(self.my_admin)
        self.check_method(method, url, data, status_code)

    def check_all_credentials(self,
                              method,
                              url,
                              data,
                              not_authenticated_status_code,
                              authenticated_status_code,
                              author_authenticated_status_code,
                              admin_authenticated_status_code):
        self.check_method(method, url, data, not_authenticated_status_code)
        self.check_authenticated_method(method, url, data, authenticated_status_code)
        self.check_author_authenticated_method(method, url, data, author_authenticated_status_code)
        self.check_admin_authenticated_method(method, url, data, admin_authenticated_status_code)

    def test_test_list(self):
        self.check_all_credentials(self.client.get, self.url_tests_list, self.empty_data, status.HTTP_200_OK,
                                   status.HTTP_200_OK, status.HTTP_200_OK, status.HTTP_200_OK)

    def test_test_post(self):
        self.check_all_credentials(self.client.post, self.url_tests_list, self.test_data, status.HTTP_403_FORBIDDEN,
                                   status.HTTP_201_CREATED, status.HTTP_201_CREATED, status.HTTP_201_CREATED)

    def test_test_get(self):
        self.check_all_credentials(self.client.get,
                                   self.url_tests_details,
                                   self.empty_data,
                                   status.HTTP_200_OK,
                                   status.HTTP_200_OK,
                                   status.HTTP_200_OK,
                                   status.HTTP_200_OK)

    def test_test_delete(self):
        self.check_all_credentials(self.client.delete,
                                   self.url_tests_details,
                                   self.delete_data,
                                   status.HTTP_403_FORBIDDEN,
                                   status.HTTP_403_FORBIDDEN,
                                   status.HTTP_204_NO_CONTENT,
                                   status.HTTP_204_NO_CONTENT)

    def test_test_put(self):
        self.check_all_credentials(self.client.put, self.url_tests_details, self.test_data, status.HTTP_403_FORBIDDEN,
                                   status.HTTP_403_FORBIDDEN, status.HTTP_200_OK, status.HTTP_200_OK)
