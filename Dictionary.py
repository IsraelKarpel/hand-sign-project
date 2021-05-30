import json
from pose_format import Pose
from pose_format.numpy import NumPyPoseBody

from PoseObj import PoseObj

BASE_PATH = "pose_en_files/"


class PoseDictionary:
    def __init__(self, lang, suffix):
        self.lang = lang
        self.suffix = suffix
        self.wordToID = {}
        self.wordToPose = {}

    def add_pose(self, text, pose):
        self.wordToPose[text] = pose

    def load_pose(self, word, filename):
        with open(BASE_PATH + filename + ".pose", "rb") as f:
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
            poseobj = PoseObj(pose,filename,word)
            poseobj.find_start_end_points()
            self.add_pose(word, poseobj)
            return poseobj

    def find_pose(self, word):
        if word in self.wordToPose:
            return self.wordToPose[word]
        else:
            if word in self.wordToID:
                pose = self.load_pose(word, self.wordToID[word])
                if pose:
                    return pose
            else:
                print("pose not found for word: " + str(word))
                return None
