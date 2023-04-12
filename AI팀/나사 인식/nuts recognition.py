#//// 카메라 부분
###########################1주차####################
import cv2
import numpy as np

# 카메라 연결
cap = cv2.VideoCapture(0)

# 연결된 카메라에서 이미지 가져오기
while True:
    ret, frame = cap.read()

    # 가져온 이미지 처리
    # ...

    # 이미지 출력
    cv2.imshow('frame', frame)

    # 키 입력 대기
    if cv2.waitKey(1) & 0xFF == ord('m'):
        break

# 카메라 연결 해제
cap.release()

# 윈도우 창 닫기
cv2.destroyAllWindows()







#///// 길이 판별


img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
img = cv2.GaussianBlur(img, (5,5), 0)
ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
edges = cv2.Canny(thresh, 100, 200)

contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    if len(approx)==4:
        x,y,w,h = cv2.boundingRect(cnt)
        ratio = w / float(h)
        if ratio > 0.8 and ratio < 1.2:
            print('Type 1 Screw with length', w)
        elif ratio > 1.2:
            print('Type 2 Screw with length', w)








#////// 나사 수 판단

# 이미지 불러오기
img = cv2.imread('screws.jpg')

# Canny 엣지 검출
edges = cv2.Canny(img, 100, 200)

# Contour 찾기
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Contour의 면적 계산
areas = [cv2.contourArea(contour) for contour in contours]

# 나사 수 계산
screw_count = len(areas)

# 결과 출력
print(f"The number of screws is {screw_count}")










#//// 나사 수가 1개면 진행 2개 이상일 경우 다시 창고로 이동

import cv2
import numpy as np

# 이미지 불러오기
img = cv2.imread('screws.jpg')

# Canny 엣지 검출
edges = cv2.Canny(img, 100, 200)

# Contour 찾기
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Contour의 면적 계산
areas = [cv2.contourArea(contour) for contour in contours]

# 나사 수 계산
screw_count = len(areas)

# 나사 수에 따라서 다른 동작 수행
if screw_count == 1:
    print("There is only one screw")
else:
    print(f"There are {screw_count} screws")
    # 다시 되돌리는 동작 수행
    # ...





#///// 합체본(초안)


import cv2
import pytesseract
import re

# pytesseract 라이브러리의 OCR 엔진 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 이미지에서 나사 검출하는 함수
def detect_nuts(image):
    # 이미지를 회색조로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 이미지의 노이즈 제거
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 이미지 이진화
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # 이미지에서 윤곽선 검출
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 윤곽선에서 나사 검출
    nuts = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        if aspect_ratio >= 0.8 and aspect_ratio <= 1.2:
            nut = image[y:y+h, x:x+w]
            nuts.append(nut)
    
    return nuts

# 이미지에서 나사 개수, 길이, 수량 추출하는 함수
def extract_nuts_info(image):
    # 이미지에서 나사 검출
    nuts = detect_nuts(image)
    
    # 각 나사에서 길이와 수량 추출
    nut_lengths = []
    nut_quantities = []
    for nut in nuts:
        # 이미지에서 문자 추출
        nut_text = pytesseract.image_to_string(nut, config='--psm 6')
        
        # 나사 길이와 수량 추출
        nut_len_match = re.search(r'\d+mm', nut_text)
        if nut_len_match:
            nut_len = int(nut_len_match.group().replace('mm', ''))
            nut_lengths.append(nut_len)
        nut_qty_match = re.search(r'Qty \d+', nut_text)
        if nut_qty_match:
            nut_qty = int(nut_qty_match.group().replace('Qty ', ''))
            nut_quantities.append(nut_qty)
    
    # 나사 개수 추출
    num_nuts = len(nuts)
    




