#Yair
from numpy import ma
import numpy as np
#import matplotlib.pyplot as plt
import scipy.signal
import math
from pose_format.numpy import NumPyPoseBody
from pose_format import Pose
WINDOW_SIZE =21
NUMBER_OF_JOINTS =137


def smoothFinalpose(pose):
    arr = []
    numberofframes = len(pose.body.data)
    for i in range(0,NUMBER_OF_JOINTS):
        arr = []
        for j in range(0,numberofframes):
            arr.append(pose.body.data[j][0][i][1])
        newdata = scipy.signal.savgol_filter(arr, 31, 3)
        for k in range(0, numberofframes):
            pose.body.data[k][0][i][1] = newdata[k]
    return pose


def findPointsInArr(rWristarr,rElbowarr,lWristarr,lElbowarr,index,numberofposes):
    lenarr = len(rElbowarr)
    rendindex = 0
    rstartindex = 0
    # in the start the wrists are below the elbows
    below = True
    for i in range(0,lenarr):
        if rWristarr[i]<= rElbowarr[i] and below==True:
            rstartindex =i
            below=False
        elif rWristarr[i]> rElbowarr[i] and below==False:
            rendindex = i
            below=True
    lendindex = 0
    lstartindex = 0
    # in the start the wrists are below the elbows
    below = True
    for i in range(0, lenarr):
        if lWristarr[i] <= lElbowarr[i] and below == True:
            lstartindex = i
            below = False
        elif lWristarr[i] > lElbowarr[i] and below == False:
            lendindex = i
            below = True
    endpoint= max(rendindex,lendindex)
    startpoint = min(rstartindex,lstartindex)
    if index==0:
        startpoint=0
    if index == numberofposes-1:
        endpoint = lenarr
    return startpoint,endpoint




def findAllStartandEndpoints(poses):
    start_pose_points = []
    end_pose_points = []
    count_pose = 0
    for pose in poses:
        rWristYpoints = []
        lWristYpoints = []
        rElbowYpoints = []
        lElbowYpoints = []
        number_of_points = len(pose.body.data)
        for i in range(0, number_of_points):
            rWristYpoints.append(pose.body.data[i][0][4][1])
            lWristYpoints.append(pose.body.data[i][0][7][1])
            rElbowYpoints.append(pose.body.data[i][0][3][1])
            lElbowYpoints.append(pose.body.data[i][0][6][1])
        st,en = findPointsInArr(rWristYpoints,rElbowYpoints,lWristYpoints,lElbowYpoints,count_pose,len(poses))
        start_pose_points.append(st)
        end_pose_points.append(en)
        count_pose += 1

    return start_pose_points,end_pose_points


def runSmoothingAlgorithm(poses):
    newfps = poses[0].body.fps
    padding = NumPyPoseBody(fps=poses[0].body.fps, data=np.zeros(shape=(10, 1, 137, 2)),confidence=np.zeros(shape=(10, 1, 137)))
    start_pose_points, end_pose_points = findAllStartandEndpoints(poses)
    countp = 0
    for pose in poses:
        if countp== 0:
            new_pose_body_data = pose.body.data[start_pose_points[countp]:end_pose_points[countp]]
            new_pose_body_confidence = pose.body.confidence[start_pose_points[countp]:end_pose_points[countp]]
        else:
            new_pose_body_data = ma.concatenate([new_pose_body_data,pose.body.data[start_pose_points[countp]:end_pose_points[countp]],padding.data])
            new_pose_body_confidence = np.concatenate([new_pose_body_confidence,pose.body.confidence[start_pose_points[countp]:end_pose_points[countp]],padding.confidence])
        countp += 1

    # Create joint pose
    new_pose_body = NumPyPoseBody(fps=poses[0].body.fps, data=new_pose_body_data, confidence=new_pose_body_confidence)
    new_pose = Pose(header=poses[0].header, body=new_pose_body.interpolate(kind='linear'))
    new_pose.focus()
    new_pose = smoothFinalpose(new_pose)
    return new_pose







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

