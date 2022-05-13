import halcon as ha
import numpy as np
import cv2
import os

'''
def findHomography(image_1_kp, image_2_kp, matches)
def align_images(images)
use cv2 to align images

'''
def findHomography(image_1_kp, image_2_kp, matches):
    image_1_points = np.zeros((len(matches), 1, 2), dtype=np.float32)
    image_2_points = np.zeros((len(matches), 1, 2), dtype=np.float32)

    for i in range(0,len(matches)):
        image_1_points[i] = image_1_kp[matches[i].queryIdx].pt
        image_2_points[i] = image_2_kp[matches[i].trainIdx].pt


    homography, mask = cv2.findHomography(image_1_points, image_2_points, cv2.RANSAC, ransacReprojThreshold=2.0)

    return homography


#
#   Align the images so they overlap properly...
#
#
def align_images(images):

    #   SIFT generally produces better results, but it is not FOSS, so chose the feature detector
    #   that suits the needs of your project.  ORB does OK
    use_sift = True

    outimages = []

    if use_sift:
        detector = cv2.xfeatures2d.SIFT_create()
    else:
        detector = cv2.ORB_create(1000)

    #   We assume that image 0 is the "base" image and align everything to it
    print("Detecting features of base image")
    outimages.append(images[0])
    image1gray = cv2.cvtColor(images[0],cv2.COLOR_BGR2GRAY)
    image_1_kp, image_1_desc = detector.detectAndCompute(image1gray, None)

    for i in range(1,len(images)):
        print("Aligning image {}".format(i))
        image_gray = cv2.cvtColor(images[i],cv2.COLOR_BGR2GRAY)
        image_i_kp, image_i_desc = detector.detectAndCompute(image_gray, None)

        if use_sift:
            bf = cv2.BFMatcher()
            # This returns the top two matches for each feature point (list of list)
            pairMatches = bf.knnMatch(image_i_desc,image_1_desc, k=2)
            rawMatches = []
            for m,n in pairMatches:
                if m.distance < 0.7*n.distance:
                    rawMatches.append(m)
        else:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            rawMatches = bf.match(image_i_desc, image_1_desc)

        sortMatches = sorted(rawMatches, key=lambda x: x.distance)
        matches = sortMatches[0:128]



        hom = findHomography(image_i_kp, image_1_kp, matches)
        newimage = cv2.warpPerspective(images[i], hom, (images[i].shape[1], images[i].shape[0]), flags=cv2.INTER_LINEAR)

        outimages.append(newimage)
        # If you find that there's a large amount of ghosting, it may be because one or more of the input
        # images gets misaligned.  Outputting the aligned images may help diagnose that.
        # cv2.imwrite("aligned{}.png".format(i), newimage)



    return outimages




#stone 001.jpg as base image for aligning
image_list = ['001.jpg', '002.jpg', '003.jpg', '004.jpg', '005.jpg', '006.jpg']
#ring step0.jpg as base image for aligning
#image_list = ['step0.jpg', 'step1.jpg', 'step2.jpg', 'step3.jpg', 'step4.jpg', 'step5.jpg']
input_folder = './input'
mid_output_folder = './mid_output'

# Align image part
focusimages = []
for image in image_list:
    focusimages.append(cv2.imread("./input/{}".format(image)))
    
images = align_images(focusimages)

for i, image in enumerate(images):
    cv2.imwrite("./mid_output/{name}".format(name=image_list[i]), image)

'''
Image_R: contains all focus level images' R channel
Image_G: contains all focus level images' G channel
Image_B: contains all focus level images' B channel
'''

Image_R = None
Image_G = None
Image_B = None

def stack_RGB(input_folder, image_list):

    Image_R = None
    Image_G = None
    Image_B = None

    for image in image_list:
        image_address = os.path.join(input_folder, image)
        Image = ha.read_image(image_address)
        tmp_Image_R, tmp_Image_G, tmp_Image_B = ha.decompose3(Image)
        if Image_R == None:
            Image_R = tmp_Image_R
            Image_G = tmp_Image_G
            Image_B = tmp_Image_B
        else:
            Image_R = ha.append_channel(Image_R, tmp_Image_R)
            Image_G = ha.append_channel(Image_G, tmp_Image_G)
            Image_B = ha.append_channel(Image_B, tmp_Image_B)
    
    return Image_R, Image_G, Image_B


Image_R, Image_G, Image_B = stack_RGB(mid_output_folder, image_list)

# find each pixels' depth
Depth_R, Confidence_R = ha.depth_from_focus(Image_R, 'bandpass', 'next_maximum')
Depth_G, Confidence_G = ha.depth_from_focus(Image_G, 'bandpass', 'next_maximum')
Depth_B, Confidence_B = ha.depth_from_focus(Image_B, 'bandpass', 'next_maximum')

# select suitable pixels' RGB value in the final result
SharpenedImage_R = ha.select_grayvalues_from_channels(Image_R, Depth_R)
SharpenedImage_G = ha.select_grayvalues_from_channels(Image_G, Depth_G)
SharpenedImage_B = ha.select_grayvalues_from_channels(Image_B, Depth_B)

SharpenedImage = SharpenedImage_R
SharpenedImage = ha.append_channel(SharpenedImage, SharpenedImage_G)
SharpenedImage = ha.append_channel(SharpenedImage, SharpenedImage_B)

# recover RGB image
ha.write_image(SharpenedImage, 'jpeg', 0, './SharpenedImage.jpg')




