# This program collects the data from the scheduled programs results and 
# plot the average velocity vs magnetic field.

import math
import os
import numpy as np
import matplotlib.pyplot as plt
import simplejson


# Creating the list of output folders
def out_folder_list():
	list_out_folders = []
	for folder in os.listdir("/home/rabindra/out/"):
		list_out_folders.append(folder)
	return list_out_folders


# Reading the table and plotting the graph
def plot_graph():
    folder_list = out_folder_list()
    list_aver_velocity = []
    field_list = []
    for folder in folder_list:
        data = np.loadtxt("/home/rabindra/out/" + "{}".format(folder) + "/" + "table.txt", skiprows=2)
        start_from = 80
        data_ends_at = len(data)
        cut_off = 4
        average_over = cut_off
        aver_vels_list = []
        for i in range(start_from, data_ends_at - cut_off, average_over):
            av_vel = sum([abs(data[i + j][5]) for j in range(0, average_over, 1)])/average_over
            aver_vels_list.append(av_vel)
        aver_vel = sum(aver_vels_list)/len(aver_vels_list)
        list_aver_velocity.append(aver_vel)
        field_list.append(data[100][8])   # taking the magnetic field value
    field = sorted(field_list)
    vel = sorted(list_aver_velocity)
    # Saving data in a text file
    datafile = open("velocity_field.txt", "w")
    simplejson.dump("magnetic field list = ", datafile)
    simplejson.dump(field, datafile)
    simplejson.dump("average velocity = ", datafile)
    simplejson.dump(vel, datafile)
    datafile.close()
    # Plotting figure
    plt.plot(field, vel)
    plt.scatter(field, vel)
    plt.title("Average velocity vs magnetic field")
    plt.ylabel("Average Velocity")
    plt.ylim(-2, 375)
    plt.xlabel("Magnetic Field")
    plt.xlim(0, 0.010)
    plt.show()

# Calling the plotting function plot_graph()
plot_graph()
