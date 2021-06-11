import pose_format.utils.openpose as op
L = ["A","B","C","D","E","F","G", "H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
for l in L:
    pose  = op.load_openpose_directory("ASL/ASL/{0}".format(str(l)))
    f = open("ASL/poses/{0}".format('$'+str(l)+'$'+'.pose'),"wb")
    pose.write(f)
    f.close()