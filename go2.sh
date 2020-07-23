xterm -hold -e "roscore "&
sleep 5
xterm -hold -e "rosrun stage_ros stageros ./.ubi_ros/ubi.world "&
sleep 5
xterm -hold -e "rosrun ia agent.py "&
sleep 5
xterm -hold -e "rosrun ia questions_keyboard.py "&
sleep 5
xterm -hold -e "rosrun ia object_recognition "&
sleep 5
xterm -hold -e "rosrun teleop_twist_keyboard teleop_twist_keyboard.py "&
