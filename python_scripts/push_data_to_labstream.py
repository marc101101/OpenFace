import sys
import time
from pylsl import StreamInfo, StreamOutlet
import numpy as np
import cv2

info = StreamInfo("client_name", 'FD', 17, 100, 'float32', 'gum11127_Openface')
outlet = StreamOutlet(info)

info_video = StreamInfo("client_name_video", 'FDV', 1, 100, 'string', 'gum11127_Openface_video')
outlet_video = StreamOutlet(info_video)
k = 0

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc('F','M','P','4')
out = cv2.VideoWriter('output-' + str(time.time()) + '.avi', fourcc, 20.0, (640, 480))

# std::cout << face_id << ", "
#		<< frame_number << ", " 
#		<< timestamp << ", " 
#		<< landmark_detection_success << ", " 
#		<< landmark_detection_confidence << ", " 
#		<< gaze_direction0.x << ", " 
#		<< gaze_direction0.y << ", " 
#		<< gaze_direction0.z << ", " 
#		<< gaze_direction1.x << ", "
#		<< gaze_direction1.y << ", "
#		<< gaze_direction1.z << ", "
#		<< head_pose[0] << ", "
#		<< head_pose[1] << ", "
#		<< head_pose[2] << ", "
#		<< head_pose[3] << ", "
#		<< head_pose[4] << ", "
#		<< head_pose[5] << std::endl;

try:
    buff = ''
    while True:
        buff += sys.stdin.read(1)
        if buff.startswith("relevant_entry"):
            ret, frame = cap.read()
            if ret == True:
                out.write(frame)
                outlet_video.push_sample(frame)
                if buff.endswith('\n'):
                    frame_to_push = buff[:-1].split(",")
                    frame_to_push.pop(0)
                    print("Message received: " + str(frame_to_push))
                    counter = 0
                    for i in frame_to_push:
                        try:
                            frame_to_push[counter] = float(i)
                            pass
                        except Exception as e:
                            frame_to_push[counter] = 0
                            raise e

                        counter = counter + 1
                    outlet.push_sample(frame_to_push)
                    buff = ''
                    k = k + 1
    else:
        if buff.endswith('\n'):
            print(buff[:-1])
            buff = ''

except KeyboardInterrupt:
    sys.stdout.flush()
pass
print("End of Log: " + str(k))
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
