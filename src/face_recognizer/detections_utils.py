import insightface
import cv2
import imutils

def detect(model,img):

    img = imutils.resize(img, width=int(img.shape[1]/1.0))

    bboxs, landmarks = model.detect(img, threshold=0.5, scale=1.0)

    faces = []
    if bboxs is not None:

        for bbox, landmark in zip(bboxs, landmarks):
            landmarks_points=[]
            for cord in landmark:
                landmarks_points.append([int(cord[0]),int(cord[1])])
            aux_json={
                "upper_left":[int(bbox[0]),int(bbox[1])],
                "down_right":[int(bbox[2]),int(bbox[3])],
                "landmarks":landmarks_points            
            }
            faces.append( aux_json )
    detections={
        "image_width":img.shape[1],
        "image_height":img.shape[0],
        "num_of_detections":len(bboxs),
        "faces_detected":faces
    }
    return detections