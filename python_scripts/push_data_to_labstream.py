import sys
import time
from pylsl import StreamInfo, StreamOutlet
import cv2
import numpy as np

info = StreamInfo("client_name", 'FD', 17, 100, 'float32', 'gum11127_Openface')
outlet = StreamOutlet(info)
k = 0

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outvideo-' + str(time.time()) +'.mp4', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

#std::cout << face_id << ", "
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
        ret, frame = cap.read()
        if ret == True:
            try:
                out.write(frame)
                cv2.imshow('frame', frame)
            except Exception as e:
                print(e)
        buff += sys.stdin.read(1)
        if buff.startswith("relevant_entry"):
	        if buff.endswith('\n'):
	            frame_to_push = buff[:-1].split(",")
	            frame_to_push.pop(0)
	            print("Message received: "  +  str(frame_to_push))
	            counter = 0
	            for i in frame_to_push:
	            	try:
	            		frame_to_push[counter] = float(i)
	            		pass
	            	except Exception as e:
	            		frame_to_push[counter] = 0
	            		raise e
	            	
	            	counter = counter+1
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
print("End of Log: "  + str(k))
# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()
