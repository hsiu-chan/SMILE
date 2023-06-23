import numpy as np
import cv2
import matplotlib.pyplot as plt


class PolygonSet:
    def __init__(self):
        self.polygons=[]

    def append(self,pol):
        pol=np.array([pol], np.int32)
        for e in self.polygons:
            if PolygonSet.isSame(e,pol):
                return
        self.polygons.append(pol)
    def clear(self):
        self.polygons=[]


    def isSame(pol1,pol2):
        def pol_center(pol):
            return (np.mean(pol[:,0]),np.mean(pol[:,1]))

        def pol_to_mask(pol):
            pol=np.array([pol], np.int32)
            mask=np.zeros([1000,1000], np.uint8)
            cv2.polylines(mask, [pol], isClosed=True,color=1, thickness=1)
            cv2.fillPoly(mask,pol,1)
            return mask
        
        if (np.mean(pol1[:,0])-np.mean(pol2[:,0]))**2+(np.mean(pol1[:,1])-np.mean(pol2[:,1]))**2>18:
            return False

        xor=(pol_to_mask(pol1)+pol_to_mask(pol2))%2
        #show_mask(xor)
        return sum(xor.flatten())/(PolygonSet.polygon_area(pol1)+PolygonSet.polygon_area(pol2))<0.1
    
    def polygon_area(points):
        area = 0
        q = points[-1]
        for p in points:
            area += p[0] * q[1] - p[1] * q[0]
            q = p
        return int(abs(area / 2))
    
    def show_mask(mask):
        w,h=mask.shape
        new=mask.reshape(h, w, 1)*1

        color = np.array([30/255, 144/255, 255/255, 0.6])
        h, w = mask.shape[-2:]
        mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
        plt.gca().imshow(mask_image)
    
    def mask_to_pol(mask):
        mask=np.array(mask, dtype='uint8')

        contours, hierarchy = cv2.findContours(mask*255, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        h,w=mask.shape

        pol=contours[0].reshape(-1,2)
        pol=[ [round(p[0]/w,3),round(p[1]/h,3)]  for p in pol]
        return pol
    
