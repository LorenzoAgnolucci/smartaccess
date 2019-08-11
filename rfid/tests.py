from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import RFIDCard, Log
import datetime
from . import views


def create_card(id, num_acc, exp_days):
    time = timezone.now() + timezone.timedelta(days=exp_days)
    return RFIDCard.objects.create(card_id=id, remaining_accesses=num_acc, expiration_date=time)


## Model test samples
# class QuestionModelTests(TestCase):
#
#     def test_is_recent_with_future_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is in the future.
#         """
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_question = Question(pub_date=time)
#         self.assertIs(future_question.is_recent(), False)
#
#     def test_is_recent_with_old_question(self):
#         time = timezone.now() - datetime.timedelta(days=2)
#         old_question = Question(pub_date=time)
#         self.assertFalse(old_question.is_recent())
#
#     def test_is_recent_with_recent_question(self):
#         time = timezone.now() - datetime.timedelta(hours=4)
#         recent_question = Question(pub_date=time)
#         self.assertTrue(recent_question.is_recent())
#
#     def test_no_questions(self):
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'No polls are available')
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
#
#     def test_past_question(self):
#         create_question('Past question', -2)
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])
#
#     def test_future_question(self):
#         create_question('Future question', 2)
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'No polls are available')
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
#
#     def test_two_past_questions(self):
#         create_question(question_text="Past question 1.", days=-30)
#         create_question(question_text="Past question 2.", days=-5)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question 2.>', '<Question: Past question 1.>']
#         )


class AccessViewTests(TestCase):

    def test_expired_card(self):
        """
        The access result page returns a page saying that the card is expired, when and
        with how many remaining accesses
        """
        expired_card = create_card(5279589593186, 5, -5)
        message = 'Card expired'
        url = reverse('rfid:access_result')+str(expired_card.card_id)+'/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, message)
        self.assertContains(response, 'last {} accesses expired on {}'.format(expired_card.remaining_accesses,
                                                                              timezone.now().date()+datetime.timedelta(days=-5)))

    def test_empty_card(self):
        """
        The access result page returns a page saying that there are no mor accesses available
        """
        days = 5
        empty_card = create_card(5279589593186, 0, days)
        message = 'No accesses'
        url = reverse('rfid:access_result')+str(empty_card.card_id)+'/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, message)

    def test_unregistered_card(self):
        """
        The access result page returns a page saying that the card is not registered
        """
        message = 'Card not registered'
        url = reverse('rfid:access_result')+str(5279589593186)+'/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, message)

    def test_valid_card(self):
        """
        The access result page returns a welcome page with the number of the accesses remained and the expiration date
        """
        # create a database with a valid card
        valid_card = create_card(5279589593186, 10, 5)
        message = 'Welcome'
        url = reverse('rfid:access_result')+str(valid_card.card_id)+'/'
        response = self.client.get(url)
        log = Log.objects.filter(card=valid_card.card_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(log), 1)
        updated_card = RFIDCard.objects.get(pk=valid_card.card_id)
        self.assertEqual(updated_card.remaining_accesses, 9)
        self.assertContains(response, message)
        self.assertContains(response, 'You have 9 accesses left. '
                                      'The card will expire on {}'.format(timezone.now().date()+datetime.timedelta(days=5)))
