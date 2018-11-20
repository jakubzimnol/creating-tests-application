from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from creating_tests_app.models import QuestionBase, Test, AnswerBase
from creating_tests_app.test_fixture import TestFactory, OpenQuestionFactory, OpenAnswerFactory, ScaleQuestionFactory, \
    ChoiceOneQuestionFactory, ChoiceFactory, ChoiceMultiQuestionFactory, BooleanQuestionFactory


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
        cls.url_tests_list = reverse("tests:tests-list")
        cls.test_data = {"name": "some_name", "description": "description2"}
        cls.empty_data = {}

    def tearDown(self):
        Test.objects.all().delete()
        QuestionBase.objects.all().delete()
        AnswerBase.objects.all().delete()

    def setUp(self):
        super().setUp()

    def check_method(self, method, url, data, status_code):
        response = method(url, data=data)
        self.assertEqual(response.status_code, status_code)

    def check_authenticated_method(self, method, url, data, status_code):
        self.client.force_login(self.user2)
        self.check_method(method, url, data, status_code)

    def check_author_authenticated_method(self, method, url, data, status_code):
        self.client.force_login(self.user)
        self.check_method(method, url, data, status_code)

    def check_admin_authenticated_method(self, method, url, data, status_code):
        self.client.force_login(self.my_admin)
        self.check_method(method, url, data, status_code)


class TestApiTestCase(EndpointsAccessAPITestCase):
    def setUp(self):
        self.test = TestFactory(user=self.user)
        self.test.save()
        self.delete_test_data = {'id': self.test.id}
        self.url_tests_details = reverse("tests:tests-detail", kwargs={'pk': self.test.id})
        super().setUp()

    def tearDown(self):
        Test.objects.all().delete()

    def test_tests_list(self):
        self.check_method(self.client.get, self.url_tests_list,
                          self.empty_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.get, self.url_tests_list,
                                        self.empty_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.get, self.url_tests_list,
                                               self.empty_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.get, self.url_tests_list,
                                              self.empty_data, status.HTTP_200_OK)

    def test_tests_post(self):
        self.check_method(self.client.post, self.url_tests_list,
                          self.test_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.post, self.url_tests_list,
                                        self.test_data, status.HTTP_201_CREATED)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.post, self.url_tests_list,
                                               self.test_data, status.HTTP_201_CREATED)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.post, self.url_tests_list,
                                              self.test_data, status.HTTP_201_CREATED)

    def test_tests_get(self):
        self.check_method(self.client.get, self.url_tests_details,
                          self.empty_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.get, self.url_tests_details,
                                        self.empty_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.get, self.url_tests_details,
                                               self.empty_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.get, self.url_tests_details,
                                              self.empty_data, status.HTTP_200_OK)

    def test_tests_delete(self):
        self.check_method(self.client.delete, self.url_tests_details,
                          self.delete_test_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.delete, self.url_tests_details,
                                        self.delete_test_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.delete, self.url_tests_details,
                                               self.delete_test_data, status.HTTP_204_NO_CONTENT)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.delete, self.url_tests_details,
                                              self.delete_test_data, status.HTTP_204_NO_CONTENT)

    def test_tests_put(self):
        self.check_method(self.client.put, self.url_tests_details,
                          self.test_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.put, self.url_tests_details,
                                        self.test_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.put, self.url_tests_details,
                                               self.test_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.put, self.url_tests_details,
                                              self.test_data, status.HTTP_200_OK)


class QuestionTestCase(EndpointsAccessAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super(QuestionTestCase, cls).setUpTestData()
        cls.test = TestFactory(user=cls.user)
        cls.test.save()

    def setUp(self):
        self.question = OpenQuestionFactory(test=self.test)
        self.question.save()
        self.choice_one_question = OpenQuestionFactory(test=self.test)
        self.choice_one_question.save()
        self.open_answer = OpenAnswerFactory(question=self.question)
        self.open_answer.save()
        self.open_question_data = {"question_content": "some_name", "answer": self.open_answer.id,
                                   "test": self.test.id, "number": 1}
        self.delete_question_data = {'id': self.question.id}
        self.url_questions_list = reverse("tests:questions-list", kwargs={'test_id': self.test.id})
        self.url_questions_details = reverse(
            "tests:questions-detail", kwargs={'test_id': self.test.id, 'pk': self.question.id})
        super().setUp()

    def tearDown(self):
        QuestionBase.objects.all().delete()
        AnswerBase.objects.all().delete()


class EndpointsQuestionTestCase(QuestionTestCase):
    def test_questions_list(self):
        self.check_method(self.client.get, self.url_questions_list,
                          self.empty_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.get, self.url_questions_list,
                                        self.empty_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.get, self.url_questions_list,
                                               self.empty_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.get, self.url_questions_list,
                                              self.empty_data, status.HTTP_200_OK)

    def test_questions_get(self):
        self.check_method(self.client.get, self.url_questions_details,
                          self.empty_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.get, self.url_questions_details,
                                        self.empty_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.get, self.url_questions_details,
                                               self.empty_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.get, self.url_questions_details,
                                              self.empty_data, status.HTTP_200_OK)

    def test_questions_delete(self):
        self.check_method(self.client.delete, self.url_questions_details,
                          self.delete_question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.delete, self.url_questions_details,
                                        self.delete_question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.delete, self.url_questions_details,
                                               self.delete_question_data, status.HTTP_204_NO_CONTENT)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.delete, self.url_questions_details,
                                              self.delete_question_data, status.HTTP_204_NO_CONTENT)

    def test_questions_put(self):
        self.check_method(self.client.put, self.url_questions_details,
                          self.open_question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.put, self.url_questions_details,
                                        self.open_question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.put, self.url_questions_details,
                                               self.open_question_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.put, self.url_questions_details,
                                              self.open_question_data, status.HTTP_200_OK)


class OpenQuestionTest(QuestionTestCase):
    def setUp(self):
        self.open_question = OpenQuestionFactory(test=self.test)
        self.open_question.save()
        self.open_question_data = {"question_content": "some_name", "test": self.test.id, "number": 1}
        self.url_question_open = reverse("tests:open_question-list", kwargs={'test_id': self.test.id})
        super().setUp()

    def test_open_question_post(self):
        self.check_method(self.client.post, self.url_question_open,
                          self.open_question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.post, self.url_question_open,
                                        self.open_question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.post, self.url_question_open,
                                               self.open_question_data, status.HTTP_201_CREATED)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.post, self.url_question_open,
                                              self.open_question_data, status.HTTP_403_FORBIDDEN)


class ChoiceOneTest(QuestionTestCase):
    def check_method(self, method, url, data, status_code):
        response = method(url, data=data, format='json')
        self.assertEqual(response.status_code, status_code)

    def setUp(self):
        self.choice_one_question = ChoiceOneQuestionFactory(test=self.test)
        self.choice_one_question.save()
        self.choice = ChoiceFactory(question_options=self.choice_one_question)
        self.choice_one_question_data = {"question_content": "some_name",
                                         "test": self.test.id,
                                         "number": 1,
                                         "options": [{"name": self.choice.name}, ],
                                         "proper_answer": [{"name": self.choice.name}, ],
                                         }
        self.url_question_choice_one = reverse("tests:choice_one_question-list", kwargs={'test_id': self.test.id})
        super().setUp()

    def test_choice_one_question_post(self):
        self.check_method(self.client.post, self.url_question_choice_one,
                          self.choice_one_question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.post, self.url_question_choice_one,
                                        self.choice_one_question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.post, self.url_question_choice_one,
                                               self.choice_one_question_data, status.HTTP_201_CREATED)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.post, self.url_question_choice_one,
                                              self.choice_one_question_data, status.HTTP_403_FORBIDDEN)


class ChoiceMultiQuestionTest(QuestionTestCase):
    def check_method(self, method, url, data, status_code):
        response = method(url, data=data, format='json')
        self.assertEqual(response.status_code, status_code)

    def setUp(self):
        self.choice_multi_question = ChoiceMultiQuestionFactory(test=self.test)
        self.choice_multi_question.save()
        self.choice = ChoiceFactory(question_options=self.choice_multi_question)
        self.question_data = {"question_content": "some_name",
                              "test": self.test.id,
                              "number": 1,
                              "options": [{"name": self.choice.name}, {"name": self.choice.name}],
                              "proper_answer": [{"name": self.choice.name}, {"name": self.choice.name}],
                              }
        self.url_question = reverse("tests:choice_multi_question-list", kwargs={'test_id': self.test.id})
        super().setUp()

    def test_choice_multi_question_post(self):
        self.check_method(self.client.post, self.url_question,
                          self.question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.post, self.url_question,
                                        self.question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.post, self.url_question,
                                               self.question_data, status.HTTP_201_CREATED)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.post, self.url_question,
                                              self.question_data, status.HTTP_403_FORBIDDEN)


class ScaleQuestionTest(QuestionTestCase):
    def setUp(self):
        self.scale_question = ScaleQuestionFactory(test=self.test)
        self.scale_question.save()
        self.question_data = {"question_content": "some_name",
                              "test": self.test.id, "number": 1, "proper_answer": 1}
        self.url_question = reverse("tests:scale_question-list", kwargs={'test_id': self.test.id})
        super().setUp()

    def test_scale_question_post(self):
        self.check_method(self.client.post, self.url_question,
                          self.question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.post, self.url_question,
                                        self.question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.post, self.url_question,
                                               self.question_data, status.HTTP_201_CREATED)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.post, self.url_question,
                                              self.question_data, status.HTTP_403_FORBIDDEN)


class BooleanQuestionTest(QuestionTestCase):
    def setUp(self):
        self.boolean_question = BooleanQuestionFactory(test=self.test)
        self.boolean_question.save()
        self.question_data = {"question_content": "some_name", "test": self.test.id,
                              "number": 1, "proper_answer": False}
        self.url_question = reverse("tests:boolean_question-list", kwargs={'test_id': self.test.id})
        super().setUp()

    def test_boolean_question_post(self):
        self.check_method(self.client.post, self.url_question,
                          self.question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.post, self.url_question,
                                        self.question_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.post, self.url_question,
                                               self.question_data, status.HTTP_201_CREATED)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.post, self.url_question,
                                              self.question_data, status.HTTP_403_FORBIDDEN)


class AnswerTestCase(QuestionTestCase):
    @classmethod
    def setUpTestData(cls):
        super(AnswerTestCase, cls).setUpTestData()
        cls.test = TestFactory(user=cls.user)
        cls.test.save()

    def tearDown(self):
        AnswerBase.objects.all().delete()


class OpenAnswerTestCase(AnswerTestCase):
    @classmethod
    def setUpTestData(cls):
        super(OpenAnswerTestCase, cls).setUpTestData()
        cls.question = OpenQuestionFactory(test=cls.test)
        cls.question.save()
        cls.url_answer = reverse("tests:answer-list",
                                 kwargs={'test_id': cls.test.id,
                                         "question_id": cls.question.id})
        cls.answer_data = {"answer": "a"}

    def setUp(self):
        self.open_answer = OpenAnswerFactory(question=self.question)
        self.open_answer.save()

    def test_open_answer_post(self):
        self.check_method(self.client.post, self.url_answer,
                          self.answer_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.check_authenticated_method(self.client.post, self.url_answer,
                                        self.answer_data, status.HTTP_201_CREATED)
        self.tearDown()
        self.check_author_authenticated_method(self.client.post, self.url_answer,
                                               self.answer_data, status.HTTP_201_CREATED)
        self.tearDown()
        self.check_admin_authenticated_method(self.client.post, self.url_answer,
                                              self.answer_data, status.HTTP_201_CREATED)

    def test_open_answer_get(self):
        self.check_method(self.client.get, self.url_answer,
                          self.empty_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.get, self.url_answer,
                                        self.empty_data, status.HTTP_404_NOT_FOUND)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.get, self.url_answer,
                                               self.empty_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.get, self.url_answer,
                                              self.empty_data, status.HTTP_404_NOT_FOUND)

    def test_open_answer_put(self):
        self.check_method(self.client.put, self.url_answer,
                          self.answer_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.put, self.url_answer,
                                        self.answer_data, status.HTTP_404_NOT_FOUND)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.put, self.url_answer,
                                               self.answer_data, status.HTTP_200_OK)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.put, self.url_answer,
                                              self.answer_data, status.HTTP_404_NOT_FOUND)

    def test_open_answer_delete(self):
        self.check_method(self.client.delete, self.url_answer,
                          self.answer_data, status.HTTP_403_FORBIDDEN)
        self.tearDown()
        self.setUp()
        self.check_authenticated_method(self.client.delete, self.url_answer,
                                        self.answer_data, status.HTTP_404_NOT_FOUND)
        self.tearDown()
        self.setUp()
        self.check_author_authenticated_method(self.client.delete, self.url_answer,
                                               self.answer_data, status.HTTP_404_NOT_FOUND)
        self.tearDown()
        self.setUp()
        self.check_admin_authenticated_method(self.client.delete, self.url_answer,
                                              self.answer_data, status.HTTP_404_NOT_FOUND)

