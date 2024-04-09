import cv2
def read_camera():
    # Create a VideoCapture object
    # The argument can be either the device index or the name of a video file
    # Device index is just the number to specify which camera
    # Normally one camera will be connected, so we pass 0
    cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('Live frame', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture and destroy the windows
    cap.release()
    cv2.destroyAllWindows()
    
def main():
    read_camera()
     
if __name__ == "__main__":
     main()
