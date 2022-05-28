import os
import sys
import argparse
import cv2

import rosbag
import rospy
from tf_bag import BagTfTransformer

from sensor_msgs.msg import Image
from cv_bridge import CvBridge


def main():
    """Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("image_topic", help="Image topic.")
    parser.add_argument("tf_source_frame", help="TF source frame name.")
    parser.add_argument("tf_target_frame", help="TF target frame name.")

    args = parser.parse_args()

    output_dir = os.path.join(sys.path[0], "../", args.output_dir)
    print "Extract images from %s on topic %s into %s using reference tf frame: %s and target tf frame: %s" % (args.bag_file,
                                                          args.image_topic, args.output_dir, args.tf_source_frame, args.tf_target_frame)

    bag = rosbag.Bag(args.bag_file, "r")
    
    bag_transformer = BagTfTransformer(bag)

    # print(bag_transformer.getTransformGraphInfo())

    # Create output files
    if os.path.exists(os.path.join(sys.path[0], "../poses.txt")):
        os.remove(os.path.join(sys.path[0], "../poses.txt"))
    poses_file = open(os.path.join(sys.path[0], "../poses.txt"), 'w')
    if os.path.exists(os.path.join(sys.path[0], "../alignment.txt")):
        os.remove(os.path.join(sys.path[0], "../alignment.txt"))
    alignment_file = open(os.path.join(sys.path[0], "../alignment.txt"), 'w')

    bridge = CvBridge()
    count = 1
    for _, msg, t in bag.read_messages(topics=[args.image_topic]):
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        translation, rotation = bag_transformer.lookupTransform(args.tf_source_frame,
        args.tf_target_frame, t)
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        # Save image
        cv2.imwrite(os.path.join(args.output_dir, "frame%06i.png" % count), cv_img)
        # Save full pose in colmap format
        poses_file.write(''.join([str(count), ' ']))
        poses_file.write(' '.join([str(-rotation[3]),str(-rotation[0]),
        str(-rotation[1]),str(-rotation[2]),str(translation[0]),
        str(translation[1]),str(translation[2])]))
        poses_file.write(''.join([' 1 ', "frame%06i.png" % count, '\n\n']))
        # Save camera centres for use in colmap model_aligner
        alignment_file.write(' '.join(["frame%06i.png" % count, 
        str(translation[0]), str(translation[1])]))
        alignment_file.write(''.join([' ', str(translation[2]), '\n']))
        print "Wrote data for image %i" % count
        count += 1

    bag.close()
    poses_file.close()
    alignment_file.close()


    return

if __name__ == '__main__':
    main()
