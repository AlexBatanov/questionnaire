import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

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

    def test_published_recently_with_old_question(self):
        """
        was_published_recently() возвращвет False если дата
        старше одного дня.
        """

        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        question = Question(pub_date=time)

        self.assertEqual(question.was_published_recently(), False)

    def test_published_recently_with_recent_question(self):
        """
        was_published_recently() возвращает True если дата
        находится в течении последних суток
        """

        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Создает вопрос с заданным `question_text` и с
    заданным количеством «дней» со смещением по настоящее время.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """ Если вопросов нет, отображается соответствующее сообщение. """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Вопросы с датой публикации в прошлом отображаются на
        индексная страница.
        """
        question = create_question(question_text='text', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Вопросы с pub_date в будущем не отображаются на
        индексной странице.
        """
        question = create_question(question_text='text', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Даже если существуют и прошлые, и будущие вопросы, только прошлые вопросы
        отображаются.
        """
        question = create_question(question_text='text', days=-30)
        create_question(question_text='text', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_question(self):
        """ На индексной странице может отображаться несколько вопросов. """
        question1 = create_question(question_text='text', days=-20)
        question2 = create_question(question_text='text', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question1, question2]
        )

class QuestionDetailTests(TestCase):
    def test_future_deatil_question(self):
        question = create_question(question_text='text', days=30)
        response = self.client.get(reverse('polls:detail', args=(question.pk,)))
        self.assertEqual(response.status_code, 404)