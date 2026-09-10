import time
import pyautogui


class GestureController:

    def __init__(self):
        self.last_pinch_y = None
        self.last_action_time = 0

        self.movement_threshold = 0.04
        self.cooldown = 0.20

    def reset(self):
        self.last_pinch_y = None

    def process(self, gesture, landmarks):

        if gesture != "PINCH":
            self.reset()
            return ""

        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        current_y = (
            thumb_tip.y + index_tip.y
        ) / 2

        if self.last_pinch_y is None:
            self.last_pinch_y = current_y
            return "PINCH ACTIVE"

        movement = self.last_pinch_y - current_y

        now = time.time()

        if (
            abs(movement) >= self.movement_threshold
            and now - self.last_action_time >= self.cooldown
        ):

            if movement > 0:

                pyautogui.press(
                    "volumeup",
                    presses=2
                )

                action = "VOLUME UP"

            else:

                pyautogui.press(
                    "volumedown",
                    presses=2
                )

                action = "VOLUME DOWN"

            self.last_pinch_y = current_y
            self.last_action_time = now

            return action

        return "PINCH ACTIVE"