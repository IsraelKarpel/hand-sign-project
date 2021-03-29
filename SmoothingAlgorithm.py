from numpy import ma
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from pose_format import Pose
from pose_format.numpy import NumPyPoseBody

# padding = NumPyPoseBody(fps=poses[0].body.fps, data=np.zeros(shape=(10, 1, 137, 2)), confidence=np.zeros(shape=(10, 1, 137)))
#
# # Join videos with padding
# pose_body_data = ma.concatenate([ma.concatenate([p.body.data[1:20], padding.data]) for p in poses])
# pose_body_confidence = np.concatenate([np.concatenate([p.body.confidence[1:20], padding.confidence]) for p in poses])



def findStartPointInArr(arr,index):
    startindex = 0
    if index == 0:
        return startindex
    else:
        startindex = (min(arr)+max(arr))/2
    return 20


# This function gets an array and returns the last max point in the array y-wise.
def findEndPointInArr(arr,index):
    index_last_curve = 0
    prev_point = arr[0]
    incline = False
    curr = -1 * arr[0]
    for i in range(1, len(arr)):
        curr = -1 * arr[i]
        if curr < prev_point and incline == True:
            incline = False
            index_last_curve = i
        elif curr > prev_point:
            incline = True
        elif curr <= prev_point:
            incline = False
        prev_point = -1 * arr[i]
    return len(arr)-30



def findAllEndpoints(poses):
    end_pose_points = []
    count_pose = 0
    for pose in poses:
        RWristYpoints = []
        LWristYpoints = []
        number_of_points = len(pose.body.data)
        for i in range(0, number_of_points):
            RWristYpoints.append(pose.body.data[i].data[0][4][1])
            LWristYpoints.append(pose.body.data[i].data[0][4][1])
        end_pose_points.append(min(findEndPointInArr(LWristYpoints,count_pose),findEndPointInArr(RWristYpoints,count_pose)))
        count_pose += 1
    return end_pose_points


def findAllStartpoints(poses):
    start_pose_points = []
    count_pose = 0
    for pose in poses:
        RWristYpoints = []
        LWristYpoints = []
        number_of_points = len(pose.body.data)
        for i in range(0, number_of_points):
            RWristYpoints.append(pose.body.data[i].data[0][4][1])
            LWristYpoints.append(pose.body.data[i].data[0][4][1])
        start_pose_points.append(min(findStartPointInArr(LWristYpoints,count_pose), findStartPointInArr(RWristYpoints,count_pose)))
        count_pose += 1
    return start_pose_points


def runSmoothingAlgorithm(poses):
    newfps = poses[0].body.fps
    padding = NumPyPoseBody(fps=poses[0].body.fps, data=np.zeros(shape=(10, 1, 137, 2)),confidence=np.zeros(shape=(10, 1, 137)))
    num_poses = len(poses)
    end_pose_points = findAllEndpoints(poses)
    start_pose_points = findAllStartpoints(poses)
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
    new_pose.focus()  # Focus pose to not be on 0,0
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

