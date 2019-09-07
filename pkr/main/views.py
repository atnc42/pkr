from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from main.utils import Checker, Card


class SayMyName(APIView):

    def post(self, *args, **kwargs):
        data = self.request.data
        hands = list()
        for hand_number in range(1, 5):
            if data.get(f'combination{hand_number}'):
                combinations = data.get(f'combination{hand_number}')
                cards = [
                    Card(card[0], card[1]) if len(card) == 2 else Card(card[:2], card[2:])
                    for card in combinations.split(',')
                ]
                hands.append(cards)
        checker = Checker(hands)
        hand_nubmer, combination, score = checker.check_combinations()
        return Response({'name': combination,
                         'score': score,
                         'hand_number': hand_nubmer
                         })

