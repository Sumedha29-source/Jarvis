import time
import pyautogui


class GestureController:

    def __init__(self):

        # -------------------------
        # PINCH / VOLUME
        # -------------------------

        self.last_pinch_y = None
        self.last_action_time = 0

        self.movement_threshold = 0.02
        self.volume_cooldown = 0.20


        # -------------------------
        # OPEN PALM → STOP
        # -------------------------

        self.open_palm_start = None
        self.open_palm_triggered = False

        self.stop_hold_time = 1.0


        # -------------------------
        # THUMBS UP → CONFIRM
        # -------------------------

        self.thumbs_up_start = None
        self.thumbs_up_triggered = False

        self.confirm_hold_time = 0.8


    def reset_pinch(self):
        self.last_pinch_y = None


    def reset_open_palm(self):
        self.open_palm_start = None
        self.open_palm_triggered = False


    def reset_thumbs_up(self):
        self.thumbs_up_start = None
        self.thumbs_up_triggered = False


    def reset(self):

        self.reset_pinch()
        self.reset_open_palm()
        self.reset_thumbs_up()


    def process(self, gesture, landmarks):

        now = time.time()


        # ======================================
        # PINCH → VOLUME CONTROL
        # ======================================

        if gesture == "PINCH":

            # Reset unrelated gestures
            self.reset_open_palm()
            self.reset_thumbs_up()

            thumb_tip = landmarks[4]
            index_tip = landmarks[8]

            current_y = (
                thumb_tip.y + index_tip.y
            ) / 2

            if self.last_pinch_y is None:

                self.last_pinch_y = current_y

                return "PINCH ACTIVE"


            movement = (
                self.last_pinch_y - current_y
            )


            if (
                abs(movement) >= self.movement_threshold
                and
                now - self.last_action_time
                >= self.volume_cooldown
            ):

                # Moving hand upward
                if movement > 0:

                    pyautogui.press(
                        "volumeup",
                        presses=5
                    )

                    action = "VOLUME UP"

                # Moving hand downward
                else:

                    pyautogui.press(
                        "volumedown",
                        presses=5
                    )

                    action = "VOLUME DOWN"


                self.last_pinch_y = current_y
                self.last_action_time = now

                return action


            return "PINCH ACTIVE"


        else:

            self.reset_pinch()


        # ======================================
        # OPEN PALM → STOP
        # ======================================

        if gesture == "OPEN PALM":

            self.reset_thumbs_up()

            if self.open_palm_start is None:

                self.open_palm_start = now

                return "HOLD TO STOP"


            elapsed = (
                now - self.open_palm_start
            )


            if (
                elapsed >= self.stop_hold_time
                and
                not self.open_palm_triggered
            ):

                self.open_palm_triggered = True

                return "STOP"


            if self.open_palm_triggered:

                return "STOP"


            remaining = max(
                0,
                self.stop_hold_time - elapsed
            )

            return (
                f"HOLD TO STOP {remaining:.1f}s"
            )


        else:

            self.reset_open_palm()


        # ======================================
        # THUMBS UP → CONFIRM
        # ======================================

        if gesture == "THUMBS UP":

            if self.thumbs_up_start is None:

                self.thumbs_up_start = now

                return "HOLD TO CONFIRM"


            elapsed = (
                now - self.thumbs_up_start
            )


            if (
                elapsed >= self.confirm_hold_time
                and
                not self.thumbs_up_triggered
            ):

                self.thumbs_up_triggered = True

                return "CONFIRM"


            if self.thumbs_up_triggered:

                return "CONFIRM"


            remaining = max(
                0,
                self.confirm_hold_time - elapsed
            )

            return (
                f"HOLD TO CONFIRM {remaining:.1f}s"
            )


        else:

            self.reset_thumbs_up()


        return ""