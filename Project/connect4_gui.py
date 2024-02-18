# connect4_gui.py
import cv2
import numpy as np
from connect4 import connect4
# from connect4V2 import connect4

class Connect4GUI:
    def __init__(self, connect4_game):
        self.connect4_game = connect4_game
        self.square_size = 100
        self.window_name = 'Virtual Connect 4'
        self.board_image = np.ones((connect4_game.get_height() * self.square_size, connect4_game.get_width() * self.square_size, 3), np.uint8)  # Initialize board_image
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.window_name, self.mouse_event)

    # Function to draw the Connect 4 board and Chess placement
    def draw_board(self):
        for row in range(self.connect4_game.get_height()):
            for col in range(self.connect4_game.get_width()):
                top_left = (col * self.square_size, row * self.square_size)
                bottom_right = ((col + 1) * self.square_size, (row + 1) * self.square_size)

                if self.connect4_game.board[col][row].get_state() == 1:
                    cv2.circle(self.board_image,
                               (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)),
                               int(self.square_size / 2), (0, 0, 255), -1)  # Red for player 1
                elif self.connect4_game.board[col][row].get_state() == 2:
                    cv2.circle(self.board_image,
                               (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)),
                               int(self.square_size / 2), (0, 255, 255), -1)  # Yellow for player 2
                else:
                    cv2.circle(self.board_image,
                               (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)),
                               int(self.square_size / 2), (255, 255, 255), -1)  # White for empty

        cv2.imshow(self.window_name, self.board_image)

    # [Testing] Mouse event for testing game's logic
    def mouse_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            col = x // self.square_size
            self.test_game_logic(col)

    def test_game_logic(self, col):
        state = self.connect4_game.get_turn()
        if self.connect4_game.put_chess(col):
        # if self.connect4_game.put_chess(state, col):
            winner = state
            text_color = (0, 0, 255) if winner == 1 else (0, 255, 255)  # Red for player 1, Yellow for player 2

            print("Player " + str(winner) + " wins!")

            # Create a new board image to avoid overlapping with existing circles
            self.board_image = np.ones((self.connect4_game.get_height() * self.square_size,
                                   self.connect4_game.get_width() * self.square_size, 3), np.uint8)

            # draw the final win step
            for row in range(self.connect4_game.get_height()):
                for col in range(self.connect4_game.get_width()):
                    top_left = (col * self.square_size, row * self.square_size)
                    bottom_right = ((col + 1) * self.square_size, (row + 1) * self.square_size)

                    if self.connect4_game.board[col][row].get_state() == 1:
                        cv2.circle(self.board_image,
                                   (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)),
                                   int(self.square_size / 2), (0, 0, 255), -1)  # Red for player 1
                    elif self.connect4_game.board[col][row].get_state() == 2:
                        cv2.circle(self.board_image,
                                   (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)),
                                   int(self.square_size / 2), (0, 255, 255), -1)  # Yellow for player 2
                    else:
                        cv2.circle(self.board_image,
                                   (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)),
                                   int(self.square_size / 2), (255, 255, 255), -1)  # White for empty

            # Draw the winning message
            text_size = cv2.getTextSize("Player " + str(winner) + " wins!", cv2.FONT_HERSHEY_PLAIN, 3, 3)[0]
            text_x = (self.board_image.shape[1] - text_size[0]) // 2
            text_y = (self.board_image.shape[0] + text_size[1]) // 6

            cv2.putText(self.board_image, "Player " + str(winner) + " wins!", (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 3, text_color, 6)

            # Create a new Connect4GUI instance with the updated board
            updated_gui = Connect4GUI(self.connect4_game)
            updated_gui.board_image = self.board_image

            cv2.imshow(self.window_name, self.board_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            exit()

if __name__ == "__main__":
    # Initialize the Connect4 game
    connect4_game = connect4(7, 6)

    # Initialize the GUI
    connect4_gui = Connect4GUI(connect4_game)

    # Main loop for Connect 4 game
    while True:
        connect4_gui.draw_board()

        key = cv2.waitKey(1)

        if key == 27:  # Esc key to exit
            break
