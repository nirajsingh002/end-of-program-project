import cv2
import numpy as np

def extract_features(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (256, 256))

    # RGB mean
    mean_r = np.mean(img[:,:,2])
    mean_g = np.mean(img[:,:,1])
    mean_b = np.mean(img[:,:,0])

    # HSV mean
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mean_h = np.mean(hsv[:,:,0])
    mean_s = np.mean(hsv[:,:,1])
    mean_v = np.mean(hsv[:,:,2])

    return [mean_r, mean_g, mean_b, mean_h, mean_s, mean_v]
