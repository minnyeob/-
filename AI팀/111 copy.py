import cv2

# 카메라 객체 생성
cap = cv2.VideoCapture(0)

# 카메라 프레임 사이즈 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 캡처 버튼을 누르면 이미지 캡처
def capture_image():
    ret, frame = cap.read()
    cv2.imwrite('captured_image.jpg', frame)
    print("Captured image saved!")
    
# ESC 키를 누를 때까지 반복
while True:
    ret, frame = cap.read()
    cv2.imshow('Camera', frame)
    
    # 키 입력 대기
    key = cv2.waitKey(1)
    
    # c 키를 누르면 이미지 캡처
    if key == ord('c'):
        capture_image()
        
    # ESC 키를 누르면 종료
    elif key == 27:
        break
    

# 객체 해제
cap.release()
cv2.destroyAllWindows()
