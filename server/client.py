import cv2
import requests
import time
from signal import signal, SIGINT
from sys import exit


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


def capture_image():
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # Adjust '0' if you have multiple cameras
    time.sleep(2)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video camera")
        exit(1)

    # Read a frame
    ret, frame = cap.read()
    if ret:
        # Save the frame as an image file
        cv2.imwrite('capture.jpg', frame)
    else:
        print("Error: Could not read frame from video camera")

    # Release the camera
    cap.release()


def post_image():
    url = "http://localhost:8000/upload-image/?query=is there a man in the image?"
    files = {'image': open('capture.jpg', 'rb')}
    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            response_data = response.json()
            content = response_data['choices'][0]['message']['content']
            print(content)
        else:
            print("Failed to get a successful response")

    except requests.exceptions.RequestException as e:
        print("Error posting image:", e)


def main():
    signal(SIGINT, handler)
    print("Running... Press CTRL-C to exit.")

    try:
        while True:
            capture_image()
            post_image()
            time.sleep(3)  # Wait for 3 seconds before the next capture
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
