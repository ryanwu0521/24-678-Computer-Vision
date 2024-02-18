
class Chess:
    state = 0

    def __init__(self, state):
        self.state = state
        self.pre_position = [0, 0]
        self.pre_state = 0

    def get_state(self):
        return self.state

    def set_state(self, state):
        if state == 0 or state == 1 or state == 2:
            self.state = state
        else:
            print("State should be 0, 1, 2, where 0 is for no chess, 1 for black, 2 for white")

    def set_pre_location(self,col,pos):
        self.pre_position = [col,pos]

class connect4:
    width = 0
    height = 0
    board = []
    nChessGet = 0
    current_turn = 1  # 1 for player 1, 2 for player 2


    def __init__(self, board_width, board_height):
        if board_height >= 4 and board_width >= 4:
            self.width = board_width
            self.height = board_height
            self.board = [[Chess(0) for _ in range(board_height)] for _ in range(board_width)]

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

    def check_draw(self):
        return self.nChessGet == self.width*self.height
    
    def put_chess(self, col):
        
        pos = 0
        record = 9
        while pos < self.height:
            if self.board[col][pos].get_state() != 0 or pos == self.height - 1:
                if pos != 0:
                    if pos == self.height - 1:
                        if self.board[col][pos].get_state() != 0:
                            self.board[col][pos - 1].set_state(self.current_turn)
                            self.pre_position = [col, pos - 1]
                            self.nChessGet += 1
                        else:
                            record = self.board[col][pos - 1].get_state()
                            self.board[col][pos].set_state(self.current_turn)
                            self.pre_position = [col, pos]
                            self.nChessGet += 1
                    else:
                        self.board[col][pos - 1].set_state(self.current_turn)
                        self.pre_position = [col, pos - 1]
                        self.nChessGet += 1
                    break
                else:
                    print("Select a new location, the column is full")
                    self.change_turn() # in case of the chess is not put to the board the turn shouldn't change
                    break
            else:
                pos += 1


        if pos==5 and record ==0:
            pos = pos
        else:
            pos -= 1

        # check for vertical win
        for i in range(1, 4):
            if pos + i < self.height and self.board[col][pos + i].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break
            
        # Horizon
        for i in range(4):
            if col-i>=0 and col+(3-i)<self.width:
                if self.board[col-i][pos].get_state() == self.current_turn and self.board[col+1-i][pos].get_state() == self.current_turn and self.board[col+2-i][pos].get_state() == self.current_turn and self.board[col+3-i][pos].get_state() == self.current_turn:
                    return True
        
        # diagonal (top right to bottom left)
        for i in range(4):
            if col-i>=0 and col+3-i<self.width and pos+i<self.height and pos-3+i>=0:
                if self.board[col-i][pos+i].get_state() == self.current_turn and self.board[col+1-i][pos-1+i].get_state() == self.current_turn and self.board[col+2-i][pos-2+i].get_state() == self.current_turn and self.board[col+3-i][pos-3+i].get_state() == self.current_turn:
                    return True
                
        # diagonal (top left to bottom right)
        for i in range(4):
            if col+i<self.width and col-3+i>=0 and pos+i<self.height and pos-3+i>=0:
                if self.board[col+i][pos+i].get_state() == self.current_turn and self.board[col-1+i][pos-1+i].get_state() == self.current_turn and self.board[col-2+i][pos-2+i].get_state() == self.current_turn and self.board[col-3+i][pos-3+i].get_state() == self.current_turn:
                    return True
                 
        self.change_turn()  # Change turn after putting a chess
        return False

    def restart(self):
        self.board = [[Chess(0) for _ in range(self.height)] for _ in range(self.width)]
        self.nChessGet = 0
        self.pre_position = [0, 0]
        self.current_turn = 1
