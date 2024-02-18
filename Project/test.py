import cv2
import numpy as np


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


class Connect4:
    width = 0
    height = 0
    board = []

    current_turn = 1  # 1 for player 1, 2 for player 2

    def get_turn(self):
        return self.current_turn

    def change_turn(self):
        self.current_turn = 3 - self.current_turn  # 1 -> 2, 2 -> 1

    def __init__(self, board_width, board_height):
        if board_height >= 4 and board_width >= 4:
            self.width = board_width
            self.height = board_height
            self.board = [[Chess(0) for _ in range(board_height)] for _ in range(board_width)]
        else:
            print("Size of the board should be greater than 4 x 4")

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

        # Vertical
        for i in range(1, 4):
            if pos + i < self.height and self.board[col][pos + i].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        for i in range(1, 4):
            if col + i < self.width and self.board[col + i][pos].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        for i in range(1, 4):
            if col - i >= 0 and self.board[col - i][pos].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        for i in range(1, 4):
            if col - i >= 0 and pos + i < self.height and self.board[col - i][pos + i].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        for i in range(1, 4):
            if col + i < self.width and pos + i < self.height and self.board[col + i][pos + i].get_state() == self.current_turn:
                if i == 3:
                    return True
            else:
                break

        # Diagonal (bottom left to top right)
        for i in range(1, 4):
            # if col + i >= 0 and pos - i < self.height and self.board[col + i][pos - i].get_state() == self.current_turn:
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

def test_game_logic(game, col):
    # Test the game logic by placing a piece in the specified column
    if game.put_chess(col):
        winner = game.get_turn()
        if winner == 1:
            text_color = (0, 0, 255)  # Red for player 1
        elif winner == 2:
            text_color = (0, 255, 255)  # Yellow for player 2
        else:
            text_color = (255, 255, 255)  # White for other cases

        print("Player " + str(winner) + " wins!")

        # Calculate the position to center the text
        text_size = cv2.getTextSize("Player " + str(winner) + " wins!", cv2.FONT_HERSHEY_PLAIN, 3, 3)[0]
        text_x = (board_image.shape[1] - text_size[0]) // 2
        text_y = (board_image.shape[0] + text_size[1]) // 6

        cv2.putText(board_image, "Player " + str(winner) + " wins!", (text_x, text_y),
                    cv2.FONT_HERSHEY_PLAIN, 3, text_color, 6)

        cv2.imshow(window_name, board_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit()

# [Testing] Mouse event for testing game's logic

def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        col = x // square_size  # Assuming square_size is defined earlier
        test_game_logic(connect4_game, col)
        # if test_game_logic(connect4_game, col):
        #     print("Winning Move!")
        # else:
        #     print("Not a Winning Move!")

# OpenCV initialization (GUI implementation)
window_name = 'Virtual Connect 4'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window_name, mouse_event)

# Declaring board constants
row_count = 6
column_count = 7
square_size = 100

# Initialize the Connect4 game
connect4_game = Connect4(column_count, row_count)

# Function to draw the Connect 4 board
def draw_board():
    board_image = np.ones((row_count * square_size, column_count * square_size, 3), np.uint8)  # Board background - black

    for row in range(row_count):
        for col in range(column_count):
            top_left = (col * square_size, row * square_size)  # Top left corner of the board
            bottom_right = ((col + 1) * square_size, (row + 1) * square_size)  # Bottom right corner of the board

            if connect4_game.board[col][row].get_state() == 1:
                cv2.circle(board_image,
                           (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)),
                           int(square_size / 2), (0, 0, 255), -1)  # Red for player 1
            elif connect4_game.board[col][row].get_state() == 2:
                cv2.circle(board_image,
                           (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)),
                           int(square_size / 2), (0, 255, 255), -1)  # Yellow for player 2
            else:
                cv2.circle(board_image,
                           (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)),
                           int(square_size / 2), (255, 255, 255), -1)  # White for empty

    cv2.imshow(window_name, board_image)

# Main loop for Connect 4 game
while True:
    draw_board()

    key = cv2.waitKey(1)

    if key == 27:  # Esc key to exit
        break

    board_image = np.ones((row_count * square_size, column_count * square_size, 3), np.uint8)  # Board background - black

cv2.destroyAllWindows()
