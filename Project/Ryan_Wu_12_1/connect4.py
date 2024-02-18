class Chess:
    state = 0

    def __init__(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_state(self, state):
        if state == 0 or state == 1 or state == 2:
            self.state = state
        else:
            print("State should be 0, 1, 2, where 0 is for no chess, 1 for black, 2 for white")


class connect4:
    width = 0
    height = 0
    board = []
    current_turn = 1  # 1 for player 1, 2 for player 2

    def __init__(self, board_width, board_height):
        if board_height >= 4 and board_width >= 4:
            self.width = board_width
            self.height = board_height
            self.board = [[Chess(0) for _ in range(board_height)] for _ in range(board_width)]

            self.pre_position = [0, 0]
        else:
            print("Size of the board should be greater than 4 x 4")

    def get_turn(self):
        return self.current_turn

    def change_turn(self):
        self.current_turn = 3 - self.current_turn  # 1 -> 2, 2 -> 1

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def put_chess(self, col):
        pos = 0
        while pos < self.height:
            if self.board[col][pos].get_state() != 0 or pos == self.height - 1:
                if pos != 0:
                    if pos == self.height - 1:
                        if self.board[col][pos].get_state() != 0:
                            self.board[col][pos - 1].set_state(self.current_turn)
                        else:
                            self.board[col][pos].set_state(self.current_turn)
                    else:
                        self.board[col][pos - 1].set_state(self.current_turn)
                    break
                else:
                    print("Select a new location, the column is full")
                    self.change_turn()
                    break
            else:
                pos += 1

        # check for vertical win
        pos -= 1
        for i in range(1, 4):
            if pos + i < self.height and self.board[col][pos + i].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        # check for horizontal win (right)
        for i in range(1, 4):
            if col + i < self.width and self.board[col + i][pos].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        # check for horizontal win (left)
        for i in range(1, 4):
            if col - i >= 0 and self.board[col - i][pos].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        # check for diagonal win (bottom left to top right)
        for i in range(1, 4):
            if col - i >= 0 and pos + i < self.height and self.board[col - i][pos + i].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        # check for diagonal win (bottom right to top left)
        for i in range(1, 4):
            if col + i < self.width and pos + i < self.height and self.board[col + i][pos + i].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        # Diagonal (bottom left to top right)
        for i in range(1, 4):
            # if col + i >= 0 and pos - i < self.height and self.board[col + i][pos - i].get_state() == self.current_turn:  # giving me index out of range error
            if 0 <= col + i < self.width and 0 <= pos - i < self.height and self.board[col + i][pos - i].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        # Diagonal (bottom right to top left)
        for i in range(1, 4):
            if col - i >= 0 and pos - i < self.height and self.board[col - i][pos - i].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        self.change_turn()  # Change turn after putting a chess
        return False
