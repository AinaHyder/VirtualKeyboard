import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep

cap = cv2.VideoCapture(0)
cap.set(3, 1288)  # Set width
cap.set(4, 728)   # Set height

detector = HandDetector(detectionCon=0.8)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finalText = ""
buttonCooldown = 0  # Cooldown counter to prevent multiple entries

class Button:
    def __init__(self, pos, text, size=(80, 80)):
        self.pos = pos
        self.size = size
        self.text = text

def draw_all(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # Draw buttons with gray color
        cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 50), cv2.FILLED)  # Gray color
        cv2.putText(img, button.text, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)  # White text
    return img

# Create button list
buttonList = [Button([100 * j + 50, 100 * i + 50], key) for i in range(len(keys)) for j, key in enumerate(keys[i])]

while True:
    success, img = cap.read()
    if not success or img is None:
        print("Error: Failed to capture image from camera.")
        continue

    # Detect hands and draw landmarks on the image
    hands, img = detector.findHands(img, draw=True)

    # Draw all buttons
    img = draw_all(img, buttonList)

    # Draw the text box once
    cv2.rectangle(img, (50, 350), (700, 450), (255, 255, 255), cv2.FILLED)  # White background
    cv2.putText(img, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)  # Black text

    # Check if any hands are detected
    if hands and buttonCooldown == 0:
        for hand in hands:
            lmList = hand['lmList']  # Get landmarks
            
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                # Check if the index finger tip is inside the button
                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    # Ensure we pass just the coordinates to findDistance
                    point1 = lmList[8][:2]  # Index finger tip
                    point2 = lmList[12][:2]  # Middle finger tip

                    # Find distance between tip of the index finger and middle finger
                    length = detector.findDistance(point1, point2)[0]

                    # Only add the button if index and middle fingers are close enough
                    if length < 40:  # Adjust this threshold for sensitivity
                        cv2.rectangle(img, (x, y), (x + w, y + h), (100, 100, 100), cv2.FILLED)  # Darker gray color for pressed button
                        cv2.putText(img, button.text, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255))
                        finalText += button.text
                        buttonCooldown = 10  # Set cooldown to prevent immediate repeat

    # Decrease cooldown on each loop iteration
    if buttonCooldown > 0:
        buttonCooldown -= 1

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
