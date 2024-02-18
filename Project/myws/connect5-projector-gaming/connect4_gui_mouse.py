 # connect4_gui.py
import cv2
import numpy as np
from connect4 import connect4


class Connect4GUI:
    def __init__(self, connect4_game):
        self.connect4_game = connect4_game
        self.square_size = 100
        self.window_name = 'Virtual Connect 4'
        self.black_background = (0, 0, 0)
        # wood_color = (248, 185, 156)  # wood background color
        self.board_image = np.full((connect4_game.get_height() * self.square_size,
                                    connect4_game.get_width() * self.square_size, 3), self.black_background, dtype=np.uint8)
        # self.board_image = np.ones((connect4_game.get_height() * self.square_size, connect4_game.get_width() * self.square_size, 3), np.uint8)  # Initialize board_image
        self.next_move_col = connect4_game.get_width() // 2
        self.not_move = 0
        self.winner = 0
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
                               # int(self.square_size / 2), (255, 0, 0), -1)  # Blue for player 2
                               int(self.square_size / 2), (0, 255, 255), -1)  # Yellow for player 2
                else:
                    cv2.circle(self.board_image,
                               (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)),
                               int(self.square_size / 2), (255, 255, 255), -1)  # White for empty

        # Determine the color for the next move indicator
        # next_player_color = (0, 0, 255) if self.connect4_game.get_turn() == 1 else (255, 0, 0)  # Red for player 1, Blue for player 2
        next_player_color = (0, 0, 255) if self.connect4_game.get_turn() == 1 else (0, 255, 255)  # Red for player 1, Yellow for player 2

        # Draw next move indicator with the next player's color
        indicator_center = (self.next_move_col * self.square_size + int(self.square_size / 2), self.square_size // 4)
        cv2.circle(self.board_image, indicator_center, int(self.square_size / 4), next_player_color, -1)

        cv2.imshow(self.window_name, self.board_image)


    # [Testing] Mouse event for testing game's logic
    def pointting_up_track(self, cx):
        col = cx // 150
        self.next_move_col = col
        self.draw_board()

    def thumb_up_event(self):
        self.test_game_logic(self.next_move_col)

    def thumb_down_event(self):
        self.connect4_game.regret()
    def mouse_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            col = x // self.square_size
            self.test_game_logic(col)
        elif event == cv2.EVENT_MOUSEMOVE:
            col = x // self.square_size
            self.next_move_col = col
            if self.not_move == 0:
                self.draw_board()

    # function to draw the winning move
    def draw_winning_move(self, winner):
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
                               # int(self.square_size / 2), (255, 0, 0), -1)  # Blue for player 2
                               int(self.square_size / 2), (0, 255, 255), -1)  # Yellow for player 2
                else:
                    cv2.circle(self.board_image,
                               (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)),
                               int(self.square_size / 2), (150, 150, 150), -1)  # Dark gray for empty

    # function to draw the result message
    def draw_result_message(self, message, text_color=(255, 255, 255)):

        text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_PLAIN, 3, 3)[0]
        text_x = (self.board_image.shape[1] - text_size[0]) // 2
        text_y = (self.board_image.shape[0] + text_size[1]) // 6

        cv2.putText(self.board_image, message, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 3, text_color, 6)


    def test_game_logic(self, col):
        state = self.connect4_game.get_turn()
        if self.connect4_game.put_chess(col):
            self.next_move_col = col
            winner = state
            # text_color = (0, 0, 255) if winner == 1 else (255, 0, 0)  # Red for player 1, Blue for player 2
            text_color = (0, 0, 255) if winner == 1 else (0, 255, 255)  # Red for player 1, Yellow for player 2

            print("Player " + str(winner) + " wins!")

            # Create a new board image to avoid overlapping with existing circles
            self.board_image = np.full((self.connect4_game.get_height() * self.square_size,
                                        self.connect4_game.get_width() * self.square_size, 3), self.black_background, dtype=np.uint8)

            # Draw the winning move
            self.draw_winning_move(winner)

            # Draw the winning message
            self.draw_result_message("Player " + str(winner) + " wins!", text_color)

            cv2.imshow(self.window_name, self.board_image)

            self.not_move = 1
            cv2.waitKey(5000)
            self.not_move = 0

            # Clear the result message
            self.board_image = np.full((connect4_game.get_height() * self.square_size,
                                        connect4_game.get_width() * self.square_size, 3), self.black_background, dtype=np.uint8)
            # cv2.destroyAllWindows()

            self.connect4_game.restart()  # Restart the game

            # Create a new Connect4GUI instance with the updated board
            updated_gui = Connect4GUI(self.connect4_game)
            updated_gui.board_image = self.board_image

            # Set the mouse callback for the new instance
            cv2.setMouseCallback(self.window_name, self.mouse_event)

            # Set the mouse callback for the new instance
            self.next_move_col = self.connect4_game.get_width() // 2
            self.draw_board()

        elif self.connect4_game.check_draw():
            print("it's a draw")

            # Create a new board image to avoid overlapping with existing circles
            self.board_image = np.ones((self.connect4_game.get_height() * self.square_size,
                                        self.connect4_game.get_width() * self.square_size, 3), np.uint8)

            # Draw the draw message
            self.draw_result_message("It's a draw!")

            cv2.imshow(self.window_name, self.board_image)
            self.not_move = 1
            cv2.waitKey(5000)
            self.not_move = 0

            # Clear the result message
            self.board_image = np.ones((self.connect4_game.get_height() * self.square_size,
                                        self.connect4_game.get_width() * self.square_size, 3), np.uint8)

            # cv2.destroyAllWindows()

            self.connect4_game.restart()

            # Create a new Connect4GUI instance with the updated board
            updated_gui = Connect4GUI(self.connect4_game)
            updated_gui.board_image = self.board_image

            # Set the mouse callback for the new instance
            cv2.setMouseCallback(self.window_name, self.mouse_event)

            # Set the mouse callback for the new instance
            self.next_move_col = self.connect4_game.get_width() // 2
            self.draw_board()

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

    # cv2.destroyAllWindows()
