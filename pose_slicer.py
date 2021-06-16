BASE_PATH = "pose_en_files/"
from pose_format import Pose
from numpy import ma
import numpy as np
from pose_format.numpy import NumPyPoseBody
names  = ['$A$.en_us.pose','$B$.en_us.pose','$C$.en_us.pose','$D$.en_us.pose',"$F$.en_us.pose","$E$.en_us.pose"
          ,"$G$.en_us.pose","$H$.en_us.pose","$I$.en_us.pose",'$J$.en_us.pose',"$K$.en_us.pose","$L$.en_us.pose",'$M$.en_us.pose','$N$.en_us.pose','$O$.en_us.pose','$P$.en_us.pose','$Q$.en_us.pose','$R$.en_us.pose','$S$.en_us.pose',
          '$T$.en_us.pose','$U$.en_us.pose','$V$.en_us.pose','$W$.en_us.pose','$X$.en_us.pose','$Y$.en_us.pose','$Z$.en_us.pose']



def poseby(filename,step):
    with open(BASE_PATH + filename , "rb") as f:
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



for l in names:
    poseby(l,3)