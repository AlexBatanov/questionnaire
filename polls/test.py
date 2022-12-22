import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() возвращвет False если дата
        больше текущей.
        """

        time = timezone.now() + datetime.timedelta(days=30)
        question = Question(pub_date=time)

        self.assertEqual(question.was_published_recently(), False)
