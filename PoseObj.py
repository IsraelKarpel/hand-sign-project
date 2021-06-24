RIGHT_SHOULDER = 2
RIGHT_WRIST = 4
RIGHT_ELBOW = 3
LEFT_WRIST = 7
LEFT_ELBOW = 6
RELATIVE_DISTANCE = 15
C = 0
from pose_format import Pose
from numpy import ma
import numpy as np
from pose_format.numpy import NumPyPoseBody

class PoseObj:
    def __init__(self, pose, id, text):
        self.id = id
        self.word = text
        self.pose = pose
        self.is_letter = check_is_letter(text)
        self.length = len(pose.body.data)
        self.is_noun = False
        self.start = None
        self.end = None

    def is_end_calculated(self):
        if self.end is None:
            return False

    def is_start_calculated(self):
        if self.start is None:
            return False

    def set_start(self, value):
        self.start = value

    def set_end(self, value):
        self.end = value

    @staticmethod
    def find_end(wristarr, elbowarr):
        lenarr = len(elbowarr)
        endindex = 0
        above = False  # in the start the wrists are below the elbows
        for i in range(0, lenarr):
            if wristarr[i] >= elbowarr[i] and above == True:
                endindex = i
                above = False
            elif wristarr[i] < elbowarr[i]:
                above = True
        return endindex

    @staticmethod
    def find_end_for_letter(wristarr, shoulderarr,rElbowarr):
        lenarr = len(wristarr)
        endindex = 0
        above = False  # in the start the wrists are below the elbows
        for i in range(0, lenarr):
            s = shoulderarr[i] + 10
            w = wristarr[i]
            #if wristarr[i] >= ((shoulderarr[i] + rElbowarr[i])/2) and above == True:
            if wristarr[i] >= (((shoulderarr[i] + rElbowarr[i]) / 2)+C) and above == True:
                endindex = i
                above = False
            elif wristarr[i] < (((shoulderarr[i] + rElbowarr[i])/2)+C):
                above = True
        #return int(lenarr*2/3)
        return endindex

    @staticmethod
    def find_start(wristarr, elbowarr):
        lenarr = len(elbowarr)
        startindex = 0
        above = False  # in the start the wrists are below the elbows
        for i in range(0, lenarr):
            if wristarr[i] <= elbowarr[i] and above == False:
                startindex = i
                above = True
        return startindex

    @staticmethod
    def find_start_for_letter(wristarr, shoulderarr,rElbowarr):
        lenarr = len(shoulderarr)
        startindex = 0
        above = False  # in the start the wrists are below the elbows
        for i in range(0, lenarr):
            s = shoulderarr[i] + 10
            w = wristarr[i]
            if wristarr[i] <= (((shoulderarr[i] + rElbowarr[i])/2)+C) and above == False:
                startindex = i
                above = True
        #return int(lenarr/3)
        return startindex

    def find_points(self, rWristarr, rElbowarr, lWristarr, lElbowarr):
        lenarr = len(rElbowarr)
        rend = self.find_end(rWristarr, rElbowarr)
        lend = self.find_end(lWristarr, lElbowarr)
        rstart = self.find_start(rWristarr, rElbowarr)
        lstart = self.find_start(lWristarr, lElbowarr)
        startpoint = 0
        endpoint = max(rend, lend)
        if endpoint == 0:
            endpoint = lenarr - 15
        startpoint = check_start(rstart, lstart)
        print("word num points: " + str(lenarr) + " start: " + str(startpoint) + " end: " + str(endpoint))
        return startpoint, endpoint

    def find_points_for_letter(self, rWristarr, rShoulderarr,rElbowarr):
        lenarr = len(rWristarr)
        rend = self.find_end_for_letter(rWristarr, rShoulderarr,rElbowarr)
        rstart = self.find_start_for_letter(rWristarr, rShoulderarr,rElbowarr)
        endpoint = rend
        if endpoint == 0:
            endpoint = lenarr - 15
        startpoint = rstart
        print("letter num points: " + str(lenarr) + " start: " + str(startpoint) + " end: " + str(endpoint))
        return startpoint, endpoint

    def find_start_end_points(self):
        if self.is_letter == False:
            rWristYpoints = []
            lWristYpoints = []
            rElbowYpoints = []
            lElbowYpoints = []
            number_of_points = len(self.pose.body.data)
            for i in range(0, number_of_points):
                rWristYpoints.append(self.pose.body.data[i][0][4][1])
                lWristYpoints.append(self.pose.body.data[i][0][7][1])
                rElbowYpoints.append(self.pose.body.data[i][0][3][1])
                lElbowYpoints.append(self.pose.body.data[i][0][6][1])
            st, en = self.find_points(rWristYpoints, rElbowYpoints, lWristYpoints, lElbowYpoints)
            self.set_start(st)
            self.set_end(en)
        else:
            rWristYpoints = []
            rshoulderYpoints = []
            rElbowYpoints = []
            number_of_points = len(self.pose.body.data)
            for i in range(0, number_of_points):
                rWristYpoints.append(self.pose.body.data[i][0][4][1])
                rshoulderYpoints.append(self.pose.body.data[i][0][2][1])
                rElbowYpoints.append(self.pose.body.data[i][0][3][1])
            st, en = self.find_points_for_letter(rWristYpoints, rshoulderYpoints,rElbowYpoints)
            self.set_start(st)
            self.set_end(en)


def check_start(rstart, lstart):
    if rstart == 0 and lstart != 0:
        startpoint = lstart
    elif lstart == 0 and rstart != 0:
        startpoint = rstart
    else:
        startpoint = min(rstart, lstart)
    return startpoint


def check_is_letter(word):
    count = 0
    for ch in word:
        if ch == '$':
            count += 1
    if count == 2:
        return True
    else:
        return False



def divideposeby(filename,step):
    with open(filename , "rb") as f:
        pose = Pose.read(f.read(), pose_body=NumPyPoseBody)
        pose.normalize(pose.header.normalization_info(
            p1=("pose_keypoints_2d", "Neck"),
            p2=("pose_keypoints_2d", "Nose")
        ), scale_factor=500)

        # Normalize width by shoulder width
        pose.normalize(pose.header.normalization_info(
            p1=("pose_keypoints_2d", "RShoulder"),
            p2=("pose_keypoints_2d", "LShoulder")
        ), scale_factor=500)

        number_of_frames = len(pose.body.data)
        condition = range(0, number_of_frames,step)
        newposebodydata  = pose.body.data[condition]
        new_pose_body_confidence = pose.body.confidence[condition]
        new_pose_body = NumPyPoseBody(20, data=newposebodydata, confidence=new_pose_body_confidence)
        new_pose = Pose(header=pose.header, body=new_pose_body.interpolate(kind='linear'))
        new_pose.focus()
        f = open("C:\\Users\\User\\PycharmProjects\\FINAL\\newASLFS\\"+str(filename), "wb")
        new_pose.write(f)
        f.close()

