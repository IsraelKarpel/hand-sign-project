import spacy
import os
from typing import List

import numpy as np
import numpy.ma as ma

from pose_format import Pose
from pose_format.numpy import NumPyPoseBody
from pose_format.pose_visualizer import PoseVisualizer
import json


all_list = [] # For every word we save the original word, the basic word and its role in the sentence
basic_words = [] #Only the words in their basic format
nlp = spacy.load("en_core_web_sm")

sentence = nlp("we learn computer science" ""     " ")

for token in sentence:
    # Ignore punctuations : / ' . , and so on
    if not token.is_punct and not token.is_space:
        # For some reason, PRON needed to specify on his own
        if token.lemma_ == "-PRON-":
            basic_words.append(token.orth_)
            all_list.append(token.text + "_" + token.orth_ + "_" + token.pos_)
        else:
            basic_words.append(token.lemma_)
            all_list.append(token.text + "_" + token.lemma_ + "_" + token.pos_)
#print(all_list)


#Read the jason and take only the english words
file = open("index.jsonl", 'r', encoding='utf-8')
pose_dic = []
for line in file.readlines():
    pose = json.loads(line)
    if str(pose["id"]).__contains__("en.us"):
        pose_dic.append(pose)

print(len(pose_dic))

FILES = []
for po in pose_dic:
    for word in basic_words:
        if str(po["texts"][0]["text"]).lower()==word.lower():
            FILES.append(str(po["id"]))


BASE_PATH = "pose_en_files/"

# Load all pose files and normalize them
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

# Create a padding
padding = NumPyPoseBody(fps=poses[0].body.fps, data=np.zeros(shape=(10, 1, 137, 2)),
                        confidence=np.zeros(shape=(10, 1, 137)))

# Join videos with padding
pose_body_data = ma.concatenate([ma.concatenate([p.body.data, padding.data]) for p in poses])
pose_body_confidence = np.concatenate([np.concatenate([p.body.confidence, padding.confidence]) for p in poses])

# Create joint pose
new_pose_body = NumPyPoseBody(fps=poses[0].body.fps, data=pose_body_data, confidence=pose_body_confidence)
new_pose = Pose(header=poses[0].header, body=new_pose_body.interpolate(kind='linear'))
new_pose.focus()  # Focus pose to not be on 0,0

# Draw video
v = PoseVisualizer(new_pose)
v.save_video("joint.mp4", v.draw())