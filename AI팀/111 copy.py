import cv2

# 카메라를 연결합니다.
cap = cv2.VideoCapture(0)

while True:
    # 카메라로부터 이미지를 읽어옵니다.
    ret, frame = cap.read()

    # 이미지 크기를 조절합니다.
    resized = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # 이미지를 회색조로 변환합니다.
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # 블러링을 적용합니다.
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 가장자리를 검출합니다.
    edges = cv2.Canny(blurred, 50, 150)

    # 윤곽선을 검출합니다.
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 윤곽선을 그리고 세모와 원을 인식합니다.
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(approx) == 3:
            cv2.drawContours(resized, [approx], 0, (0, 255, 0), 3)

            # 인식된 세모의 중심 좌표를 계산합니다.
            M = cv2.moments(approx)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # 세모의 중심 좌표를 출력합니다.
            cv2.putText(resized, "Triangle", (cx - 40, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        elif len(approx) > 7:
            (x,y),radius = cv2.minEnclosingCircle(contour)
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(resized,center,radius,(0,255,0),2)
            cv2.putText(resized, "Circle", (int(x) - 40, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 결과를 출력합니다.
    cv2.imshow('Image', resized)

    # 100ms 대기합니다.
    key = cv2.waitKey(100)

    # ESC 키를 누르면 종료합니다.
    if key == 27:
        break

# 카메라와 윈도우를 해제합니다.
cap.release()
cv2.destroyAllWindows()