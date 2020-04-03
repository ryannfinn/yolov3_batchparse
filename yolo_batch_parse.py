import csv
import sys
import glob
import os
import pexpect
import re
from collections import Counter

# run the command and return the output to a list
def output_result (child, each_file, pics_count):
	if pics_count == 0:
		child.sendline(each_file)
		child.expect("Enter Image Path:")
	else:
		child.sendline(each_file)
		child.expect("Enter Image Path:")
	print (child.before.decode("UTF-8"))
	return child.before.decode("UTF-8").splitlines()

def command_making ():
	cmd = ["./darknet", "detect", "cfg/yolov3.cfg", "yolov3.weights"]
	return " ".join(cmd)

# copy the predictions.jpg to a proper location
def copy_photo (og_image_file_name):
	photo_name = os.path.basename(og_image_file_name)
	photo_name = os.path.splitext(photo_name)[0]
	os.system("cp predictions.jpg {}/{}_o.jpg".format(f_name,photo_name))

input_folder = sys.argv[1]
output_csv_path = sys.argv[2]

# generate a list of files (appropriate extension)
wildcards = ['*.jpg', '*.jpeg', '*.png']
wildcards.extend ([t.upper() for t in wildcards])  # the tuple of file types
filelist = []
for files in wildcards:
	filelist.extend(glob.glob(os.path.join(input_folder,files)))

# open directory
f_name = os.path.join(input_folder,"output")
if not os.path.exists(f_name):
	os.makedirs(f_name)

ls_all_objects = []
pics_count = 0

print (filelist)

pwd = os.getcwd()
child = pexpect.spawn ("bash")
child.expect (r"bash.*\$")
child.sendline ("cd {}".format(pwd))
child.expect (r"bash.*\$")
child.sendline (command_making())
child.expect ("Enter Image Path:")

def main():
	# a file for writing the csv
	with open(output_csv_path, "w") as output_csv:
		pics_count = 0
	# for loop for executing
		for file in filelist:
			# run the command, get the result (terminal output) from the function
			list_of_output = output_result(child, file, pics_count)
			# Split the result by ":", then take the first slice
			# First and second entry on the list is not data for our use, therefore [1:]
			list_of_objects = [re.split(":",entry)[0] for entry in list_of_output[2:]]
			# get unique objects on the list
			ls_unique_objects = list(sorted(set(list_of_objects)))
			# write the give the filename as first entry on the row
			output_csv.write(os.path.basename(file)+ ",")
			# write the objects to a row, also append the unique object to a list for summary calculation
			for object in ls_unique_objects:
				output_csv.write(object + ",")
				ls_all_objects.append(object)
			output_csv.write("\n")
			# keeping a counter for the number of photos, for summary calculation
			pics_count += 1
			# Append the result for calculating the final result
			copy_photo(file)

	# summary stat
	print ("\nThe number of pictures processed is: {}".format(pics_count))
	print ("Occurence of objects:")
	print (Counter(ls_all_objects))

main()
