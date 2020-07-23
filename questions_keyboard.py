#!/usr/bin/env python
# coding: utf8
import rospy
from std_msgs.msg import Int32,String
import sys
import tty

# ---------------------------------------------------------------
def questions():
	# node name
	rospy.init_node('questions_keyboard')
	pub=rospy.Publisher('questions_keyboard',String,queue_size=10)
	r = rospy.Rate(10)
	
	# show questions
	print ' ************************'
	print '    QUESTIONS '
	print ' ************************'
	print '  0-What did you find in each room?'
	print '  1-How many rooms are not occupied?'
	print '  2-How many suites did you find until now?'
	print '  3-Is it more probable to find people in the corridors or inside the rooms?'
	print '  4-If you want to find a computer, to which type of room do you go to?'
	print '  5-What is the number of the closest single room?'
	print '  6-How can you go from the current room to the elevator?'
	print '  7-How many books do you estimate to find in the next 2 minutes?'
	print '  8-What is the probability of finding a table in a room without books but that has at least one chair?'	
	print '  9-What rooms are single rooms? And double rooms? And suites? And meeting rooms? And generic rooms?'
 
	tty.setcbreak(sys.stdin)

	while not rospy.is_shutdown():
		# read from keyboard
		k=sys.stdin.read(1)
		if int(k) < 0 or int(k) > 9:
			continue
		pub.publish(k)
		#print 'Asked question: ' , k
		
# ---------------------------------------------------------------
if __name__ == '__main__':
	questions()

