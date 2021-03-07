import json
from typing import List
from pose_format import Pose
from pose_format.numpy import NumPyPoseBody

def load_poses(path,lang):
    file = open(path, 'r', encoding='utf-8')
    pose_dic = []
    for line in file.readlines():
        pose = json.loads(line)
        if str(pose["id"]).__contains__(lang):
                pose_dic.append(pose)

        # print(len(pose_dic))
    return pose_dic


def find_poses(BASE_PATH,pose_dict,basic_words):
    FILES = []
    for po in pose_dict:
        for word in basic_words:
            if str(po["texts"][0]["text"]).lower() == word.lower():
                FILES.append(str(po["id"]))
    poses: List[Pose] = []
    for f_name in FILES:
        with open(BASE_PATH + f_name + ".pose", "rb") as f:
            pose = Pose.read(f.read(), pose_body=NumPyPoseBody)

        # # Normalize height by neck nose height
        # pose.normalize(pose.header.normalization_info(
        #     p1=("pose_keypoints_2d", "Neck"),
        #     p2=("pose_keypoints_2d", "Nose")
        # ), scale_factor=500)

        # Normalize width by shoulder width
        pose.normalize(pose.header.normalization_info(
            p1=("pose_keypoints_2d", "RShoulder"),
            p2=("pose_keypoints_2d", "LShoulder")
        ), scale_factor=500)

        poses.append(pose)
    return poses


