import os
import random
import re
import threading
import time

import utils
from command import SuperCommand
from consts import Cmd

HIDDEN_CHAR = "-"

# JSON field names
QUIZ = "quiz"
QUESTIONS = "total_questions"
ANSWERED = "total_answered"
LAST_ANSWERED = "last_answered"
USERS = "users"
USER_COMBO = "combo"
POINTS = "points"


class QuizCmd(SuperCommand):
    """Module responsible for all quiz related things"""

    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        self._accept_answers = False
        self._current_combo = []
        self._timer = None
        self._timeout_set = False
        self._question = None
        self._answer = None
        self._hidden = ""
        self._hidden_count = 0

        with open(os.path.dirname(os.path.realpath(__file__)) + "/klausimai.txt", "r") as infile:
            self._lines = infile.readlines()
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        if args is None:
            args = self.config[Cmd.ARGS]["help"]

        # Checks if it is a command
        for key, val in self.config[Cmd.ARGS].items():
            if val == args:
                if key == "help":
                    self.sendMessage(self.config["help"])

                elif key == "repeat_question":
                    if self._timeout_set:
                        self.sendMessage("{0}\n\n{1}".format(self.getQuestion(), self._hidden))
                    else:
                        self.giveQuestion()

                elif key == "get_question":
                    self.giveQuestion()

                elif key == "user_stats":
                    stats = self.getUserStats(self._bot.fbidToName(author_id))
                    if stats:
                        msg = self.config["user_stats_text"].format(name=self._bot.fbidToName(author_id), **stats)
                    else:
                        msg = self.config["user_not_played"]
                    self.sendMessage(msg)

                elif key == "global_stats":
                    stats = self._bot.config[QUIZ]
                    msg = self.config["global_stats_text"].format(**stats)
                    self.sendMessage(msg)

                elif key == "top_3":
                    users = self.getTop(3)

                    msg = self.config["top_text"]
                    for i, user in enumerate(users):
                        msg += self.config["top_position_text"].format(str(i + 1), user[0], user[1][POINTS])
                    self.sendMessage(msg)

                break
        # Command not found, it is a guess
        else:
            self.tryGuess(author_id, " ".join(args))

    def doesAcceptAnswers(self):
        return self._accept_answers

    def getQuestion(self):
        if not self._accept_answers:
            return self.getNewQuestion()
        return self._question

    def getAnswer(self):
        return self._answer

    def getUserStats(self, author_id):
        return self._bot.stats[QUIZ][USERS].get(author_id)

    def getNewQuestion(self):
        """Generates and returns new question"""
        self.updateQuizQuestions()
        self._accept_answers = True

        rnd = random.randint(0, len(self._lines))
        parts = self._lines[rnd].split("|")
        self._question = parts[0]
        self._answer = parts[1]
        self._hidden = re.sub("[0-9a-zA-Z]", HIDDEN_CHAR, self._answer)
        self._hidden_count = len(self._hidden)
        return self._question

    def _revealLetter(self):
        """Makes one letter visible. First and second are revealed first,
        other random. Returns false if full reveal"""
        # All letters hidden
        string = list(self._hidden)
        if self._hidden_count == len(self._answer):
            string[0] = self._answer[0]
            self._hidden = "".join(string)
            self._hidden_count -= 1
            return True
        elif self._hidden_count == len(self._answer) - 1 and len(self._answer) != 2:
            string[1] = self._answer[1]
            self._hidden = "".join(string)
            self._hidden_count -= 1
            return True
        # First letter revelaled
        elif self._hidden_count > 1:
            rnd = random.randint(1, len(self._answer) - 1)
            while self._hidden[rnd] != HIDDEN_CHAR:
                rnd = random.randint(1, len(self._answer) - 1)
            string[rnd] = self._answer[rnd]
            self._hidden = "".join(string)
            self._hidden_count -= 1
            return True
        # One letter left, reveal answer
        else:
            self._hidden = self._answer
            self._accept_answers = False
            return False

    def guessAnswer(self, author_id, guess):
        """If guess is correct, updates stats and returns points. Returns `None` otherwise"""
        if utils.unicode_decode(guess.lower()) == self._answer.lower():
            self._accept_answers = False

            if not self._current_combo:
                self._current_combo.append(author_id)
            else:
                if self._current_combo[-1] == author_id:
                    self._current_combo.append(author_id)
                else:
                    self._current_combo.clear()
                    self._current_combo.append(author_id)

            return self.givePoints(author_id)
        return None

    def givePoints(self, author_id):
        """Calculates points, updates stats, returns amount of points"""
        points = self._hidden_count / len(self._answer)
        points = round(points * 10)
        points = 1 if points == 0 else points

        self.updateQuizPoints(author_id, points)
        return points

    def updateQuizQuestions(self):
        self._bot.stats[QUIZ][QUESTIONS] += 1
        self._bot.markStatsDirty()

    def updateQuizPoints(self, author_id, points):
        stats = self._bot.stats[QUIZ]
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        stats[ANSWERED] += 1
        stats[LAST_ANSWERED] = time_now

        user = stats[USERS].get(author_id)
        if not user:
            self.insertUserToStats(author_id)
            user = stats[USERS][author_id]

        user[POINTS] += points
        user[ANSWERED] += 1
        user[LAST_ANSWERED] = time_now

        if self._current_combo[-1] == author_id:
            if user[USER_COMBO] < len(self._current_combo):
                user[USER_COMBO] = len(self._current_combo)

        self._bot.markStatsDirty()

    def insertUserToStats(self, author_id):
        """Creates user entry in stats"""
        stats = self._bot.stats[QUIZ][USERS]
        stats[author_id] = {
            POINTS: 0,
            ANSWERED: 0,
            USER_COMBO: 0,
            LAST_ANSWERED: ""
        }
        self._bot.markStatsDirty()

    def getTop(self, count):
        """Returns a list of tuples of given number of top users sorted by points"""
        if count < 1:
            raise ValueError

        users = self._bot.stats[QUIZ][USERS]
        users = sorted(users.items(), key=lambda x: x[1][POINTS], reverse=True)
        return users[:count]

    def revealLetter(self, timer):
        """Reveals letter for quiz if answers are accepted and restarts timer"""
        if self._accept_answers:
            if self._revealLetter():
                # Restarts timer
                timer = threading.Timer(self.config["timeout"], self.revealLetter)
                timer.args = (timer,)
                self._timer = timer
                self._timer.start()
                self.sendMessage("ayy")
            else:
                timer.cancel()
                self._timer = None
                self._timeout_set = False
                msg = self.config["timeout_text"].format(self._answer)
                self.sendMessage(msg)

    def giveQuestion(self):
        """Gives quiz question and sets a timer to reveal letters"""
        self.sendMessage("{0}\n\n{1}".format(self.getQuestion(), self._hidden))

        if not self._timeout_set:
            timer = threading.Timer(self.config["timeout"], self.revealLetter)
            timer.args = (timer,)
            self._timer = timer
            self._timer.start()
            self._timeout_set = True

    def tryGuess(self, author_id, message):
        """Makes a quiz guess and shows new question if guess is correct"""
        # Might be an answer but answers are not accepted
        if self._accept_answers:
            points = self.guessAnswer(author_id, message)
            # Correct answer
            if points:
                # nickname = self.getNickname(self.fbidToNameCode(author_id))
                msg = self.config["guess_correct"].format(self._bot.fbidToName(author_id), str(points))
                self.sendMessage(msg)
                self._timer.cancel()
                self._timer = None
                self._timeout_set = False
                self.giveQuestion()


def getObj():
    return QuizCmd()
