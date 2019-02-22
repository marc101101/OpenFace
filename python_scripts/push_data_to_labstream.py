import sys
import time
from pylsl import StreamInfo, StreamOutlet

info = StreamInfo("client_name", 'FD', 17, 100, 'float32', 'gum11127_Openface')
outlet = StreamOutlet(info)
k = 0

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
        buff += sys.stdin.read(1)
        if buff.startswith("relevant_entry"):
	        if buff.endswith('\n'):
	            frame_to_push = buff[:-1].split(",")
	            frame_to_push.pop(0)
	            print("Message received: "  +  str(buff[:-1].split(",")))
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