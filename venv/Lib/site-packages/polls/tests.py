from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionTestCase(TestCase):
    def setUp(self):
        now = timezone.now().date()
        Question.objects.create(
            question_text="Une question de test ?", publish_date=now)
        self.question = Question.objects.get(
            question_text="Une question de test ?")

    def tearDown(self):
        del self.question

    def test_question_published_recently(self):
        self.assertTrue(self.question.was_published_recently())

    def test_question_published_three_day_ago(self):
        self.question.publish_date = self.question.publish_date \
            - timedelta(days=3)
        self.assertFalse(self.question.was_published_recently())

    def test_question_publish_in_the_future(self):
        self.question.publish_date = self.question.publish_date \
            + timedelta(days=2)
        self.assertFalse(self.question.was_published_recently())


#  Work in progress
''' class ResultViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        now = timezone.now().date()
        Question.objects.create(
            question_text="Une question de test ?", publish_date=now)
        self.question = Question.objects.get(
            question_text="Une question de test ?")
        self.question.reponse_set.create(
            reponse_text='reponse test', nb_vote=1)

    def tearDown(self):
        del self.question
        del self.client

    def test_vote(self):
        response = self.client.get(
            reverse(('vote'), kwargs={'question_id':  self.question.id}))
        self.assertEqual(response.status_code, 302) '''
