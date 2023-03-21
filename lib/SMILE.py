from lib.Base64 import path_to_base64
from skimage import io
import numpy as np
#from PIL import Image
import cv2
def SMILE(path):
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
    
