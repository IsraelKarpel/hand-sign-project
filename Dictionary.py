import json
from pose_format import Pose
from pose_format.numpy import NumPyPoseBody

from PoseObj import PoseObj

BASE_PATH = "pose_en_files/pose_files/"
# BASE_PATH = "pose_en_files/"
import spacy


class PoseDictionary:
    def __init__(self, lang, suffix, package):
        self.lang = lang
        self.suffix = suffix
        self.wordToID = {}
        self.wordToPose = {}
        # new
        self.IdToWord = {}
        # b
        self.language_package = package
        if package != "None":
            self.nlp_module = spacy.load(package)
        else:
            self.nlp_module = None
        self.dict_array = None

    def add_pose(self, text, pose, id):
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
            pose.focus()
            # new

            pose_id = filename.split('_')[0]
            index = pose_id.find('$')
            if index != -1:
                pose_id = -1
            else:
                if pose_id:
                    pose_id = int(pose_id)

            # new
            poseobj = PoseObj(pose, filename, word, pose_id)
            poseobj.find_start_end_points()
            self.add_pose(word, poseobj, pose_id)
            return poseobj

    def check_if_word_exist(self, word):
        if word in self.wordToID:
            return True
        return False

    def find_pose(self, word):
        if word in self.wordToPose:
            # print("cached "+ word+" "+str(self.lang))
            return self.wordToPose[word]
        else:
            if word in self.wordToID:
                pose = self.load_pose(word, self.wordToID[word])
                if pose:
                    return pose
            else:
                # print("pose not found for word: " + str(word))
                return None

    def find_pose_by_ID(self, id):
        if id == -1:
            return None, None
        try:
            word = self.IdToWord[id]
            if word in self.wordToPose:
                # print("cached "+ word+" "+str(self.lang))
                return self.wordToPose[word] ,word
            else:
                if word in self.wordToID:
                    pose = self.load_pose(word, self.wordToID[word])
                    if pose:
                        return pose, word
                else:
                    # print("pose not found for word: " + str(word))
                    return None,None
        except:
            return None, None


def find_longest_word(dict):
    max_len = -1
    for phrase in dict:
        if (len(phrase)) > max_len:
            max_len = len(phrase)
    return max_len


def create_length_Array(dict):
    lenArray = []
    max_length = find_longest_word(dict)
    for i in range(0, max_length + 1):
        arr = []
        lenArray.append(arr)
    for phrase in dict:
        lenArray[len(phrase)].append(phrase)
    return lenArray
