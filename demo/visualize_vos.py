import os
import glob

import numpy as np
import pycocotools.mask as maskUtils
import matplotlib.pyplot as plt

from mmdet.apis import init_detector, inference_tracker, show_result
import mmcv

def save_result_pyplot(img,
                       result,
                       class_names,
                       outfile, 
                       score_thr=0.3,
                       fig_size=(15, 10)):
    """Visualize the detection results on the image.

    Args:
        img (str or np.ndarray): Image filename or loaded image.
        result (tuple[list] or list): The detection result, can be either
            (bbox, segm) or just bbox.
        class_names (list[str] or tuple[str]): A list of class names.
        score_thr (float): The threshold to visualize the bboxes and masks.
        fig_size (tuple): Figure size of the pyplot figure.
        out_file (str, optional): If specified, the visualization result will
            be written to the out file instead of shown in a window.
    """
    img = show_result(
        img, result, class_names, score_thr=score_thr, show=False)
    plt.figure(figsize=fig_size)
    plt.savefig(mmcv.bgr2rgb(img), outfile)

config_file = '../configs/siam_polarmask/siampolar_r50.py'
checkpoint_file = '../work_dirs/siam_polarmask_r50/epoch_12.pth'
model = init_detector(config_file, checkpoint_file, device='cuda:0')

imgs = sorted(glob.glob('../data/DAVIS/JPEGImages/480p/bear/*jpg'))
print(imgs)
img_refer = '../data/DAVIS/JPEGImages/480p/bear/00000.jpg'
bbox = np.array([96, 214, 369, 221])
for img in imgs:
    result = inference_tracker(model, img, img_refer, bbox)
    save_result_pyplot(img, result, model.CLASSES, os.path.join('./', img))
    print("save {}".format(os.path.join('./', img)))
