import os


class Config:
    

    data_folder = "data_face_recognation"
    root_directory = f"{os.getcwd()}/{data_folder}"
    
    

            
    
    rec_path = {
        'images_for_training':f"{root_directory}/images/",
        'haarcascade_frontalface_path':f"{root_directory}/haarcascade_frontalface_default.xml",
        'trainner_file':f"{root_directory}/classifiers/trainner.xml",
    }
    
    
    
   

                

                
                    
                


