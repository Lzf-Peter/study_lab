import cv2
import os
import xml.etree.ElementTree as ET
import numpy as np
file_dir = 'egg'
xml_path = 'chicken_images/xml/' + file_dir
jpg_path = 'chicken_images/images/' + file_dir
save_path = 'chicken_images/chicken_images_augment/' + file_dir
if not os.path.exists(save_path):
    os.mkdir(save_path)
xml_files = os.listdir(xml_path)
scale = [0.9,1.1,1.2,1.3,1.4,1.5]
for xml_file in xml_files:
    if xml_file[-3:] != 'xml':
        continue
    tree = ET.parse(os.path.join(xml_path,xml_file))
    root = tree.getroot()
    for n in root:
        if n.tag == 'filename':
            file_name = n.text
            if xml_file[:-4] != n.text[:-4]:
                ima = cv2.imread(os.path.join(jpg_path, xml_file[:-4] + '.jpg'))
            else:
                ima = cv2.imread(os.path.join(jpg_path, n.text))
            print(n.text)

        if n.tag == 'object':
            for m in n:
                if m.tag == 'bndbox':
                    for l in m:
                        if l.tag == 'xmin':
                            xmin = int(l.text)
                        if l.tag == 'xmax':
                            xmax = int(l.text)
                        if l.tag == 'ymin':
                            ymin = int(l.text)
                        if l.tag == 'ymax':
                            ymax = int(l.text)
    bbox_w = xmax - xmin
    bbox_h = ymax - ymin
    lenth = int(max(bbox_h,bbox_w)/2)

    y_center = int((ymax+ymin)/2)
    x_center = int((xmax+xmin)/2)
    for i in range(len(scale)):
        ymin = y_center - int(lenth*scale[i])
        ymax = y_center + int(lenth*scale[i])
        xmin = x_center - int(lenth*scale[i])
        xmax = x_center + int(lenth*scale[i])
        # print(file_name)
        # print(ymin, ymax, xmin, xmax)
        ymin_chazhi = 0
        xmin_chazhi = 0
        ymax_chazhi = 0
        xmax_chazhi = 0
        if ymin < 0:
            ymin_chazhi = 0 - ymin
            ymin = 0
        if xmin < 0:
            xmin_chazhi = 0 - xmin
            xmin = 0
        if ymax > ima.shape[0]:
            ymax_chazhi = ymax - ima.shape[0]
            ymax = ima.shape[0]
        if xmax > ima.shape[1]:
            xmax_chazhi = xmax - ima.shape[1]
            xmax = ima.shape[1]

        # cropped_img = ima

        cropped_img = ima[int(ymin):int(ymax),int(xmin):int(xmax)]
        cropped_img = cv2.copyMakeBorder(cropped_img, ymin_chazhi, ymax_chazhi,xmin_chazhi, xmax_chazhi, cv2.BORDER_REPLICATE)

        if cropped_img.shape[1] > cropped_img.shape[0]:
            a = int((cropped_img.shape[1] - cropped_img.shape[0])/2)
            cropped_img = cv2.copyMakeBorder(cropped_img, a, a, 0, 0, cv2.BORDER_REPLICATE)
        if cropped_img.shape[1] < cropped_img.shape[0]:
            a = int((cropped_img.shape[0] - cropped_img.shape[1])/2)
            cropped_img = cv2.copyMakeBorder(cropped_img, 0, 0, a, a, cv2.BORDER_REPLICATE)
        if cropped_img.shape[1] != cropped_img.shape[0]:
            print(cropped_img.shape[1],cropped_img.shape[0])
        # cv2.imshow('aaaa',cropped_img)
        # cv2.waitKey()
        file_name1 =  file_name[:-4] +'scale%.1f.jpg'%scale[i]


        # print(file_name1)
        # cv2.imwrite(os.path.join(save_path,file_name1),cropped_img)
        w = cropped_img.shape[0]
        h = w
        center = (w //2 , h // 2)
        for j in range(3):
            # angle = np.random.randint(-30,30)
            # M = cv2.getRotationMatrix2D(center, angle, 1.0)
            file_name2 = file_name1[:-4] +'_%d.jpg'%j
            # rotated_img = cv2.warpAffine(cropped_img, M, (w, h))
            # cv2.imwrite(os.path.join(save_path,file_name2),cropped_img)