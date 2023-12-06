from pathlib import Path

USE_SAMPLE_INPUT = False

in_path = Path.cwd() / 'input.txt'

sample_input = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".strip()

if USE_SAMPLE_INPUT:
    input = sample_input
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

class Move:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def parse_str(str: str) -> 'Move':
        colors = {'red', 'green', 'blue'}
        color_counts = {}

        for part in str.split(','):
            num, color = part.strip().split()
            num = int(num)
            if color not in colors:
                raise ValueError(f'Unknown color: {color}')
            if color in color_counts:
                raise ValueError(f'Duplicated color: {color}')
            color_counts[color] = num

        for color in colors:
            if color not in color_counts:
                color_counts[color] = 0

        return Move(color_counts['red'], color_counts['green'], color_counts['blue'])

    def __str__(self) -> str:
        return f'{self.red} red, {self.green} green, {self.blue} blue'

class Game:
    def __init__(self, game_num: int, moves: 'list[Move]'):
        self.game_num = game_num
        self.moves = moves

    @staticmethod
    def parse_str(str: str) -> 'Game':
        idx = str.find(':')
        if idx < 0:
            raise ValueError('Malformed game string')

        _, game_num = str[:idx].split()
        move_strs = str[idx+1:].split(';')

        moves = [Move.parse_str(move_str) for move_str in move_strs]

        return Game(int(game_num), moves)

    def __str__(self) -> 'str':
        return f'Game {self.game_num}: ' + '; '.join([str(move) for move in self.moves])

games = [Game.parse_str(line) for line in input.split('\n')]

red_count = 12
green_count = 13
blue_count = 14

game_id_sum = 0

for game in games:
    possible = True
    for move in game.moves:
        if move.red > red_count:
            possible = False
            break
        if move.green > green_count:
            possible = False
            break
        if move.blue > blue_count:
            possible = False
            break
    if possible:
        game_id_sum += game.game_num

print(f'Part 1 Solution: {game_id_sum}')

power_sum = 0

for game in games:
    max_red = 0
    max_green = 0
    max_blue = 0

    for move in game.moves:
        max_red = max(max_red, move.red)
        max_green = max(max_green, move.green)
        max_blue = max(max_blue, move.blue)

    power = max_red * max_green * max_blue

    power_sum += power

print(f'Part 2 solution: {power_sum}')
