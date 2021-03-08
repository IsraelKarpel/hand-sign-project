import numpy as np
import numpy.ma as ma

from pose_format import Pose
from pose_format.numpy import NumPyPoseBody
from pose_format.pose_visualizer import PoseVisualizer

import Parser
import PoseLoader
import SubsAnalyse

path = "News.srt"
subs = SubsAnalyse.getCaptions(path)
#subs is a list contains list of captions lins, the format: [start time, end time,
#   the actual time of the captions in deconds, and the actual subs words]
for line in subs:
    basic_words, all_list = Parser.parse_captions1(line[3])
    pose_dic = PoseLoader.load_poses("index.jsonl", "en.us")
    poses = PoseLoader.find_poses("pose_en_files/", pose_dic, basic_words)

    # Create a padding
    num_of_words = (len((line[3]).split()))
    padding = NumPyPoseBody(fps=poses[0].body.fps, data=np.zeros(shape=(10, 1, 137, 2)),
                              confidence=np.zeros(shape=(10, 1, 137)))

    # Join videos with padding
    pose_body_data = ma.concatenate([ma.concatenate([p.body.data, padding.data]) for p in poses])
    pose_body_confidence = np.concatenate([np.concatenate([p.body.confidence, padding.confidence]) for p in poses])

    #calculate the total frames number of the sentence
    frames_per_seconds = len(pose_body_confidence) / line[2]

    # Create joint pose
    new_pose_body = NumPyPoseBody(fps=frames_per_seconds, data=pose_body_data, confidence=pose_body_confidence)
    new_pose = Pose(header=poses[0].header, body=new_pose_body.interpolate(kind='linear'))
    new_pose.focus()  # Focus pose to not be on 0,0

    # Draw video
    v = PoseVisualizer(new_pose)
    v.save_video("joint.mp4", v.draw())