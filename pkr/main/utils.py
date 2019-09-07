

class Card:

    ALPHA_TO_NUMBER = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 11
    }

    def __init__(self, rank, suit):
        self.rank = int(self.ALPHA_TO_NUMBER.get(rank, rank))
        self.suit = suit

    def __ge__(self, other):
        return self.rank >= other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __ne__(self, other):
        return self.rank > other.rank

    def __eq__(self, other):
        return self.rank is other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __lt__(self, other):
        return self.rank < other.rank


class CheckerResult:

    def __init__(self, hand, name_of_cards, score):
        self.hand = hand
        self.name_of_cards = name_of_cards
        self.score = score

    def __ge__(self, other):
        return self.score >= other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ne__(self, other):
        return self.score > other.score

    def __eq__(self, other):
        return self.score is other.score

    def __le__(self, other):
        return self.score <= other.score

    def __lt__(self, other):
        return self.score < other.score


class Checker:

    def __init__(self, hands):
        self.hands = hands
        self.hands_result = list()

    def score(self, cards):
        score = sum([card.rank for card in cards])
        return score

    def is_royal(self, cards):
        """
       ['AS', 'KS', 'QS', 'JS', '10S', ]
        """
        name_of_hand = 'Royal flush'
        found = True
        sorted_cards = sorted(cards, reverse=True)

        expected_suit = sorted_cards[0].suit

        expected_max_rank = 14  # A - max rank

        for card in sorted_cards:
            if card.rank != expected_max_rank or card.suit != expected_suit:
                found = False
                break
            else:
                expected_max_rank -= 1

        if found:
            return name_of_hand, self.score(cards)
        # go to the next hand
        return self.is_straight_flush(sorted_cards)

    def is_straight_flush(self, cards):
        """

        ['10S', '9S', '8S', '7S', '6S']
        """
        name_of_hand = 'Straight flush'
        found = True
        expected_suit = cards[0].suit
        expected_max_rank = cards[0].rank
        for card in cards:
            if card.rank != expected_max_rank or card.suit != expected_suit:
                found = False
                break
            else:
                expected_max_rank -= 1

        if found:
            return name_of_hand, self.score(cards)
        # go to the next hand
        return self.is_four(cards)

    def is_four(self, cards):
        """

        ['10S', '10D', '10H', '10C', 'AS']

        """
        name_of_hand = 'Four'

        expected_rank = cards[1].rank
        cards_rank = [card.rank for card in cards]

        if cards_rank.count(expected_rank) == 4:
            return name_of_hand, self.score(cards)

        return self.is_full_house(cards)

    def is_full_house(self, cards):
        """

        ['10S', '10D', '10H', 'AC', 'AS']

        """
        name_of_hand = 'Full house'

        cards_rank = [card.rank for card in cards]

        first_combinations_rank = cards_rank[0]
        second_combinations_rank = cards_rank[-1]

        first_combinations_rank_count = cards_rank.count(first_combinations_rank)
        second_combinations_rank_count = cards_rank.count(second_combinations_rank)

        if (first_combinations_rank_count == 2 and second_combinations_rank_count == 3) or (
                second_combinations_rank_count == 2 and first_combinations_rank_count == 3
        ):
            return name_of_hand, self.score(cards)

        return self.is_flush(cards)

    def is_flush(self, cards):
        """

       ['10S', 'JS', 'QS', 'KS', 'AS']


        """
        name_of_hand = 'Flush'

        cards_suite = set([card.suit for card in cards])

        if len(cards_suite) == 1:
            return name_of_hand, self.score(cards)

        return self.is_straight(cards)

    def is_straight(self, cards):
        """

        ['10S', '9D', '8S', '7H', '6C']

        """
        name_of_hand = 'Straight'

        expected_max_rank = cards[0].rank
        found = True

        for card in cards:
            if card.rank != expected_max_rank:
                found = False

        if found:
            return name_of_hand, self.score(cards)

        return self.is_three_of_kind(cards)

    def is_three_of_kind(self, cards):
        """

        ['10S', '10D', '8S', '7H', '10C']

        """

        name_of_hand = 'Three of a kind'

        cards_rank = [card.rank for card in cards]

        expexted_rank = cards_rank[2]
        if cards_rank.count(expexted_rank) == 3:
            return name_of_hand, self.score(cards)

        return self.is_two_pairs(cards)

    def is_two_pairs(self, cards):
        """

        ['10S', '10D', '8S', '8H', '6C']

        """
        name_of_hand = 'Pairs'
        # 2 and 4 have identical rank
        cards_rank = [card.rank for card in cards]

        first_pair = cards_rank[1]
        second_pair = cards_rank[3]

        if cards_rank.count(first_pair) == 2 and cards_rank.count(second_pair) == 2:
            return name_of_hand, self.score(cards)

        return self.is_pair(cards)

    def is_pair(self, cards):
        """

        ['10S', '10D', '8S', '7H', '6C']

        """
        name_of_hand = 'Pair'
        cards_rank = [card.rank for card in cards]
        counts_card_rank = set([cards_rank.count(card_rank) for card_rank in cards_rank])
        score = self.score(cards)
        if 2 in counts_card_rank:
            return name_of_hand, score
        return 'High card', score

    def check_combinations(self):
        # start from higher combination
        for num, hand in enumerate(self.hands, 1):
            result = self.is_royal(hand)
            self.hands_result.append(CheckerResult(
                num,
                *result
            ))
        max_combination = max(self.hands_result)
        return max_combination.hand, max_combination.name_of_cards, max_combination.score
