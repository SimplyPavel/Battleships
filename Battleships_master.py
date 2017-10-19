import random
# prolly can into bigger ships

board = [] 
board_cheat = []
ship_locations = []
total_turns = 0
turn = 1
num_of_ships = 0
num_of_players = 0
players = []

def how_many_players():
    global num_of_players
    num_of_players = int(input("How many players are there? "))
    if num_of_players > 5:
        print("The number is too high. The maximum number of players is 5.")
        how_many_players()

def generate_player(num_of_players, players):
    sequence = 1
    for player in range(num_of_players):
        name = input("Please input player " + str(sequence) + " name: ")
        sequence += 1
        players.append({'Name': name, 'Score': 0})

def how_many_ships():
    global num_of_ships
    num_of_ships = int(input("How many ships do you want to be there? "))

def how_many_turns():
    global total_turns
    total_turns = 3 * num_of_players

def how_many_ships_left():
    current = num_of_ships - len(ship_locations)
    if current == 1:
        return 'first'
    elif current == 2:
        return 'second'
    elif current == 3:
        return 'third'
    elif current == 4:
        return 'fourth'
    elif current == 5:
        return 'fifth'
    elif current == 6:
        return 'sixth' 
    else:
        return 'another'

def player_turns(turn): 
    for i, j in enumerate(players):
        if turn <= num_of_players:
            if turn == i + 1:
                return i, j
        elif turn > num_of_players:
            if (turn - i + 1) % num_of_players == 0: 
                return i, j

def statistics():
    print("Score: ")
    for i in players:
        print(i['Name'], ":", i['Score'])

def init_board(board):
    for x in range(5):
        board.append(["O"] * 5)

init_board(board)
init_board(board_cheat)

def print_board(board):
    for row in board: 
        print(" ".join(row))

def extra_part(row, col):
    ship_extra_row = 0
    ship_extra_col = 0
    chance = random.randrange(1, 3) #sth wrong here, sometimes generates infinite loop here
    if chance == 1:
        if row < (len(board) - 1): #extend ship veritically down
            ship_extra_row = row + 1
            ship_extra_col = col
        elif row >= (len(board) - 1): #extend ship veritically up
            ship_extra_row = row - 1
            ship_extra_col = col
    else:
        if col < (len(board[0]) - 1): #extend ship horizontally right
            ship_extra_row = row
            ship_extra_col = col + 1
        elif col >= (len(board[0]) - 1): #extend ship horizontally left
            ship_extra_row = row
            ship_extra_col = col - 1
    return [ship_extra_row, ship_extra_col] #could return as a list already and remove 'second_part' from generate_ship def


def generate_ships(num_of_ships): 
    try:
        while num_of_ships > len(ship_locations):
            ship_row = random.randint(0, (len(board) - 1))
            ship_col = random.randint(0, (len(board[0]) - 1))
            first_part = list(([ship_row, ship_col]))
            second_part = extra_part(ship_row, ship_col)
            if any(first_part in x for x in ship_locations) == True or any(second_part in y for y in ship_locations) == True:
                continue
            else:
                ship = list([first_part, second_part])
                ship_locations.append(ship)
    except RecursionError:
        print("Couldn't place ships.")
        load_game()

def find_ship_part(where_hit):
    for i, ship in enumerate(ship_locations):
        for j, part in enumerate(ship):
            if part == where_hit:
                return (i, j)

def end_game():
    print("Game Over")
    exit()

def input_check(board):
    global turn
    global ship_locations
    while True:
        while True:
            try:
                guess_row = int(input("Guess Row:")) - 1
                guess_col = int(input("Guess Col:")) - 1
            except ValueError:
                print("Sorry, you can use only numbers!")
                continue
            else:
                break
        where_hit = []
        where_hit.extend([guess_row, guess_col])
        if guess_row < 0 or guess_row >= len(board) or guess_col < 0 or guess_col >= len(board[0]):
            print("Oops, that's not even in the ocean.")
            print_board(board)
        elif board[guess_row][guess_col] == "X" or board[guess_row][guess_col] == "!":
            print("You guessed that one already.")
            print_board(board)
        elif any(where_hit in x for x in ship_locations) == True:
            loc_in_shiplist = find_ship_part(where_hit)
            del ship_locations[loc_in_shiplist[0]][loc_in_shiplist[1]]
            len_bef = len(ship_locations)
            ship_locations = list(filter(None, ship_locations))
            len_af = len(ship_locations)
            if len_af < len_bef: 
                print("Congratulations! You sunk the", how_many_ships_left(), "out of " + str(num_of_ships) + " battleships!")
                player_turns(turn)[1]['Score'] += 0.5
                statistics()
            else:
                print("Congratulations! You hit one of the battleships!")
                player_turns(turn)[1]['Score'] += 1.0
                statistics()
            turn += 1
            board[guess_row][guess_col] = "!"
            print_board(board)
            break
        else:
            print("You missed my battleship!")
            turn += 1
            board[guess_row][guess_col] = "X"
            print_board(board)
            break

def cheat():
    try:
        for ship in ship_locations:
            print("Ship location: ")
            for loc in ship:
                board_cheat[loc[0]][loc[1]] = "!"
                print(loc[0] + 1, loc[1] + 1)
    except IndexError: #sometimes does not generate the second part of a ship...
        print(ship_locations)
        exit()
    print_board(board_cheat)
    print('')

def game(total_turns):
    for turns in range(total_turns):
        if ship_locations == []:
            play_again()
            break
        else:
            print("Turn", turn)
            print("It's %s's turn" % player_turns(turn)[1]['Name'])
            input_check(board)
    else:
        play_again()

def load_game():
    global turn
    turn = 1
    how_many_players()
    generate_player(num_of_players, players)
    how_many_turns()
    ship_locations = []
    how_many_ships()
    generate_ships(num_of_ships)
    cheat_mode = input("Cheat mode on/off? ")
    if cheat_mode == "on":
        cheat()
    else:
        pass
    print_board(board)
    print('Total turns:', total_turns)
    game(total_turns)

def play_again():
    ask_if_again = input("Do you want another match? y/n: ")
    if ask_if_again == "y":
        init_board(board)
        init_board(board_cheat)
        load_game()
    elif ask_if_again == "n":
        end_game()
    else:
        print("Come again?")
        play_again()
    
print("Let's play Battleship!")
load_game()
