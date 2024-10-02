
"""
My game of Fortune
"""
import random
import operator
import typer

from wonderwords import RandomWord
from itertools import cycle


class Player:
    # CR: this class does too much (keeps track of score but also checks input)
    # CR: the seperation of round and total points is confusing (and unnecesery)
    """
    class which define player
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.round_points = 0
        self.total_points = 0

    def __str__(self) -> str:
        state = f"{self.name} total points: {self.total_points}"
        return state

    def add_points(self, points: int) -> None:
        """
        add points to current round
        Args:
            points: amount of point
        """
        # CR: doc string redundant. Change the function name to `add_round_points` and remove the doc string
        self.round_points += points

    def reset_round_points(self) -> None:
        # CR: doc string is redundant.
        """
        reset points to 0 for new round
        """
        self.round_points = 0

    def sum_total_points(self) -> None:
        """
        add points to total points
        """
        # CR: this is a confusing fucntion. and the doc string does not help. If you call sumething sum, I would expect to add the "parts" that are summed.
        # and the docstring says you `add` points - what points are added? neither the name nor the docstring help me understand what this function does.
        self.total_points += self.round_points

    @staticmethod
    def next_round() -> bool:
        # CR: I don't think this function should be part of the Player class. It has nothing to do with the rest of the data and operations in this class.
        """
        ask user if he wants to continue to play or exit the game
        """
        # CR: you searched for `wonderwords` but could not find a package to handle this question? you can use rich.Prompt.confirm.
        user_input = input("Do you want to continue to next word? (yes/no)")
        while True:
            if user_input.lower() in ['1', 'y', 'yes', 'true']:
                is_continue = True
                break
            elif user_input.lower() in ['0', 'n', 'no', 'false']:
                is_continue = False
                break
            else:
                print("Wrong user input")
        return is_continue

    def player_turn(self) -> str:
        """
        asking user to insert his answer to following question in the game
        checking if user value is valid and if not ask again
        """
        # CR: in this class you have some data/ops that deal with score, and some that deal with input validations, and these 2 are hardly connected, don't think they should be in the same class
        while True:
            user_input = input(
                f"{self.name} turn\n"
                f"Points:   {self.round_points} \n"
                f"Guess a letter, word, or type 'exit' or 'pass':\n")
            if user_input.isalpha():
                break
            else:
                print("Inserted value is not valid please try again")

        return user_input


class FortuneWheel:
    """
    game logic class
    """

    def __init__(
            self,
            # CR 1: this is a mypy mistake. You shoule write `word_pool_file: str | None = None`
            # CR 2: If this is a path, why not demand a `pathlib.Path` object?
            word_pool_file: str = None,
            word_count: int = 15,
            player_tries: int = 5,
            player_count: int = 2
    ) -> None:
        """

        Args:
            word_pool_file: a path to pool of words
                example: file with words separated by comma
            word_count: how many words use want in the game
            player_tries: for future reference how many tries user get to guess the word
            player_count: how many max players you want in a game
        """
        self.players = []
        self.current_player = None
        self.word_pool_file = word_pool_file
        self.used_from_pool = []
        self.word_pool = []
        self.word_count = word_count
        # CR: if you are not using this is currently, it probably should not be here. There should be very good reason for "Hachana LeMazgan" like this, and that reason is usually tests, which is not the case here
        self.player_tries = player_tries
        self.player_count = player_count

    def do_work(self) -> None:
        # CR: This is an initialization function. So either call it `initialize_game` or make it part of the constructor, or part of the `start_the_game` function
        """
        game flow
        """
        self.get_word_pool()  # get game words # CR: if you think you need this comment, you need to change the name of the function

        players = self.get_player_count()  # ask how many players u want to have in game

        # enter players names
        self.players = [Player(input(f'Enter the name player #{i + 1}')) for i in range(players)]

        self.start_the_game()

        self.end_game()

    def end_game(self) -> None:
        # CR: a better name would be `print_end_game_message` or `print_game_results` and then remove the docstring
        """
        end of game message
        will show winner of the game
        """
        print('=' * 30)
        players_stats = {}
        for player in self.players:
            player.sum_total_points()
            players_stats[player.name] = player.total_points
            print(player)
        print('=' * 30)
        player_won = max(players_stats.items(), key=operator.itemgetter(1))[0]
        print(f"Player {player_won} won the game with {players_stats[player_won]} points")
        print("Game is over !!!!")
        print("Hope to see you next time !!!!")
        print('=' * 30)

    def get_random_word(self) -> str:
        # CR 1: you can random.shuffle the entire list of words when it's created, and then you don't have to do a random operation on each round.
        # CR 2: you can change the name of the function to `pop_word`
        """
        get word from words pool and remove it from the pool
        Returns:
            word: str selected randomly word

        """
        word = random.choice(self.word_pool)
        self.word_pool.remove(word)
        return word

    def get_player_count(self) -> int:
        # CR: why do you need both this function and the self.players_count prop? why the confusing duplication?
        # CR: this whole thing should have been handled with in the argument parser (typer)
        """
        asking how many players user want in the game
        checking if user input is in side the min max limits
        Returns:
            player number
        """
        question = 'How many players?'
        user_input = input(question)
        while True:
            try:
                players = int(user_input)
                if players < 1:
                    err_message = f'Must be at least 1'
                elif players > self.player_count:
                    err_message = f'Must be at most {self.player_count}'
                else:
                    break
            except ValueError:
                err_message = f'{user_input} is not a number.'
            user_input = input(f'{err_message}\n{question}')
        return players

    def get_word_pool(self) -> None:
        # CR: if this function returns nothing, it should be called `initialize_word_pool`, and not `get_` anything
        # CR: A. This can be done in the constructor
        # CR: B. Class does too much. Should have the list of words, the way to get them is a different story and might be handled differently
        """
        get list of words from file
        if file was not given ill generate list of words my self with RandomWord lib
        making sure list does not exceed the max word value
        """
        if not self.word_pool_file:
            random_word = RandomWord()
            for i in range(self.word_count): # CR: you are not using `i`. In python it's better to use `_` for unused variables
                self.word_pool.append(random_word.word(word_min_length=10))
        else:
            with open(self.word_pool_file, 'r') as file:
                # CR A. this assumes some structure that I am not aware of. Please provide an example for this file
                # CR B. I don't like it that `words` can be 2 different things (and types) and differents line. This should we 1-liner or 2 different variables
                words = file.read()
                words = words.replace(" ", "").split(',')
                # CR: could have done all the operations no `self.word_pool`
                self.word_pool = words
                if len(words) > self.word_count:
                    self.word_pool = random.sample(words, self.word_count)
        self.word_pool = list(filter(None, self.word_pool))

    @staticmethod
    # CR: bad naming. word_status is not clear, and `winner` is also confusing (makes me think it should be the player)
    def word_status(
            word: str,
            guessed: list,
            winner: bool = False
    ) -> str:
        """
        refreshing word shown to user by guesses he made by now
        Args:
            word: current game word
            guessed: all guesses till now
            winner: round is won, to generate the word faster for showing to user

        Returns:
            current word state: cane be part of the word or all
            chars not found will be represented by '_'
        """
        found_word = ''
        if winner:
            found_word = word
        else:
            for char in word:
                if char.isalpha() and char not in guessed:
                    found_word += '_'
                else:
                    found_word += char
        return found_word

    # CR: what is this comment here and not in the docstring? 
    # Returns a string representing the current state of the game
    @staticmethod
    def show_state(obscured_word, guessed):
        return f"""Word:     {obscured_word}\nGuessed:  {', '.join(sorted(guessed))}\n"""

    def start_the_game(self):
        """
        start the game
        """

        # CR: I would put this in it's own function - `print_titile` - it interferes with the reading flow of the code.`
        print('=' * 15)
        print('WHEEL OF Denis')
        print('=' * 15)
        print('')

        guessed = []
        # using this for easier rotation on current player turns
        # CR: this is nice! 
        players = cycle(self.players)
        player = next(players)

        word = self.get_random_word()  # get a random word from list

        while True:
            # CR: I would put this in it's own function 
            print('')
            print('-' * 45)
            print(self.show_state(obscured_word=self.word_status(word, guessed), guessed=guessed))
            print('-' * 45)
            print('')

            user_input = player.player_turn()
            winner, exit_player, pass_player, found_char = self.check_user_guess(user_input, word, guessed)

            if winner:
                points = len(word) - sum(word.count(i) for i in guessed if i in word)
                player.add_points(points)
                is_continue = self.round_won(guessed, player, winner, word)
                if not is_continue:
                    break
                else:
                    guessed, word = self.reset_round()

            elif found_char:
                player.add_points(word.count(found_char))
                found_word = self.word_status(word, guessed)
                if '_' not in found_word:
                    winner = True
                    is_continue = self.round_won(guessed, player, winner, word)
                    if not is_continue:
                        break
                    else:
                        guessed, word = self.reset_round()

            if exit_player:
                break

            if pass_player or not found_char:
                player = next(players)

    def reset_round(self) -> tuple[list, str]:
        """
        reset previous guesses and generate new word
        Returns:
            guesses: empty list
            word: new word for next round
        """
        guessed = []
        word = self.get_random_word()
        return guessed, word

    def round_won(
            self,
            guessed: list,
            player: Player,
            winner: bool,
            word: str
    ) -> bool:
        """
        ask user if he wants to continue to next round
        add some points to last user which guessed the word
        Args:
            guessed: all guesses till now
            player: current player
            winner: if we have a winner
            word: current word

        Returns:
            is_continue: bool continue to next round or exit the game
        """
        print(f'Congratulation you found the word {player.name}')
        print('You get bonus 5 points')
        player.add_points(5)
        print(self.word_status(word, guessed, winner))
        for player in self.players:
            player.sum_total_points()
            player.reset_round_points()
            print(player)
        is_continue = player.next_round()
        return is_continue

    # CR: A function that return 4 values is reaaaaaaaaally messy and confusing. This could fly in JS, but in python it's bad. If you really need it (and I think you dont) return an object
    @staticmethod
    def check_user_guess(
            user_input: str,
            word: str,
            guessed: list
    ) -> tuple[bool, bool, bool, str]:
        # CR: docstring too long. This is a hint that this function is not straightforward
        """
        proceed the game by user input
        char -> check if in current word
        full word -> check if it's a word
        pass -> pass your turn
        exit -> exit the game
        Args:
            user_input:  user input can be char/full word/exit/pass
            word: current word in the game
            guessed: all guesses from users

        Returns:
            tuple of answers
            winner = True if user guessed the word
            exit_game = True if user_input was 'exit'
            pass_turn = True if user_input was 'pass'
            found_char: if user input in word else empty string
        """
        winner = False
        exit_game = False
        pass_turn = False
        found_char = ''
        user_input = user_input.strip().lower()
        if len(user_input) > 1:
            if user_input == word:
                winner = True
            elif user_input == 'exit':
                exit_game = True
            elif user_input == 'pass':
                pass_turn = True

        elif len(user_input) == 1:
            if user_input not in guessed:
                guessed.append(user_input)
            # CR: if the guess is in `guessed`, I get the point, and can do it again and again
            if user_input in word:
                found_char = user_input

        return winner, exit_game, pass_turn, found_char


def main(
        word_pool_file: str = None,
        word_count: int = 15,
        player_tries: int = 5,
        player_count: int = 2
)-> None:
    """

    Args:
        word_pool_file: a path to pool of words, file with words separated by comma
        word_count: how many words use want in the game
        player_tries: for future reference how many tries user get to guess the word
        player_count: how many max players you want in a game


    """
    game = FortuneWheel(
        word_pool_file=word_pool_file,
        word_count=word_count,
        player_count=player_count,
        player_tries=player_tries
    )
    game.do_work()


if __name__ == "__main__":
    typer.run(main)