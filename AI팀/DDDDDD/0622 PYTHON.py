
import cv2
import serial
import time

# 시리얼 통신 설정
arduino = serial.Serial('COM10', 9600, timeout=1)  # COM 포트 번호와 timeout 설정

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

    # 윤곽선을 그리고 네모와 원을 인식합니다.
    num_circles = 0
    if len(contours) == 0:  # 물체가 없을 경우
        cv2.putText(resized, "No object", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # 아두이노로 신호를 보냅니다.
        arduino.write(b'0')
        time.sleep(0.1)  # 0.1초 대기
        if num_circles > 1:
            # 아두이노로 '3'을 전송합니다.
            arduino.write(b'3')
            time.sleep(0.1)  # 0.1초 대기
            break  # 프로그램을 종료합니다.
    else:
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)  # 근사치 정확도 조정 (0.03 -> 0.04)

            if len(approx) == 4 and cv2.isContourConvex(approx):
                area = cv2.contourArea(approx)
                if area > 100:
                    cv2.drawContours(resized, [approx], 0, (0, 255, 0), 2)

                    # 인식된 네모의 중심 좌표를 계산합니다.
                    M = cv2.moments(approx)
                    if M['m00'] != 0:
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        # 네모의 중심 좌표를 출력합니다.
                        cv2.putText(resized, "Square", (cx - 40, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        if area > 500:
                            surface_status = 0
                        else:
                            surface_status = 1

                        # 표면 상태를 출력합니다.
                        cv2.putText(resized, f"Surface: {surface_status}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 255, 0), 2)
                        # 아두이노로 신호를 보냅니다.
                        arduino.write(b'1')
                        time.sleep(0.1)  # 0.1초 대기
                        if num_circles > 1:
                            cv2.putText(resized, "Defective", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                            # 아두이노로 '3'를 전송합니다.
                            arduino.write(b'3')
                            time.sleep(0.1)  # 0.1초 대기
                            break  # 프로그램을 종료합니다.

            elif len(approx) >= 8:  # 원의 근사치 정확도를 조정 (7 -> 8)
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                cv2.circle(resized, center, radius, (0, 255, 0), 2)
                cv2.putText(resized, "Circle", (int(x) - 40, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # Check if the circle has a hole
                if hierarchy[0] is not None:
                    # If the circle has a contour inside, it has a hole
                    hole = True
                else:
                    # If the circle doesn't have a contour inside, it doesn't have a hole
                    hole = False

                # Determine the surface status based on the presence of a hole
                if hole:
                    surface_status = 1  # Circle with a hole
                else:
                    surface_status = 0  # Circle without a hole

                num_circles += 1

                # Output the surface status
                cv2.putText(resized, f"Surface: {surface_status}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                            2)
                # 아두이노로 신호를 보냅니다.
                arduino.write(b'2')
                time.sleep(0.1)  # 0.1초 대기
                if num_circles > 1:
                    cv2.putText(resized, "Defective", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    # 아두이노로 '3'를 전송합니다.
                    arduino.write(b'3')
                    time.sleep(0.1)  # 0.1초 대기
                    break  # 프로그램을 종료합니다.

    # 결과를 출력합니다.
    cv2.imshow('Image', resized)

    # 100ms 대기합니다.
    key = cv2.waitKey(100)

    # ESC 키를 누르면 종료합니다.
    if key == 27:
        break

    # 아두이노로 3의 값이 전송되면 나머지 동작을 중지합니다.
    if arduino.read() == b'3':
        break

# 카메라와 윈도우를 해제합니다.
cap.release()
cv2.destroyAllWindows()