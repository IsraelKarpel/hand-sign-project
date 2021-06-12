# Yair
import json
from typing import List
from pose_format import Pose
from pose_format.numpy import NumPyPoseBody
import pose_format.utils.openpose as op
import PoseObj


def load_pose(path, lang):
    file = open(path, 'r', encoding='utf-8')
    pose_dic = []
    if file:
        for line in file.readlines():
            pose = json.loads(line)
            if str(pose["id"]).__contains__(lang):
                pose_dic.append(pose)
        file.close()
        return pose_dic


def find_poses(BASE_PATH, dictionary, basic_words, suffix):
    FILES = []
    texts = []
    poses: List[Pose] = []
    countwords =0
    countnot =0
    for word in basic_words:
        countwords+=1
        pose = dictionary.find_pose(word)
        if pose:
            poses.append(pose)
        else:
            countnot+=1
    print("words total:" +str(countwords))
    print("words not found " +str(countnot))
    return poses
