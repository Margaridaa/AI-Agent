# AI-Agent
A robotic agent travels in a world, finds objects and answers questions that are asked by the user. This world is a floor in a hotel.

The robot is inside a simulator called Stage, and Stage works in ROS, which is the Robot Operating System.

## Possible Questions
The user can ask the robot the following questions:

0. What did you find in each room?
1. How many rooms are not occupied?
2. How many suites did you find until now?
3. Is it more probable to find people in the corridors or inside the rooms?
4. If you want to find a computer, to which type of room do you go to?
5. What is the number of the closest single room?
6. How can you go from the current room to the elevator?
7. How many books do you estimate to find in the next 2 minutes?
8. What is the probability of finding a table in a room without books but that
has at least one chair?
9. What rooms are single rooms? And double rooms? And suites? And meeting rooms? And generic rooms?


## User Guide

You need VirtualBox to open the virtual machine: https://www.virtualbox.org/. Choose a 64bit version.
Everything about ROS can be found here: http://ros.org.
Download the virtual machine with the complete setup in shorturl.at/qwK69.  It is a 4GByte file.

After that, you need to download the file *go2.sh* and place it at **Home**.

Open a terminal and run `./go2.sh`. You should then see some XTerms and the world (the hotel) and some colored squares - the objects. Note that one of these squares will be the robot. The robot will always start in a corridor, in front of the elevator.

