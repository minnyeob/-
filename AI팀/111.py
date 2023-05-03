import cv2

# 이미지 파일을 읽어옵니다.
image = cv2.imread('C:\sdafsdf\cap.jpg')

# 이미지의 크기를 출력합니다.
height, width, channels = image.shape
print("이미지 크기: {} x {} pixels, 채널 수: {}".format(width, height, channels))

# 이미지를 회색조로 변환합니다.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 블러링을 적용합니다.
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 가장자리를 검출합니다.
edges = cv2.Canny(blurred, 50, 150)

# 가장자리 이미지를 출력합니다.
cv2.imshow('Edges', edges)

# 윤곽선을 검출합니다.
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print("검출된 윤곽선 수: {}".format(len(contours)))

# 윤곽선을 그리고 세모를 인식합니다.
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

    if len(approx) == 3:
        cv2.drawContours(image, [approx], 0, (0, 255, 0), 3)

        # 인식된 세모의 중심 좌표를 계산합니다.
        M = cv2.moments(approx)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # 세모의 중심 좌표를 출력합니다.
        cv2.putText(image, "Triangle", (cx - 40, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 결과를 출력합니다.
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
