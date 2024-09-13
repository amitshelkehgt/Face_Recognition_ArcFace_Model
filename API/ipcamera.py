import cv2
import numpy as np

# move to .env later
# username = "Nimbleio"
# password = "Nimble@#2024"
# ip = "103.140.18.67"
username = "admin"
password = "HgtlKKD%40%232022" #"HgtlKKD@#2022"
ip = "103.140.18.68"
port = 554
channel = "1"
stream = "01"

# https://supportusa.hikvision.com/support/solutions/articles/17000129064-how-do-i-get-my-rtsp-stream-
# rtsp://<username>:<password>@<IP address of device>:<RTSP port>/Streaming/channels/<channel number><stream number>
url = f"rtsp://{username}:{password}@{ip}:{port}/Streaming/channels/{channel}{stream}"
# rtsp://admin:HgtlKKD@#2022@103.140.18.68/Streaming/channels/101
# rtsp://<IP address of device>:<RTSP port>/Streaming/channels/<channel number><stream number>
# url = f"rtsp://{ip}:{port}/Streaming/channels/{channel}{stream}"
cap = cv2.VideoCapture(url)

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()