from django.urls import reverse

from rest_framework.test import APITestCase


class PokerTest(APITestCase):

    def test_combination(self):
        response = self.client.post(
            reverse('main:say_my_name'),
            data={
                'combination1': '9C,3D,5S,10H,JC',
                'combination2': '10C,10D,10S,10H,JC',
            }
        )
        self.assertEqual(2, response.data.get('hand_number'))

        response = self.client.post(
            reverse('main:say_my_name'),
            data={
                'combination1': '9C,3D,5S,10H,JC',
                'combination2': '10C,10D,10S,10H,JC',
                'combination3': 'AC,KC,10C,QC,JC',
            }
        )
        self.assertEqual(3, response.data.get('hand_number'))

