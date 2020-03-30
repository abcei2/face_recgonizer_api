from face_recognizer.detections_utils import *
import insightface


# simple version for working with CWD
model = insightface.model_zoo.get_model('retinaface_r50_v1')
model.prepare(ctx_id = -1, nms=0.4)

def do_detect(img):
    return detect(model,img)
