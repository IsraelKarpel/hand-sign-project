# Yair
from numpy import ma
import numpy as np
# import matplotlib.pyplot as plt
import scipy.signal
import math
from pose_format.numpy import NumPyPoseBody
from pose_format import Pose

import SquareDistanceMatrix

WINDOW_SIZE = 21
NUMBER_OF_JOINTS = 137


def smoothFinalpose(pose):
    arr = []
    number_of_frames = len(pose.body.data)
    for i in range(0, NUMBER_OF_JOINTS):
        arr = []
        for j in range(0, number_of_frames):
            arr.append(pose.body.data[j][0][i][1])
        newdata = scipy.signal.savgol_filter(arr, 31, 3)
        for k in range(0, number_of_frames):
            pose.body.data[k][0][i][1] = newdata[k]
    return pose


# def get_connection_points(start_points, end_points, poses):
#     index = 0
#     connectionpoints = []
#     print((len(poses)))
#     print(start_points)
#     print(end_points)
#     for i in range(0, len(poses)):
#         index = index + end_points[i] - start_points[i]
#         connectionpoints.append(index)
#     return connectionpoints
#
#
# def smoothFinalposenew(pose, connectionpoints):
#     arr = []
#     numberofframes = len(pose.body.data)
#     for i in range(0, NUMBER_OF_JOINTS):
#         index = 0
#         arr = []
#         for j in range(0, numberofframes):
#             if (j >= (connectionpoints[index] - 15)) and (j < (connectionpoints[index] + 16)):
#                 arr.append(pose.body.data[j][0][i][1])
#                 if (j == (connectionpoints[index] +15)):
#                     newdata = scipy.signal.savgol_filter(arr, 31, 3)
#                     for k in range((connectionpoints[index] - 15)), ((connectionpoints[index] + 15)):
#                         pose.body.data[k][0][i][1] = newdata[k]
#                     index+=1
#                     arr=[]
#
#     return pose


# def find_end(wristarr,elbowarr):
#     lenarr = len(elbowarr)
#     endindex = 0
#     above = False  # in the start the wrists are below the elbows
#     for i in range(0, lenarr):
#         if wristarr[i] >= elbowarr[i] and above == True:
#             rendindex = i
#             above=False
#         elif wristarr[i] < elbowarr[i]:
#             above = True
#     return endindex
#
# def find_start(wristarr,elbowarr):
#     lenarr = len(elbowarr)
#     startindex = 0
#     above = False  # in the start the wrists are below the elbows
#     for i in range(0, lenarr):
#         if wristarr[i] <= elbowarr[i] and above == False:
#             startindex = i
#             above=True
#     return startindex
#
# def check_start(rstart,lstart):
#     if rstart == 0 and lstart != 0:
#         startpoint = lstart
#     elif lstart == 0 and rstart != 0:
#         startpoint = rstart
#     else:
#         startpoint = min(rstart, lstart)
#     return startpoint


# def find_end_start_points(rWristarr,rElbowarr,lWristarr,lElbowarr,index,numberofposes):
#     lenarr=len(rElbowarr)
#     rend = find_end(rWristarr,rElbowarr)
#     lend = find_end(lWristarr,lElbowarr)
#     rstart = find_start(rWristarr, rElbowarr)
#     lstart = find_start(lWristarr, lElbowarr)
#     startpoint = 0
#     endpoint = max(rend,lend)
#     if endpoint == 0:
#         endpoint = lenarr - 15
#     if index == 0:
#         startpoint = 0
#     else:
#         startpoint = check_start(rstart,lstart)
#     if index == numberofposes - 1:
#         endpoint = len(rElbowarr)
#     print("num points: " + str(lenarr) + " start: " + str(startpoint) + " end: " + str(endpoint))
#     return startpoint, endpoint
#

# def find_wrists_elbows_arr(poses):
#     start_pose_points = []
#     end_pose_points = []
#     count_pose = 0
#     for pose in poses:
#         rWristYpoints = []
#         lWristYpoints = []
#         rElbowYpoints = []
#         lElbowYpoints = []
#         number_of_points = len(pose.body.data)
#         for i in range(0, number_of_points):
#             rWristYpoints.append(pose.body.data[i][0][4][1])
#             lWristYpoints.append(pose.body.data[i][0][7][1])
#             rElbowYpoints.append(pose.body.data[i][0][3][1])
#             lElbowYpoints.append(pose.body.data[i][0][6][1])
#         st,en = find_end_start_points(rWristYpoints,rElbowYpoints,lWristYpoints,lElbowYpoints,count_pose,len(poses))
#         start_pose_points.append(st)
#         end_pose_points.append(en)
#         count_pose += 1
#     return start_pose_points,end_pose_points


def get_start_and_end_points_arr(poses):
    start_pose_points = []
    end_pose_points = []
    count_pose = 0
    number_of_poses = len(poses)
    for pose in poses:
        if count_pose == 0:
            start_pose_points.append(0)
        else:
            start_pose_points.append(pose.start)
        if count_pose == number_of_poses - 1:
            end_pose_points.append(pose.length)
        else:
            end_pose_points.append(pose.end)
        count_pose += 1
    return start_pose_points, end_pose_points


def runSmoothingAlgorithm(posesarr, time=None):
    poses = []
    for p in posesarr:
        poses.append(p.pose)
    start_pose_points1, end_pose_points1 = get_start_and_end_points_arr(posesarr)
    start_pose_points, end_pose_points = SquareDistanceMatrix.find_best_connection_points(poses, start_pose_points1,
                                                                                          end_pose_points1)
    #c = get_connection_points(start_pose_points, end_pose_points, poses)
    padding = NumPyPoseBody(fps=poses[0].body.fps, data=np.zeros(shape=(10, 1, 137, 2)),
                            confidence=np.zeros(shape=(10, 1, 137)))
    countp = 0
    for pose in poses:
        if countp == 0:
            new_pose_body_data = \
                pose.body.data[start_pose_points[countp]:end_pose_points[countp]]
            new_pose_body_confidence = \
                pose.body.confidence[start_pose_points[countp]:end_pose_points[countp]]
        else:
            new_pose_body_data = ma.concatenate(
                [new_pose_body_data, pose.body.data[start_pose_points[countp]:end_pose_points[countp]], padding.data])
            new_pose_body_confidence = np.concatenate(
                [new_pose_body_confidence, pose.body.confidence[start_pose_points[countp]:end_pose_points[countp]],
                 padding.confidence])
        countp += 1
    sumframes = 0
    for i in range(0, len(poses)):
        numberframes = end_pose_points[i] - start_pose_points[i]
        sumframes += numberframes

    if time is not None:
        frames_per_seconds = int(sumframes / time)
        new_pose_body = NumPyPoseBody(frames_per_seconds, data=new_pose_body_data,
                                      confidence=new_pose_body_confidence)
    else:
        # Create joint pose
        new_pose_body = NumPyPoseBody(20, data=new_pose_body_data, confidence=new_pose_body_confidence)
    new_pose = Pose(header=poses[0].header, body=new_pose_body.interpolate(kind='linear'))
    new_pose.focus()
    new_pose1 = smoothFinalpose(new_pose)


    lenarray = []
    for i in range(0, len(poses)):
        lenarray.append(end_pose_points[i] - start_pose_points[i])
    return new_pose1, lenarray

# # for checking smoothness
# def anlyze_hands_array(poses):
#     end_pose_points = []
#     count_pose = 0
#     number_points_arr = []
#     for pose in poses:
#         RWristYpoints = []
#         LWristYpoints = []
#         number_of_points = len(pose.body.data)
#         number_points_arr.append(number_of_points)
#         righthandXpoints = []
#         for i in range(0, number_of_points):
#             # RWristYpoints.append(pose.body.data[i][0][4][1])
#             LWristYpoints.append(pose.body.data[i].data[0][40][1])
#         end_pose_points.append(findEndPoint(RWristYpoints))
#         count_pose += 1
#     print(end_pose_points)
#     return end_pose_points
#
#
#
#
#
#
# def trim_poses(poses):
#     endpose = anlyze_hands_array(poses)
#     RWristYpoints = []
#     end_pose_points = []
#     countp = 0
#     for pose in poses:
#         number_of_points = len(pose.body.data)
#         righthandXpoints = []
#
#         for i in range(0, number_of_points):
#             if i >= endpose[countp]:
#                 continue
#             else:
#                 x = pose.body.data[i].data[0][40][0]
#                 RWristYpoints.append(-1 * pose.body.data[i].data[0][4][1])
#         countp += 1
#     print(RWristYpoints)
#     improved = scipy.signal.savgol_filter(RWristYpoints, 31, 3)
#     plt.plot(RWristYpoints)
#     plt.plot(improved, color="red")
#     plt.show()
