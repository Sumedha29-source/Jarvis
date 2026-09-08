import math

import cv2
import mediapipe as mp


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def distance(point1, point2):
    return math.sqrt(
        (point1.x - point2.x) ** 2
        + (point1.y - point2.y) ** 2
    )


def fingers_extended(landmarks):
    """
    Returns states for:
    index, middle, ring, pinky
    """

    return [
        landmarks[8].y < landmarks[6].y,
        landmarks[12].y < landmarks[10].y,
        landmarks[16].y < landmarks[14].y,
        landmarks[20].y < landmarks[18].y
    ]


def detect_gesture(landmarks):

    fingers = fingers_extended(landmarks)

    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    index_tip = landmarks[8]

    # PINCH
    pinch_distance = distance(
        thumb_tip,
        index_tip
    )

    if pinch_distance < 0.05:
        return "PINCH"

    # THUMBS UP
    other_fingers_folded = not any(fingers)

    thumb_up = (
        thumb_tip.y < thumb_ip.y
    )

    if thumb_up and other_fingers_folded:
        return "THUMBS UP"

    # OPEN PALM
    if all(fingers):
        return "OPEN PALM"

    # FIST
    if not any(fingers):
        return "FIST"

    return "UNKNOWN"


def main():

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not access webcam.")
        return

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:

        print("Gesture system online.")
        print("Press Q to quit.")

        while True:

            success, frame = camera.read()

            if not success:
                break

            # Mirror webcam
            frame = cv2.flip(
                frame,
                1
            )

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = hands.process(
                rgb_frame
            )

            gesture = "NO HAND"

            if results.multi_hand_landmarks:

                hand = results.multi_hand_landmarks[0]

                mp_drawing.draw_landmarks(
                    frame,
                    hand,
                    mp_hands.HAND_CONNECTIONS
                )

                gesture = detect_gesture(
                    hand.landmark
                )

            cv2.putText(
                frame,
                f"Gesture: {gesture}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                "JARVIS Gesture Vision",
                frame
            )

            key = cv2.waitKey(1)

            if key & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()