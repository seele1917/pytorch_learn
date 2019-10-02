import sys
import os
import glob
import dlib
import cv2
import shutil
from scraping import get_member_name

root_path = './keyaki_member_data'
phase = 'valid'
targets = get_member_name().ruby_roman
target = targets[13]
print(target)

target_path = root_path + '/%s/%s/*.*' %(phase, target)
file_path_list = []
for path in glob.glob(target_path):
    file_path_list.append(path)

save_path = root_path + '_edited/' + phase + '/'+target+'/%d%04d.jpg'
os.makedirs(save_path.rsplit('/', 1)[0], exist_ok=True)
os.makedirs('./trash/'+target, exist_ok=True)

face_detector = dlib.get_frontal_face_detector()

for i, file_path in enumerate(file_path_list):
    img = cv2.imread(file_path)
    cv2.imshow('show image', img)
    k = cv2.waitKey()
    if chr(k) == 'd':
        shutil.move(file_path, './trash/'+target)
        continue
    
    detected_faces = face_detector(img, 1)
    
    for j, face_rect in enumerate(detected_faces):
        # cv2.rectangle(img, tuple([face_rect.left(), face_rect.top()]), tuple([face_rect.right(), face_rect.bottom()]), (0, 0, 255), thickness=2)
        top = face_rect.top()
        left = face_rect.left()
        bottom = face_rect.bottom()
        right = face_rect.right()
        if face_rect.top() < 0:
            top = 0
        if face_rect.left() < 0:
            left = 0

        img_edited = img[top:bottom, left:right]
        # print(file_path, img_edited, face_rect)
        cv2.imshow('show image', img_edited)
        k = cv2.waitKey()
        if chr(k) == 'a':  
            cv2.imwrite(save_path %(j, i), img_edited)

cv2.destroyAllWindows()
