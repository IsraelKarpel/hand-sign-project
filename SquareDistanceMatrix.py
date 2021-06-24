import math

import numpy as np
from numpy import ma
from pandas import np

WINDOW_SIZE = 11
NUMBER_OF_JOINTS = 137
ALPHA = 0.15




def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def getSquraredDistancesSum(frame1, frame2):
    sum = 0
    distance = 0
    for i in range(0, 137):
        x1 = frame1[i][0]
        y1 = frame1[i][1]
        x2 = frame2[i][0]
        y2 = frame2[i][1]
        if x1 is ma.masked:
            continue
        if y1 is ma.masked:
            continue
        if x2 is ma.masked:
            continue
        if y2 is ma.masked:
            continue
        sum += get_distance(x1, y1, x2, y2)
    return sum


def calculate_win_size(nf1, nf2, startpoint, endpoint):
    window1size = round(nf1 * ALPHA)
    while ((endpoint - window1size) < 0):
        window1size -= 1
    window2size = round(nf2 * ALPHA)
    while (startpoint + window2size > nf2):
        window2size -= 1
    return window1size, window2size


def getSquraredDistancesSumnew(frame1, frame2):
    # d1 = np.sqrt((np.square((np.subtract(frame1, frame2)))).sum(axis=1))
    sum = np.sum(np.sqrt((np.square((np.subtract(frame1, frame2)))).sum(axis=1)))
    return sum

def get_best_connection_point(pose1, pose2, endpoint, startpoint):
    # right now it's a fixed window size but it should be dynamic and specific to the pose
    nf1 = len(pose1.body.data)
    nf2 = len(pose2.body.data)
    window1size, window2size = calculate_win_size(nf1, nf2, startpoint, endpoint)
    distancematrix = np.zeros(shape=(window1size, window2size))
    for i in range(endpoint - window1size, endpoint):
        for j in range(startpoint, startpoint + window2size):
            #d1 = getSquraredDistancesSum(pose1.body.data[i][0], pose2.body.data[j][0])
            d = getSquraredDistancesSumnew(pose1.body.data[i][0], pose2.body.data[j][0])
            distancematrix[i - (endpoint - window1size)][j - startpoint] = d
    min = 1000000
    newstartpoint = startpoint
    newendpoint = endpoint
    # result = np.where(distancematrix == np.amin(distancematrix))
    # listOfCordinates = list(zip(result[0], result[1]))
    # travese over the list of cordinates
    # for cord in listOfCordinates:
    #     print(cord)
    for i in range(0, window1size):
        for j in range(0, window2size):
            if distancematrix[i][j] <= min:
                min = distancematrix[i][j]
                l=i
                k=j
                newstartpoint = j + startpoint
                newendpoint = i + (endpoint - window1size)
    # s = listOfCordinates[0][0]
    # e = listOfCordinates[0][1]
    # newstartpoint = e + startpoint
    # newendpoint = s + (endpoint - window1size)
    print(newstartpoint,newendpoint)
    return newstartpoint, newendpoint


def find_best_connection_points(poses, startpoints, endpoints):
    number_of_poses = len(poses)
    start_pose_points = []
    end_pose_points = []
    i = -1
    for i in range(0, number_of_poses - 1):
        if i == 0:
            start = 0
            start_pose_points.append(start)
        start, end = get_best_connection_point(poses[i], poses[i + 1], endpoints[i], startpoints[i + 1])
        start_pose_points.append(start)
        end_pose_points.append(end)

    end_pose_points.append(endpoints[i + 1])
    return start_pose_points, end_pose_points
