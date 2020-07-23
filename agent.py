#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by: Margarida Quelhas, nº 39782; Henrique Albuquerque, nº 39851

from __future__ import print_function
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import time
import math

# -------------------------------------------------------------------#

x_ant = 0
y_ant = 0
obj_ant = ''
obj = ''
loc_ant = ""
loc_ant2 = ""
loc_ant3 = ""
loc = ""

# -------------------------------------------------------------------#

rooms_name = ["room1", "room2", "room3", "room4", "room5", "room6", "room7", "room8", "room9", "room10", "room11", "room12", "room13", "room14"]
# Lists to store info about every room concerning objects.
room1 = []
room2 = []
room3 = []
room4 = []
room5 = []
room6 = []
room7 = []
room8 = []
room9 = []
room10 = []
room11 = []
room12 = []
room13 = []
room14 = []

all_rooms = [room1, room2, room3, room4, room5, room6, room7, room8, room9, room10, room11, room12, room13, room14]

# -------------------------------------------------------------------#

# Lists to store the coordinates to every room.
room1c = [-15.6, 3.6, -3.0, -1.4]
room2c = [-11.8, -9.5, -1.4, 5.3]
room3c = [-11.8, 3.6, 5.3, 7.3]
room4c = [-3.9, -1.4, -1.4, 5.3]
room5c = [-15.6, -11.9, -1.4, 2.6]
room6c = [-15.6, -11.9, 2.6, 7.3]
room7c = [-15.6, -10.8, 7.4, 11.1]
room8c = [-10.8, -5.8, 7.4, 11.1]
room9c = [-5.8, -0.9, 7.4, 11.1]
room10c = [-0.9, 3.6, 7.4, 11.1]
room11c = [-1.4, 3.6, 2.0, 5.3]
room12c = [-1.4, 3.6, -1.4, 2.0]
room13c = [-9.5, -6.7, -1.4, 5.3]
room14c = [-6.7, -3.9, -1.4, 5.3]
elevatorc = [-15.6, -14.0, -3.0, -1.8]

all_coordinates = [room1c, room2c, room3c, room4c, room5c, room6c, room7c, room8c, room9c, room10c, room11c, room12c, room13c, room14c]

# -------------------------------------------------------------------

# Lists to indicate which rooms are connected to which corridors.
connected_to_corridor1 = []
connected_to_corridor2 = []
connected_to_corridor3 = []
connected_to_corridor4 = []

# -------------------------------------------------------------------

# Lists that store single, double, meeting and generic rooms and suites.
single_rooms = []
double_rooms = []
suites = []
meeting_rooms = []
generic_rooms = []

# -------------------------------------------------------------------

# Variables to help the agent answer questions.
rooms_visited = []		            # To keep track of the rooms the agent has visited.
rooms_occupied = []     	        # For question 1
people_in_corridors = []    	    # For question 3
people_in_rooms = []        	    # For question 3
persons_found = []      	        # For question 3
pc_single = ["single"]      	    # For question 4
pc_double = ["double"]          	# For question 4
pc_meeting = ["meeting"]            # For question 4
pc_generic = ["generic"]            # For question 4
pc_suite = ["suite"]        	    # For question 4
closest_singleroom = ""    	        # For question 5
directions_to_elevator = []	        # For question 6
books_found = []        	        # For question 7
start_time = time.time()	        # For question 7
rooms_to_consider_with_table = []   # For question 8

# Names of the corridors and rooms.
corridors = ["room1", "room2", "room3", "room4"]
rooms = ["room5", "room6", "room7", "room8", "room9", "room10", "room11", "room12", "room13", "room14"]

# ---------------------------------------------------------------
# Questions_keyboard callback
# This function's purpose is to answer some questions, using the knowlegde obtained from all the functions created below.

def answers(data):

    global start_time, directions_to_elevator, generic_rooms, all_rooms, rooms_name

    # Answer to question 0.
    if (int(data.data) == 0):
        print("\nAnswer to question 0:")
        i = -1
        flag_no_room_seen = 0

        for room in all_rooms:
            if len(room)!=0:
                flag_no_room_seen=-1

        if flag_no_room_seen==0:
            print("\tI haven't found anything yet.")

        else:
            print("\tI have found:")
            for room in all_rooms:
                i = i + 1
                if (len(room)>0):            
                    print(rooms_name[i], end = " = ")
                    for item in room:
                        if item!=room[-1]:
                            print("%s" % item, end = ", ")
                    print("%s." % room[-1])


    # Answer to question 1.
    if (int(data.data) == 1):
        print("\nAnswer to question 1:\n\tThere are %d rooms not occupied.\n" % (10-len(rooms_occupied)))


    # Answer to question 2.
    if (int(data.data) == 2):
        print("\nAnswer to question 2:\n\tI've found %d suites untill now.\n" % (len(suites)/2))


    # Answer to question 3.
    if (int(data.data) == 3):
        if (len(persons_found) == 0):
            print("\nAnswer to question 3:\n\tNo person has been seen yet.\n")
        else:
            prob_corridors = float(len(people_in_corridors)) / float(len(persons_found))
            prob_rooms = float(len(people_in_rooms)) / float(len(persons_found))

            #print(persons_found)
            #print(people_in_rooms)

            print("\nAnswer to question 3:\n\tThe probability to find people in the corridors is %0.2f and inside the rooms is %0.2f." % (prob_corridors, prob_rooms))

            if (prob_corridors > prob_rooms):
                print("\tIt is, then, more probable to find people in corridors than inside the rooms.\n")
            elif (prob_corridors==prob_rooms):
                print("\tIt is, then, equiprobable.\n")
            else:
                print("\tIt is, then, more probable to find people inside the rooms than in corridors.\n")

     
    # Answer to question 4.
    if (int(data.data) == 4):

        r = where_are_computers()

        if (len(r) > 0):
            if "single" in r:
                str = "single room.\n\t"
            if "double" in r:
                str = "double room.\n\t"
            if "suite" in r:
                str = "suite.\n\t"
            if "meeting" in r:
                str = "meeting room.\n\t"
            if "generic" in r:
                str = "generic room.\n\t"
            print("\nAnswer to question 4: \n\tTo find a computer, you should go to a %s\n" % str)

        if (len(r) == 0):
            print("\nAnswer to question 4: \n\tI still have to travel more around the hotel to be able to answer that question.\n")


    # Answer to question 5.
    if (int(data.data) == 5):
        if closest_singleroom:
            print("\nAnswer to question 5: \n\tThe closest single room is %s\n\t" % closest_singleroom)
        else:
            print("\nAnswer to question 5: \n\tI still have to travel more around the hotel to be able to answer that question.\n")


    # Answer to question 6.
    if (int(data.data) == 6):
        print("\nAnswer to question 6:")
        for direction in directions_to_elevator:
            print(direction)

    
    # Answer to question 7.
    if (int(data.data) == 7):
        question_time = time.time() - start_time # actual time 

        # the agent calculates how many books he has found in the last 2 minutes
        predict_number_books_to_be_seen = 120 * len(books_found) / question_time
        
        print("\nAnswer to question 7:\n\tIn the next 2 minutes I estimate to find %d books.\n" % (predict_number_books_to_be_seen))
        predict_number_books_to_be_seen = 0


    # Answer to question 8.
    if (int(data.data) == 8):
        p = question_8()
        print("\nAnswer to question 8:\n\tThere is a %0.2f probability to find a table in a room without books but with chairs.\n" % p)
    
    
    # Answer to question 9.
    if (int(data.data) == 9):
        print("\nAnswer to question 9:")

        if (len(single_rooms) > 0):
            print("\n\tThe single rooms are:")
            for item in single_rooms:
                if (item != single_rooms[-1]):
                    print("%s, " % item, end = "")
            print("%s.\n" % single_rooms[-1])
        else:
            print("\tI have no information concerning single rooms yet.")

        if (len(double_rooms) > 0):
            print("\n\tThe double rooms are: ")
            for item in double_rooms:
                if (item != double_rooms[-1]):
                    print("%s, " % item, end = "")
            print("%s.\n" % double_rooms[-1])
        else:
            print("\tI have no information concerning double rooms yet.")

        if (len(meeting_rooms) > 0):
            print("\n\tThe meeting rooms are: ")
            for item in meeting_rooms:
                if (item != meeting_rooms[-1]):
                    print("%s, " % item, end = "")
            print("%s.\n" % meeting_rooms[-1])
        else:
            print("\tI have no information concerning meeting rooms yet.")
        
        if (len(suites) > 0):
            print("\n\tThe suites are: ")
            for item in suites:
                if (item != suites[-1]):
                    print("%s, " % item, end = "")
            print("%s.\n" % suites[-1])
        else:
            print("\tI have no information concerning suites yet.")
        
        if (len(generic_rooms) > 0):
            print("\n\tThe generic rooms are: ")
            for item in generic_rooms:
                if (item != generic_rooms[-1]):
                    print("%s, " % item, end = "")
            print("%s.\n" % generic_rooms[-1])
        else:
            print("\tI have no information concerning generic rooms yet.")

# -------------------------------------------------------------------

# Auxiliar function.
# This function's purpose is to provide information on the actual position of the agent.
def position(data):

    global loc_ant, loc, single_rooms, double_rooms, rooms_name, all_rooms
    x=data.pose.pose.position.x-15
    y=data.pose.pose.position.y-1.5

    loc = what_room (x,y)

    if (loc_ant != loc):
        rooms_visited.append(loc)
        if (len(all_rooms[rooms_name.index(loc)]) > 0):
            print("\tThis is the %s. I've detected the following objects here:" % loc)
            print(all_rooms[rooms_name.index(loc)])
        else:
            print("\tThis is the %s." % loc)

    loc_ant = loc
    return x, y

# -------------------------------------------------------------------

# Auxiliar function.
# This function's purpose is to use the agent's objects recognition capacity to update its knowledge everytime it notices a person.
# It also helps constructing the lists "persons_found", "people_in_corridors", "people_in_rooms" and "rooms_occupied", as the agent travels.
def recognize_person(data):
    
    global loc, rooms_occupied, people_in_corridors, people_in_rooms, persons_found


    object_split = data.data.split(',')
        #print(object_split)

    for individual in object_split:
        if "person" in individual:
            persons_name = individual.split('_')
            if individual not in persons_found:
                persons_found.append(individual)
                print("\t\tHello, %s!" % persons_name[1]) 

            if loc in corridors:
                if individual not in people_in_corridors:
                    people_in_corridors.append(individual)

            if loc in rooms:
                if individual not in people_in_rooms:
                    people_in_rooms.append(individual)
                if loc not in rooms_occupied:
                    rooms_occupied.append(loc)

# -------------------------------------------------------------------

# Auxiliar function.
# This function's purpose is to append to a list every object the agent has detected in the room he is in.
def detected_objects_room(data):

    global rooms_name, all_rooms

    categorize_rooms()

    if len(loc)>0:

        object_split = data.data.split(',')
        #print(object_split)

        for item in object_split:
                if len(item)>0:
                    if item not in all_rooms[rooms_name.index(loc)]:
                            all_rooms[rooms_name.index(loc)].append(item)
                            print("\tI've detected %s." % item)

# -------------------------------------------------------------------

# Auxiliar function.
# This function returns the name of the room the agent is currently in, based on its location and the coordinates of all the rooms.
def what_room(x,y):

    global loc, room1c, room2c, room3c, room4c, room5c, room6c, room7c, room8c, room9c, room10c, room11, room12c, room13c, room14c, elevatorc

    if (x > room1c[0] and x < room1c[1] and y > room1c[2] and y < room1c[3]):
        loc = "room1"

    if (x > room2c[0] and x < room2c[1] and y > room2c[2] and y < room2c[3]):
        loc = "room2"

    if (x > room3c[0] and x < room3c[1] and y > room3c[2] and y < room3c[3]):
        loc = "room3"

    if (x > room4c[0] and x < room4c[1] and y > room4c[2] and y < room4c[3]):
        loc = "room4"

    if (x > room5c[0] and x < room5c[1] and y > room5c[2] and y < room5c[3]):
        loc = "room5"

    if (x > room6c[0] and x < room6c[1] and y > room6c[2] and y < room6c[3]):
        loc = "room6"

    if (x > room7c[0] and x < room7c[1] and y > room7c[2] and y < room7c[3]):
        loc = "room7"

    if (x > room8c[0] and x < room8c[1] and y > room8c[2] and y < room8c[3]):
        loc = "room8"

    if (x > room9c[0] and x < room9c[1] and y > room9c[2] and y < room9c[3]):
        loc = "room9"

    if (x > room10c[0] and x < room10c[1] and y > room10c[2] and y < room10c[3]):
        loc = "room10"

    if (x > room11c[0] and x < room11c[1] and y > room11c[2] and y < room11c[3]):
        loc = "room11"

    if (x > room12c[0] and x < room12c[1] and y > room12c[2] and y < room12c[3]):
        loc = "room12"

    if (x > room13c[0] and x < room13c[1] and y > room13c[2] and y < room13c[3]):
        loc = "room13"

    if (x > room14c[0] and x < room14c[1] and y > room14c[2] and y < room14c[3]):
        loc = "room14"

    return loc

# -------------------------------------------------------------------

# Auxiliar Function used to categorize rooms as single, double, meeting, generic rooms or suites.
def categorize_rooms():
    
    global all_rooms, single_rooms, double_rooms, suites, meeting_rooms, generic_rooms, rooms_name
    
    beds_found = []
    tables_found = []
    chairs_found = []
    i = -1

    for room in all_rooms:

            i = i + 1
            room_to_categorize = rooms_name[i]

            for item in room:
                # Count beds in room
                if "bed" in item:
                    if item not in beds_found:
                        beds_found.append(item)
                        
                # Count tables in room
                if "table" in item:
                    if item not in tables_found:
                        tables_found.append(item)
                        
                # Count chairs in room
                if "chair" in item:
                    if item not in chairs_found:
                        chairs_found.append(item)
            
            if (len(beds_found)==1):
                if room_to_categorize not in single_rooms and room_to_categorize not in suites:
                    single_rooms.append(room_to_categorize)
                
            if (len(beds_found)==2):
                if room_to_categorize not in double_rooms and room_to_categorize not in suites:
                    double_rooms.append(room_to_categorize)
                    
                    if room_to_categorize in single_rooms:
                        single_rooms.remove(room_to_categorize)
                        
            # Is the room part of a suite? To be a suite, it has to have at least one bed, which means the outer room had to be categorized as a single or double room previously, or the actual room needs to be a single or double room.
            if (len(rooms_visited) > 1):    
                if (rooms_visited[-2] in rooms and rooms_visited[-1] in rooms and rooms_visited[-2] not in suites and rooms_visited[-1] not in suites):
                    if (rooms_visited[-2] in single_rooms or rooms_visited[-2] in double_rooms or rooms_visited[-1] in single_rooms or rooms_visited[-1] in double_rooms):
                        suites.append(rooms_visited[-2])
                        suites.append(rooms_visited[-1])

                        if (rooms_visited[-2] in single_rooms):
                            single_rooms.remove(rooms_visited[-2])
                        if (rooms_visited[-2] in double_rooms):
                            double_rooms.remove(rooms_visited[-2])
                        
                        if (rooms_visited[-1] in single_rooms):
                            single_rooms.remove(rooms_visited[-1])
                        if (rooms_visited[-1] in double_rooms):
                            double_rooms.remove(rooms_visited[-1])

            elif (len(chairs_found) > 1 and len(tables_found)==1):
                if room_to_categorize not in meeting_rooms:
                    meeting_rooms.append(room_to_categorize)


            # If the room was once categorized as 'Generic' but the agent has categorized it as another type of room, then that room is no longer a 'Generic' room.
            if room_to_categorize in generic_rooms:
                generic_rooms.remove(room_to_categorize)

            # If the room was not categorized, then that room is a 'Generic' room.
            if room_to_categorize not in single_rooms and room_to_categorize not in double_rooms and room_to_categorize not in meeting_rooms and room_to_categorize not in suites and room_to_categorize in rooms:
                if room_to_categorize not in generic_rooms:
                    generic_rooms.append(room_to_categorize)

            beds_found = []
            tables_found = []
            chairs_found = []

# -------------------------------------------------------------------

# Auxiliar Function used to answer question 4.
def where_are_computers():

    global all_rooms, rooms_name, pc_single, pc_double, pc_meeting, pc_generic, pc_suite
    i=-1
    flag = 0
    list_pc_rooms = [pc_single, pc_double, pc_meeting, pc_suite, pc_generic]

    for room in all_rooms:
            i = i + 1
            r = rooms_name[i]
            for item in room:

                if "computer" in item:

                    if r in single_rooms:
                        if r not in pc_single:
                            pc_single.append(r)

                    if r in double_rooms:
                        if r not in pc_double:
                            pc_double.append(r)

                    if r in meeting_rooms:
                        if r not in pc_meeting:
                            pc_meeting.append(r)

                    if r in generic_rooms:
                        if r not in pc_generic:
                            pc_generic.append(r)

                    if r in suites:
                        if r not in pc_suite:
                            pc_suite.append(r)

                    if r in pc_single or r in pc_double or r in pc_meeting or r in pc_suite:
                        if r in pc_generic:
                            pc_generic.remove(r)


                    list_pc_rooms.sort(key=lambda item: (-len(item), item))
                    flag = 1

    if (flag == 1 ):
        return list_pc_rooms[0]
    else:
        return []

# ---------------------------------------------------------------
# Auxiliar function for question 5.
def closest_single_room(data):
    
    global all_coordinates, rooms_name, single_rooms, closest_singleroom
    x=data.pose.pose.position.x-15
    y=data.pose.pose.position.y-1.5

    closest_singlerooom = ""
    i=-1
    d_min = 100
    j = -1
    for room in all_coordinates:
        i = i + 1
        r = rooms_name[i]

        if len(single_rooms)>0:
                    
            if r in single_rooms:
                pm = [float(room[1] + room[0]) / float(2) , float(room[3] + room[2]) / float(2)]

                d = math.sqrt( (x - pm[0])**2 + (y - pm[1])**2 )
                if ( d < d_min):
                    d_min = d
                    j = i

            closest_singleroom = rooms_name[j]

        else:
            closest_singleroom = ""

# ---------------------------------------------------------------
# Auxiliar function for question 6.
# This function fills the "connected_to_corridor" lists, in order to be able to provide information about all the room connections in the hotel, as the agent travels it.
def connections_in_hotel(data):

    global loc, loc_ant2, rooms_visited, connected_to_corridor1, connected_to_corridor2, connected_to_corridor3, connected_to_corridor4
    x=data.pose.pose.position.x-15
    y=data.pose.pose.position.y-1.5

    loc = what_room (x,y)

    if (loc_ant2 != loc):

        if (len(rooms_visited) >= 2):
            
            # Corridors - the agent needs to know what rooms connect to which corridor.
            if loc == "room1":  
                if rooms_visited[-2] not in connected_to_corridor1:
                    #print(rooms_visited[-1])                
                    connected_to_corridor1.append(rooms_visited[-2])
                    if (rooms_visited[-2]=="room2"):
                        connected_to_corridor2.append(loc)
                    if (rooms_visited[-2]=="room3"):
                        connected_to_corridor3.append(loc)
                    if (rooms_visited[-2]=="room4"):
                        connected_to_corridor4.append(loc)
                #print(connected_to_corridor1)
            if loc == "room2":
                if rooms_visited[-2] not in connected_to_corridor2:                         
                    connected_to_corridor2.append(rooms_visited[-2])
                    if (rooms_visited[-2]=="room1"):
                        connected_to_corridor1.append(loc)
                    if (rooms_visited[-2]=="room3"):
                        connected_to_corridor3.append(loc)
                    if (rooms_visited[-2]=="room4"):
                        connected_to_corridor4.append(loc)
                #print(connected_to_corridor2)
            if loc == "room3":
                if rooms_visited[-2] not in connected_to_corridor3:                         
                    connected_to_corridor3.append(rooms_visited[-2])
                    if (rooms_visited[-2]=="room1"):
                        connected_to_corridor1.append(loc)
                    if (rooms_visited[-2]=="room2"):
                        connected_to_corridor2.append(loc)
                    if (rooms_visited[-2]=="room4"):
                        connected_to_corridor4.append(loc)
                #print(connected_to_corridor3)
            if loc == "room4":
                if rooms_visited[-2] not in connected_to_corridor4:                         
                    connected_to_corridor4.append(rooms_visited[-2])
                    if (rooms_visited[-2]=="room1"):
                        connected_to_corridor1.append(loc)
                    if (rooms_visited[-2]=="room2"):
                        connected_to_corridor2.append(loc)
                    if (rooms_visited[-2]=="room3"):
                        connected_to_corridor3.append(loc)
                #print(connected_to_corridor4)


            # Rooms - the agent needs to know what rooms connect to which corridor.
            if loc == "room5":
                if (rooms_visited[-2]=="room1"):
                    connected_to_corridor1.append(loc)
                if (rooms_visited[-2]=="room2"):
                    connected_to_corridor2.append(loc)
                if (rooms_visited[-2]=="room3"):
                    connected_to_corridor3.append(loc)
                if (rooms_visited[-2]=="room4"):
                    connected_to_corridor4.append(loc)
            if loc == "room6":
                if (rooms_visited[-2]=="room1"):
                    connected_to_corridor1.append(loc)
                if (rooms_visited[-2]=="room2"):
                    connected_to_corridor2.append(loc)
                if (rooms_visited[-2]=="room3"):
                    connected_to_corridor3.append(loc)
                if (rooms_visited[-2]=="room4"):
                    connected_to_corridor4.append(loc)
            if loc == "room7":
                if (rooms_visited[-2]=="room1"):
                    connected_to_corridor1.append(loc)
                if (rooms_visited[-2]=="room2"):
                    connected_to_corridor2.append(loc)
                if (rooms_visited[-2]=="room3"):
                    connected_to_corridor3.append(loc)
                if (rooms_visited[-2]=="room4"):
                    connected_to_corridor4.append(loc)
            if loc == "room8":
                if (rooms_visited[-2]=="room1"):
                    connected_to_corridor1.append(loc)
                if (rooms_visited[-2]=="room2"):
                    connected_to_corridor2.append(loc)
                if (rooms_visited[-2]=="room3"):
                    connected_to_corridor3.append(loc)
                if (rooms_visited[-2]=="room4"):
                    connected_to_corridor4.append(loc)
            if loc == "room9":
                if (rooms_visited[-2]=="room1"):
                    connected_to_corridor1.append(loc)
                if (rooms_visited[-2]=="room2"):
                    connected_to_corridor2.append(loc)
                if (rooms_visited[-2]=="room3"):
                    connected_to_corridor3.append(loc)
                if (rooms_visited[-2]=="room4"):
                    connected_to_corridor4.append(loc)
            if loc == "room10":
                if (rooms_visited[-2]=="room1"):
                    connected_to_corridor1.append(loc)
                if (rooms_visited[-2]=="room2"):
                    connected_to_corridor2.append(loc)
                if (rooms_visited[-2]=="room3"):
                    connected_to_corridor3.append(loc)
                if (rooms_visited[-2]=="room4"):
                    connected_to_corridor4.append(loc)
            if loc == "room11":
                if (rooms_visited[-2]=="room1"):
                    connected_to_corridor1.append(loc)
                if (rooms_visited[-2]=="room2"):
                    connected_to_corridor2.append(loc)
                if (rooms_visited[-2]=="room3"):
                    connected_to_corridor3.append(loc)
                if (rooms_visited[-2]=="room4"):
                    connected_to_corridor4.append(loc)
            if loc == "room12":
                if (rooms_visited[-2]=="room1"):
                    connected_to_corridor1.append(loc)
                if (rooms_visited[-2]=="room2"):
                    connected_to_corridor2.append(loc)
                if (rooms_visited[-2]=="room3"):
                    connected_to_corridor3.append(loc)
                if (rooms_visited[-2]=="room4"):
                    connected_to_corridor4.append(loc)
            if loc == "room13":
                if (rooms_visited[-2]=="room1"):
                    connected_to_corridor1.append(loc)
                if (rooms_visited[-2]=="room2"):
                    connected_to_corridor2.append(loc)
                if (rooms_visited[-2]=="room3"):
                    connected_to_corridor3.append(loc)
                if (rooms_visited[-2]=="room4"):
                    connected_to_corridor4.append(loc)
            if loc == "room14":
                if (rooms_visited[-2]=="room1"):
                    connected_to_corridor1.append(loc)
                if (rooms_visited[-2]=="room2"):
                    connected_to_corridor2.append(loc)
                if (rooms_visited[-2]=="room3"):
                    connected_to_corridor3.append(loc)
                if (rooms_visited[-2]=="room4"):
                    connected_to_corridor4.append(loc)

    loc_ant2 = loc

# ---------------------------------------------------------------
# Function for question 6.
def to_the_elevator (data):
    
    global connected_to_corridor1, connected_to_corridor2, connected_to_corridor3, connected_to_corridor4, rooms_visited, loc_ant3, directions_to_elevator

    x=data.pose.pose.position.x-15
    y=data.pose.pose.position.y-1.5

    loc = what_room (x,y)

    if (loc_ant3 != loc):
        directions_to_elevator = list()

        # if the agent is already in corridor 1     
        if (loc=="room1"):
            directions_to_elevator.append("\tLook around. You should be able to detect the elevator in the room you are in.\n")

        # if the agent is in a suite and he is in the most internal room of the suite
        if (loc in suites and loc not in connected_to_corridor1 and loc not in connected_to_corridor2 and loc not in connected_to_corridor3 and loc not in connected_to_corridor4):
            directions_to_elevator.append("\t1 - Go to %s." % rooms_visited[-2])
            
            if (rooms_visited[-2] in connected_to_corridor1):
                directions_to_elevator.append("\t2 - Then go to corridor 1.")
                directions_to_elevator.append("\t3 - Then look around. You should be able to detect the elevator in the room you are in.\n")

            if (rooms_visited[-2] in connected_to_corridor2):
                directions_to_elevator.append("\t2 - Then move to corridor 2.")
                directions_to_elevator.append("\t3 - Then go to corridor 1.")
                directions_to_elevator.append("\t4 - Then look around. You should be able to detect the elevator in the room you are in.\n")

            if (rooms_visited[-2] in connected_to_corridor3):
                half_corridor3 = (room3c[0] + room3c[1] ) / 2                   
                if (x > half_corridor3):
                    directions_to_elevator.append("\t2 - Then go to corridor 3.")
                    directions_to_elevator.append("\t3 - Then move to corridor 4.")                        
                    directions_to_elevator.append("\t4 - Then move to corridor 1.")
                    directions_to_elevator.append("\t5 - Then look around. You should be able to detect the elevator in the room you are in.\n")                
                else:
                    directions_to_elevator.append("\t2 - Then go to corridor 3.")
                    directions_to_elevator.append("\t3 - Then move to corridor 2.")
                    directions_to_elevator.append("\t4 - Then move to corridor 1.")
                    directions_to_elevator.append("\t5 - Then look around. You should be able to detect the elevator in the room you are in.\n")

            if (rooms_visited[-2] in connected_to_corridor4):
                directions_to_elevator.append("\t2 - Then go to corridor 4.")
                directions_to_elevator.append("\t3 - Then move to corridor 1.")
                directions_to_elevator.append("\t4 - Then look around. You should be able to detect the elevator in the room you are in.\n")

                
        elif (loc in connected_to_corridor1):
            directions_to_elevator.append("\t1 - Go to corridor 1.")
            directions_to_elevator.append("\t2 - Then look around. You should be able to detect the elevator in the room you are in.\n")

        elif (loc in connected_to_corridor2):
            directions_to_elevator.append("\t1 - Go to corridor 2.")
            directions_to_elevator.append("\t2 - Go to corridor 1.")
            directions_to_elevator.append("\t3 - Then look around. You should be able to detect the elevator in the room you are in.\n")

        elif (loc in connected_to_corridor3):
                half_corridor3 = (room3c[0] + room3c[1] ) / 2                   
                if (x > half_corridor3):
                    directions_to_elevator.append("\t1 - Go to corridor 3.")
                    directions_to_elevator.append("\t2 - Then move to corridor 4.")                        
                    directions_to_elevator.append("\t3 - Then move to corridor 1.")
                    directions_to_elevator.append("\t4 - Then look around. You should be able to detect the elevator in the room you are in.\n")                
                else:
                    directions_to_elevator.append("\t1 - Go to corridor 3.")
                    directions_to_elevator.append("\t2 - Then move to corridor 2.")
                    directions_to_elevator.append("\t3 - Then move to corridor 1.")
                    directions_to_elevator.append("\t4 - Then look around. You should be able to detect the elevator in the room you are in.\n")

        elif (loc in connected_to_corridor4):
                directions_to_elevator.append("\t1 - Go to corridor 4.")
                directions_to_elevator.append("\t2 - Then move to corridor 1.")
                directions_to_elevator.append("\t3 - Then look around. You should be able to detect the elevator in the room you are in.\n")
        
    loc_ant3 = loc

# ---------------------------------------------------------------
# Function for question 7.
def time_books(data):
    
    global books_found
    
    object_split = data.data.split(',')
    for item in object_split:
        if "book" in item:
            # if the agent still hasn't found any book
            if not books_found:
                books_found.append(item)

            else:
                if item != books_found[-1]:
                    books_found.append(item)
# ---------------------------------------------------------------
def question_8():
    
    global rooms_name, all_rooms, rooms_to_consider_with_table

    i = -1
    p = 0 # Probability
    rooms_to_consider = []
    del rooms_to_consider_with_table[:]

    # Flags to indicate the presence of chairs, books and tables in the rooms.
    flag_chair = 0
    flag_book = 0
    flag_table = 0

    for room in all_rooms:

        i = i + 1
        r = rooms_name[i] # r contains the string value of the name of the room that is being iterated.
        flag_chair = 0
        flag_book = 0
        flag_table = 0
        
        for item in room:
            if "chair" in item:
                flag_chair = 1

            if "book" in item:
                flag_book = 1

            if "table" in item:
                flag_table = 1

        # The room musn't have books, but it must have at least one chair.
        # It is, then, a room to consider when calculating the probability.
        if flag_chair==1 and flag_book==0:
            if r not in rooms_to_consider:
                rooms_to_consider.append(r)
       
            if flag_table==1:
                if r not in rooms_to_consider_with_table:
                    rooms_to_consider_with_table.append(r)

    if (len(rooms_to_consider)==0):
        return 0
        
    else:
        p = float(len(rooms_to_consider_with_table)) / float(len(rooms_to_consider))
        return p

# ---------------------------------------------------------------
def agent():
    rospy.init_node('agent')

    rospy.Subscriber("questions_keyboard", String, answers)
    rospy.Subscriber("object_recognition", String, detected_objects_room)
    rospy.Subscriber("object_recognition", String, time_books)
    rospy.Subscriber("object_recognition", String, recognize_person)
    #rospy.Subscriber("odom", Odometry, callback)
    rospy.Subscriber("odom", Odometry, position)
    rospy.Subscriber("odom", Odometry, connections_in_hotel)
    rospy.Subscriber("odom", Odometry, to_the_elevator)
    rospy.Subscriber("odom", Odometry, closest_single_room)
    rospy.spin()

# ---------------------------------------------------------------
if __name__ == '__main__':
    agent()


