import os
import random
import numpy
import random
from collections import defaultdict
from random import choice

points_files = os.listdir("Points")
print points_files
users_dict = {}
name_email_dict = defaultdict()

# Add points to user's point count
def add_points(line, point_value, email_col_idx):
    data = [x.strip() for x in line.split(',')]
    if users_dict.get(data[email_col_idx]) == None:
        users_dict[data[email_col_idx]] = point_value 
    else:
        users_dict[data[email_col_idx]] = users_dict.get(data[email_col_idx]) + point_value

# Add point for Envision Committee attendance
def add_envision_points(line, email_col_idx):
    data = [x.strip() for x in line.split(',')]
    for cell in data:
        if cell.lower() == "x":
            if users_dict.get(data[email_col_idx]) == None:
                users_dict[data[email_col_idx]] = 1 
            else:
                users_dict[data[email_col_idx]] = users_dict.get(data[email_col_idx]) + 1.0
        
# Return the index of the column with emails
def find_email_col(fields):
    email_col_idx = -1
    for field in fields:
        email_col_idx += 1
        if "email" in field.strip().lower() or "e-mail" in field.strip().lower():#field.strip().lower() == "email" or field.strip().lower() == "e-mail":
            break
    return email_col_idx

def isfloat(input):
    try:
        float(input)
        return True
    except ValueError:
        return False

def count_points(isRaffle):
    for p_file in points_files: 
        p_file_path = "Points/" + p_file
        with open(p_file_path) as f:
            if isfloat(p_file[1:4]):
                points_value = 0.0
                if isRaffle:
                    points_value = 1.0
                else:
                    points_value = float(p_file[1:4])
                
                header = f.readline()  # Get header line
                fields = [x.strip() for x in header.split(',')]
                email_col_idx = find_email_col(fields)
                if email_col_idx < 0:
                    print(p_file + " does not have an email field.")
                else:
                    for line in f:
                        add_points(line, points_value, email_col_idx)
            elif p_file[:8].lower() == "envision": 
                if isRaffle == False:
                    for line in f:
                        add_envision_points(line, 1)
            else:
                print("The file name " + p_file + " does not specify the points value correctly. Example: [2.0] points_file_name")

    points_file = open('SWE_BEE_Points.csv','w')
    points_file.write("Email,Points,Is Member?\n")
    for user in users_dict:
        isMember = float(users_dict.get(user)) >= 10.0
        if isMember:
            print user
        points_file.write("{0},{1},{2}\n".format(user, users_dict.get(user), isMember))

    points_file.close()
    print users_dict
    
def getList():
    users_list = []
    for user in users_dict:
        i = users_dict[user]
        while i > 0:
            users_list.append(user)
            i -= 1
    return users_list
    
def drawWinners():
    count_points(True)
    users_list = getList()
    winners = numpy.random.choice(len(users_list), 3)
    print "start raffle"
    for w in winners:
        print users_list[w]
    

count_points(False)
