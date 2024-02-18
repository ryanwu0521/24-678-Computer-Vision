class chess:
    state = 0

    def __init__(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_state(self, state):
        if state == 0 or state == 1 or state == 2:
            self.state = state
        else:
            print("state should be 0, 1, 2. which 0 for no chess, 1 for black, 2 for white")

class connect4:
    width = 0
    height = 0
    board = []
    current_turn = 1  # 1 for player 1, 2 for player 2

    def __init__(self, boardwidth, boardheight):
        if (boardheight >= 4 and boardwidth >= 4):
            self.width = boardwidth
            self.height = boardheight
            self.board = [[chess(0) for i in range(boardheight)] for j in range(boardwidth)]

            self.pre_position = [0, 0]
            self.turn = 1

        else:
            print("size of the board should be greater than 4 x 4")


    def get_turn(self):
        return self.turn

    # function to change turn
    def change_turn(self):
        self.current_turn = 3 - self.current_turn  # 1 -> 2, 2 -> 1

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_pre_position(self):
        return self.pre_position

    def set_pre_position(self, x_cor, y_cor):
        # Take x and y coordinate as input
        self.pre_position = [x_cor, y_cor]

    def regret(self):
        x_cor, y_cor = self.get_pre_position
        self.board[x_cor][y_cor].set_state(0)

    def put_chess(self, state, col):
        pos = 0
        while pos < self.height:
            if self.board[col][pos].get_state() != 0 or pos == self.height - 1:
                if pos != 0:
                    if pos == self.height - 1:
                        if self.board[col][pos].get_state() != 0:
                            self.board[col][pos - 1].set_state(state)
                            self.set_pre_position(col, pos - 1)
                        else:
                            self.board[col][pos].set_state(state)
                            self.set_pre_position(col, pos)
                    else:
                        self.board[col][pos - 1].set_state(state)
                        self.set_pre_position(col, pos - 1)
                    break
                else:
                    print("select a new location, the col is full")
                    self.change_turn()
                    break
            else:
                pos += 1

        pos -= 1

        for i in range(1, 4):
            if pos + i >= 0 and pos + i < self.height:
                if self.board[pos + i][col].get_state() == state:
                    if i == 3:
                        return [True, state]
                    continue
                else:
                    break

        for i in range(1, 4):
            if col + i >= 0 and col + i < self.width:
                if self.board[pos][col + i].get_state() == state:
                    if i == 3:
                        return [True, state]
                    continue
                else:
                    break

        for i in range(1, 4):
            if col - i >= 0 and col - i < self.width:
                if self.board[pos][col - i].get_state() == state:
                    if i == 3:
                        return [True, state]
                    continue
                else:
                    break

        for i in range(1, 4):
            if col - i >= 0 and col - i < self.width and pos + i >= 0 and pos + i < self.height:
                if self.board[pos + i][col - i].get_state() == state:
                    if i == 3:
                        return [True, state]
                    continue
                else:
                    break

        for i in range(1, 4):
            if col + i >= 0 and col + i < self.width and pos + i >= 0 and pos + i < self.height:
                if self.board[pos + i][col + i].get_state() == state:
                    if i == 3:
                        return [True, state]
                    continue
                else:
                    break

        for i in range(1, 4):
            if col + i >= 0 and col + i < self.width and pos - i >= 0 and pos - i < self.height:
                if self.board[pos - i][col + i].get_state() == state:
                    if i == 3:
                        return [True, state]
                    continue
                else:
                    break

        for i in range(1, 4):
            if col - i >= 0 and col - i < self.width and pos - i >= 0 and pos - i < self.height:
                if self.board[pos - i][col - i].get_state() == state:
                    if i == 3:
                        return [True, state]
                    continue
                else:
                    break
        self.change_turn()  # Change turn after putting a chess
        return [False, state]
