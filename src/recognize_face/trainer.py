import numpy as np
from PIL import Image
import os, cv2

from .recognize_config import Config
from telega import Telega

config = Config()

class Trainer():


        def train_classifer_all(self):
                path = config.rec_path['images_for_training']
                                
                faces = []
                ids = []
                labels = []
                label_to_id = {}
                current_id = 0 
 
                for label in os.listdir(path):
                        label_path = os.path.join(path, label)
                        
                        if os.path.isdir(label_path):
                                label_to_id[label] = current_id  
                                labels.append(label)
                                current_id += 1 
                        
                        
                        for pic in os.listdir(label_path):
                                
                                pic_path = os.path.join(label_path,pic)
                                print(pic_path)
                                
                                img = cv2.imread(pic_path)
                                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                
                                faces.append(gray)
                                ids.append(label_to_id[label]) 
                                
                                
                
                    
                ids = np.array(ids)
                
                clf = cv2.face.LBPHFaceRecognizer_create()
                clf.train(faces, ids)
                
                
                clf.write(config.rec_path['trainner_file'])
                
                return labels     
        
        
        def get_labels(self) -> list:
                
                path = os.path.join(config.rec_path['images_for_training'])
                labels = []
                
                for label in os.listdir(path):
                        labels.append(label)
                
                return labels
        
        def set_camera(self,vs):
                self.vs = vs;
                
        
        def set_telega(self,telega : Telega):
                self.telega = telega        
        
                     

        def create_images(self,name:str,num_images=310):
                path = f"{config.rec_path['images_for_training']}/{name}"
                detector = cv2.CascadeClassifier(config.rec_path['haarcascade_frontalface_path'])
                
                start_num = 0
                
                if not os.path.exists(path):
                        os.makedirs(path)
                else:
                        print('Directory Already Created')
                
                        start_num = len(os.listdir(path))
                        num_images += start_num
                        
                
     
                count_img=start_num
                
                while count_img < num_images:
                
                        img = self.vs.get_frame()
                        new_img = None
                        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
                        for x, y, w, h in face:
                                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
                                cv2.putText(img, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                                cv2.putText(img, str(str(count_img)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                                new_img = img[y:y+h, x:x+w]
                        
                        
                 
                        
                        
                        key = cv2.waitKey(1) & 0xFF
                        
                        if new_img is not None:
                                cv2.imwrite(str(path+"/"+str(count_img)+name+".jpg"), new_img)
                                print(count_img)
                                count_img += 1
                                
                                cv2.imwrite(f'{os.getcwd()}/Files/fr.jpg',img)
                                img = open(f'{os.getcwd()}/Files/fr.jpg','rb')
            
             
                                
                        
                        
                        if key == ord("q") or key == 27 :
                                break
                