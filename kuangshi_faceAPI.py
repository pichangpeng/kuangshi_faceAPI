import os
from glob import glob
from tqdm import tqdm
from PIL import Image, ImageDraw
import shutil
import requests
import base64


def getDetect(imagePath,url,api_key,api_secret,outPath):
    i=0
    imagePaths=glob(imagePath+"**.jpg",recursive=True) #默认图片格式为jpg格式，若为其他格式，将jpg修改成对应格式即可
    for path in tqdm(imagePaths):
        name=path.split("/")[-1]
        f = open(path,"rb") # 以二进制读取图片
        base64data = base64.b64encode(f.read())# 得到 byte 编码的数据
        base64data = str(base64data,'utf-8')# 重新编码数据
        payload={"api_key":api_key,"api_secret":api_secret,"image_base64":base64data}
        response=requests.post(url=url,data=payload)
        faces=response.json()
        while "error_message" in faces.keys():
            response=requests.post(url=url,data=payload)
            faces=response.json()
        faces=faces["faces"]
        if faces:
            i+=1
            img = Image.open(path)
            a = ImageDraw.ImageDraw(img)
            for face in faces:
                face_rectangle=face["face_rectangle"]
                y_min=face_rectangle["top"]
                x_min=face_rectangle["left"]
                x_max=x_min+face_rectangle["width"]
                y_max=y_min+face_rectangle["height"]
                a.rectangle(((x_min, y_max), (x_max, y_min)), fill=None, outline='red', width=2)
            img.save(outPath+"/detect/"+name)
        else:
            shutil.copy(imagePath+name,outPath+"/undetect/")
    print("检测图片数量:%d   未能检测图片数量:%d"%(i,len(imagePaths)-i))   

if __name__=="__main__":
    imagePath="./hand_dataset/images/"  #存储图片的文件夹路径（只包含需要做检测的图片,一定要以“/”结尾）
    url=url="https://api-cn.faceplusplus.com/facepp/v3/detect" #旷视科技提供的URL接口（不需要做修改）
    api_key="ixeDY8Gyv054pJwDoImwXsbyw9phavcd" #旷视科技帐号上的api_key(可自己到官方网站免费申请，或则直接用我的)
    api_secret="-hephbfyqseyry9kZruP0rILWz1hz6lK"#密钥（需和api_key搭配使用)
    outPath="./output" #输出图片的文件夹路径

    if not os.path.exists(outPath+"/detect/"): #存放检测出来的图片
        os.makedirs(outPath+"/detect/")
    if not os.path.exists(outPath+"/undetect/"): #存放未能检测出来的图片
        os.makedirs(outPath+"/undetect/")

    getDetect(imagePath,url,api_key,api_secret,outPath)