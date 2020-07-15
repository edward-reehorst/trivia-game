import requests
import json
import html
import random


class TriviaGame:

    def __init__(self, categories=None):
        self.length=int(input('How many questions would you like to play?\t'))
        self.num_team=int(input('How many teams are playing?\t'))
        self.categories = categories
        self.score = [0 for p in range(self.num_team)]
        self.team_names = []
        for t in range(self.num_team):
            self.team_names.append(input('What is the name for team {}?\t'.format(t+1)))
        assert len(self.team_names) == self.num_team

    def run_game(self):
        for i in range(self.length):
            # get question
            category = random.choice(self.categories)
            q = Question(category=category)
            # show pre question info
            input(q.get_pre_q())
            input(q.get_question())
            input(q.get_ans())
            for t in range(self.num_team):
                correct = input('Was {} correct? (y or n)\t'.format(self.team_names[t]))
                if correct == 'y':
                    self.score[t] += 1

            self.print_scores()
            input()


    def print_scores(self):
        for t in range(self.num_team):
            print('{}: {} pts'.format(self.team_names[t],self.score[t]))





class Question:
    def __init__(self, **kwargs):
        if 'q_dict' in kwargs:
            self.from_dict(kwargs['q_dict'])
        else:
            self.from_web(**kwargs)

    def from_web(self, **kwargs):
        print(kwargs)
        # TODO process url
        url = 'https://opentdb.com/api.php?amount=1'
        for k in kwargs:
            url = url + '&' + k + '=' + str(kwargs[k])
        # TODO handle requests errors
        r = requests.get(url)
        # check response
        response_code = json.loads(r.text)['response_code']
        if response_code != 0:
            # TODO raise error
            pass
        # get dictionary
        q_dict = json.loads(r.text)["results"][0]
        self.from_dict(q_dict)

    def from_dict(self, q_dict):
        self.cat = q_dict['category']
        self.type = q_dict['type']
        self.difficulty = q_dict['difficulty']
        self.q = q_dict['question']
        self.ans = q_dict['correct_answer']
        self.wrong_ans = q_dict['incorrect_answers']

    def get_pre_q(self):
        return 'Difficulty: {}\nCategory: {}'.format(self.difficulty, self.cat)

    def get_question(self, possible_ans=True):
        str = self.q
        if possible_ans:
            # TODO add possible answers to string
            pos_ans = self.wrong_ans + [self.ans]
            random.shuffle(pos_ans)
            print(pos_ans)
            for i, ans in enumerate(pos_ans):
                str += '\n{}: {}'.format(i, ans)

        return str


    def get_ans(self):
        return 'Answer: {}'.format(self.ans)

# Categories
# 9: general knowledge, 10: books, 11: film, 12: music, 13: theatre, 14: TV
# 15 is video games, 16 is board games, 17 is science, 18 is computers
# 19: math, 20: Mythology, 21: sports, 22: geography, 23: history, 24: politics
# 25: art, 26: celebrities, 27: animals, 28: vehicles, 29: comics, 30: gadgets,
# 31: anime, 32: cartoons
cats = [9, 10, 11, 12, 13, 14, 17, 21, 22, 23, 24, 25, 26, 27, 28, 32]
game = TriviaGame(categories=cats)
game.run_game()
