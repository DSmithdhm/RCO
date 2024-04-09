"""
Created 01Apr2024
@author: Dave Smith
To utilize, object = Fusion(0, 0), which initializes num_matches & num_frames = 0
This function compare() receives timestamps from the camera and radar from a Main program.
If the data received from the camera or radar is invalid, ts_camera1 or ts_radar1 == 0.
If either <=0, the function returns match_ok as False and frame_yield = -1
ts_camera1 and ts_radar1 are used, in case more units are added to the system.
The timestamps uses: int(time.time()*1000), which is implemented in read camera.py & readheader.py
It also receives a tolerance in time units.
If the two timestamps are within tolerance, the boolean variable match_ok = True, otherwise it is False.
This module also calculates frame_yield = (Number of Matches) / (Total Compares).
This module returns match_ok and frame_yield.
As tolerance is adjusted in the Main program, frame_yield can be monitored as feedback.
Revisions:
03Apr2024 num_matches & num_frames initialized to 0 without input parameters needed.
          ts_camera1 & ts_radar1 must be >0 or compare returns False and -1.0
          Add read_camera() function
"""

import time
import cv2


class Fusion:

    def __init__(self):
        self.num_matches = int(0)
        self.num_frames = int(0)
        self.ts_camera1 = int(0)
        self.ts_radar1 = int(0)

    def read_camera(self,cap):

        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('Live frame', frame)

        self.ts_camera1 = int(time.time()*1000)

        return self.ts_camera1

    def read_radar(self):
        self.ts_radar1 = int(time.time()*1000)

        return self.ts_radar1
    

    def compare(self, tolerance):  # tolerance int()
        match_ok = False
        frame_yield = -1.0

        if self.ts_camera1 > 0 and self.ts_radar1 > 0:  # Both Camera & Radar have good frames
            # calculate the time stamp differences. Use abs() to keep +
            delta_camera1_radar1 = abs(self.ts_camera1 - self.ts_radar1)
            self.num_frames += 1
            if delta_camera1_radar1 <= tolerance:  # frames with-in Tolerance
                match_ok = True
                self.num_matches += 1
            if self.num_frames != 0:  # Check for divide by zero
                frame_yield = self.num_matches / self.num_frames
            if self.num_frames > 10000:  # remove some old data and give more weight to new data
                self.num_matches /= 2  # yield stays the same.
                self.num_frames /= 2
        return match_ok, frame_yield


def main():

    # Create a VideoCapture object
    # The argument can be either the device index or the name of a video file
    # Device index is just the number to specify which camera
    # Normally one camera will be connected, so we pass 0
    cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Create a Fusion Object
    fusion = Fusion()
    while True:
        # Call read_camera function & capture one frame
        ts_camera = fusion.read_camera(cap)
        print(ts_camera)

        # Call read_radar function & capture one frame
        ts_radar = fusion.read_radar()
        print(ts_radar)

        # Call compare function to insure camera and radar frame timestamps are within tolerance
        # which is passed to the function
        tolerance = int(123)
        match, f_yield = fusion.compare(tolerance)

        print('match = ', match, 'yield = ', f_yield)

        # Break the loop on Cntr C key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1)

    # When everything done, release the capture and destroy the windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
