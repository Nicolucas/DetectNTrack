
import cv2 

def createTrackerByName(tracker_type):
    major_ver, minor_ver, subminor_ver = cv2.__version__.split('.')
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.legacy.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            tracker = cv2.legacy.TrackerMIL_create()
        elif tracker_type == 'KCF':
            tracker = cv2.legacy.TrackerKCF_create()
        elif tracker_type == 'TLD':
            tracker = cv2.legacy.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            tracker = cv2.legacy.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
            tracker = cv2.legacy.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            tracker = cv2.legacy.TrackerMOSSE_create()
        elif tracker_type == 'CSRT':
            tracker = cv2.legacy.TrackerCSRT_create()
        else:
            tracker = None
            print('Incorrect tracker name')
    return tracker

def rect_to_opencv(rect, imsize_hw):
    imheight, imwidth = imsize_hw
    xmin_abs = rect['xmin'] * imwidth
    ymin_abs = rect['ymin'] * imheight
    xmax_abs = rect['xmax'] * imwidth
    ymax_abs = rect['ymax'] * imheight
    return (xmin_abs, ymin_abs, xmax_abs - xmin_abs, ymax_abs - ymin_abs)


def rect_from_opencv(rect, imsize_hw):
    imheight, imwidth = imsize_hw
    xmin_abs, ymin_abs, width_abs, height_abs = rect
    xmax_abs = xmin_abs + width_abs
    ymax_abs = ymin_abs + height_abs
    return {
        'xmin': xmin_abs / imwidth,
        'ymin': ymin_abs / imheight,
        'xmax': xmax_abs / imwidth,
        'ymax': ymax_abs / imheight,
    }
