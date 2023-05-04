from lib.Base64 import path_to_base64
from skimage import io
import numpy as np
#from PIL import Image
import cv2
import mediapipe as mp
#from segment_anything 
from .segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import os
import json
import matplotlib.pyplot as plt
import sys

print(os.path.dirname(os.path.abspath(__file__)))


sys.path.append("..")
sam_checkpoint = f"{os.path.dirname(os.path.abspath(__file__))}/sam_vit_h_4b8939.pth"
model_type = "default"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(
    #device='mps'
)

predictor = SamPredictor(sam)
"""mask_generator = SamAutomaticMaskGenerator(model=sam,
    points_per_side=32,
    pred_iou_thresh=0.86,
    stability_score_thresh=0.92,
    crop_n_layers=1,
    crop_n_points_downscale_factor=2,
    min_mask_region_area=20,)"""


def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)

class SMILE:
    def __init__(self,input_path,out_dir):
        self.input_path=input_path 
        self.out_dir=out_dir


        img=io.imread(input_path)
        h, w ,d= img.shape
        self.img=cv2.resize(img, (512, int(512*h/w)), interpolation=cv2.INTER_AREA)
        self.img=cv2.cvtColor(self.img,cv2.COLOR_RGB2BGR)
        self.shape=self.img.shape

        self.mouse=[]
        self.box=[]
        self.boximg=[]
        self.result=[]

        
        
        self.cuted=[]
        self.mask={}
        self.out_path=out_dir
        self.output=f"output.{input_path.split('.')[-1]}"
        self.base64=''

        pass

    def set_predictor(self):
        try:
            self.box[1]
        except:
            self.find_mouse()
        predictor.set_image(self.boximg)
    
    def predict(point):
        masks, scores, logits = predictor.predict(
        point_coords=np.array(point),
        point_labels=np.array([1]*len(point)),
        multimask_output=True,
        )
        sorted_mask = sorted(list(zip(masks, scores)), key=(lambda x: x[1]), reverse=True)
        mask=sorted_mask[0][0]
        mask=np.array(mask, dtype='uint8')

        #plt.imshow(self.boximg)
        #show_mask(mask[0], plt.gca())
        #plt.axis('off')
        #plt.savefig(self.output)
        #self.base64=path_to_base64(self.output)

        contours, hierarchy = cv2.findContours(mask*255, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        pol=contours[0].reshape(-1,2)



    
        return pol,f'{sorted_mask[0][1]:.3f}'
    
        
        

    """def gen_mask(self):
        try:
            self.box[1]
        except:
            self.find_mouse()
        
        self.masks = mask_generator.generate(self.img[self.box[2]-5:self.box[3]+5,self.box[0]-5:self.box[1]+5])
        self.masks  = sorted(self.masks , key=(lambda x: x['area']), reverse=True)"""



    def cut(self, pol):
        pol=np.array([pol], np.int32)
        #遮片
        mask=np.zeros(self.img.shape[:2], np.uint8)
        #多邊形填上白色
        cv2.polylines(mask, [pol], isClosed=True,color=(255,255,255), thickness=1)
        cv2.fillPoly(mask,pol,255)
        
        dst=cv2.bitwise_and(self.img, self.img, mask=mask)
        return dst
    
    def find_mouse(self):
        h, w, d = self.img.shape
        mp_face_detection = mp.solutions.face_detection
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh=mp_face_mesh.FaceMesh(
            min_detection_confidence=0.2,
            min_tracking_confidence=0.2)
    #嘴巴
        mouse=[62,96,89,179,86,15,316,403,319,325,292,407,272,271,268,12,38,41,42,183]
        lip=[78,95,88,178,87,14,317,402,318,324,308,415,310,311,312,13,82,81,80,191]#嘴唇
    
        #########################openCV辨識嘴 #########################
        RGBim = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(RGBim)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                #for index in mouse:
                for index in lip:
                    x = int(face_landmarks.landmark[index].x * w)
                    y = int(face_landmarks.landmark[index].y * h)
                    self.mouse.append([x,y])
        self.mouse=np.array(self.mouse)
        
        """mousep_b=[]
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for index in mouse:
                    x = int(face_landmarks.landmark[index].x * w)
                    y = int(face_landmarks.landmark[index].y * h)
                    mousep_b.append([x,y])
        mousep_b=np.array(mousep_b)"""

        
        #找 marker
        umos=min(self.mouse[:,1])#嘴上緣
        dmos=max(self.mouse[:,1])#嘴下緣
        lmos=min(self.mouse[:,0])#嘴左緣
        rmos=max(self.mouse[:,0])#嘴右緣
        wmos=rmos-lmos#嘴寬
        hmos=dmos-umos#嘴高
        mmos=[int((lmos+rmos)/2),int((umos+dmos)/2)]#嘴中心

        self.box=np.array([lmos,rmos,umos,dmos])
        self.boximg=self.img[self.box[2]-5:self.box[3]+5,self.box[0]-5:self.box[1]+5]

        cv2.imwrite(self.output
                    ,self.boximg)
        self.base64=path_to_base64(self.output)

        
        
        
        ##self.cuted=self.cut( self.mouse)
        
        return self.box
    
    def show_box(self):
        path=f"{self.out_dir}/{self.input_path.split('/')[-1]}"

        cv2.imwrite(path
                    ,self.boximg)
        return path_to_base64(path)
    
    


    


        


    


    def show_anns(self):
        import matplotlib.pyplot as plt

        if len(self.masks) == 0:
            return

        ax = plt.gca()
        ax.set_autoscale_on(False)
        polygons = []
        color = []
        figsize=self.box[1]-self.box[0]
        for ann in self.mask:
            #print(ann)
            if (ann['area']>figsize/10) ^ (ann['area']<figsize/200):
                continue

            
            m = ann['segmentation']
            img = np.ones((m.shape[0], m.shape[1], 3))
            color_mask = np.random.random((1, 3)).tolist()[0]
            for i in range(3):
                img[:,:,i] = color_mask[i]
            ax.imshow(np.dstack((img, m*0.35)))
        plt.axis('off')

        path=f"{self.out_dir}/ooouuuttt{self.input_path.split('.')[-1]}"
        plt.savefig(path)
        return path_to_base64(path)
        #plt.show()




def SMILE_0(path):
    ########圖像處理########
    def cut(img, pol):
        pol=np.array([pol], np.int32)
        #遮片
        mask=np.zeros(img.shape[:2], np.uint8)
        #多邊形填上白色
        cv2.polylines(mask, [pol], isClosed=True,color=(255,255,255), thickness=1)
        cv2.fillPoly(mask,pol,255)
        
        dst=cv2.bitwise_and(img, img, mask=mask)
        return dst


    img=io.imread(path)
    h, w ,d= img.shape
    img=cv2.resize(img, (1000, int(1000*h/w)), interpolation=cv2.INTER_AREA)
    pol=np.array([[110,200],[300,400],[160,50]])
    #pol= np.array([[200, 200], [300, 100], [300, 200], [200, 200], [200, 250]], np.int32)
    img=cut(img,pol)



    result = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    #######輸出#####
    out_path='output.jpg'
    cv2.imwrite(out_path, img)
    
    
    
    return path_to_base64(out_path)
    #return 'a'    
    
