import streamlit as st
import cv2, queue, threading, time, asyncio
import requests, os, re
import numpy as np
from insightface.app import FaceAnalysis
# import onnxruntime
from pymongo import MongoClient
from dotenv import load_dotenv
 
load_dotenv()


 
st.set_page_config(
    page_title="Face Recognition",
    page_icon="👋",
    layout="wide"
)
 
# def get_public_url():
#     return "https://camera.kodefast.com"
 
# st.markdown(f"[Open Camera Page]({get_public_url()})")

# MongoDB Connection (Load embeddings once)
MONGO_URI = os.getenv('db_url')
client = MongoClient(MONGO_URI)
db = client["Face_Recognitions"]
collection = db["face_embeddings"]

# known_face_embeddings = []
# known_face_names = []

# stored_faces_count = collection.count_documents({})
# if stored_faces_count > 0:
#     for face in collection.find({}):
#         known_face_names.append(face["name"])
#         known_face_embeddings.append(np.array(face["embedding"]))
#     print(f"Loaded {stored_faces_count} face embeddings from MongoDB.")
# else:
#     print("No stored embeddings found in MongoDB.")
#     exit()

# Video Capture Class with Threading
class VideoCapture:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source,cv2.CAP_FFMPEG)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                self.q.get_nowait()
            self.q.put(frame)

    def read(self):
        return self.q.get()


# Update with your RTSP camera URL
username = "admin"
password = "HgtlKKD%40%232022"
ip = "103.140.18.68"
port = 554
channel = "1"
stream = "01"

# Create the RTSP URL
rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/Streaming/channels/{channel}{stream}" 
print(rtsp_url)      

# Start video capture
video_capture = VideoCapture(rtsp_url)

# Initialize ArcFace Model with ONNX Runtime
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])  #'CUDAExecutionProvider'
app.prepare(ctx_id=0, det_size=(640, 640))  # Smaller size for faster processing

known_face_embeddings = []
known_face_names = []

stored_faces_count = collection.count_documents({})
if stored_faces_count > 0:
    for face in collection.find({}):
        known_face_names.append(face["name"])
        known_face_embeddings.append(np.array(face["embedding"]))
    print(f"Loaded {stored_faces_count} face embeddings from MongoDB.")
else:
    print("No stored embeddings found in MongoDB.")
    exit()

# Streamlit UI
# st.title("Real-time Face Recognition")
# run = st.checkbox('Run')
FRAME_WINDOW = st.empty()
tolerance = 1.0

# Async Face Processing Function
async def process_faces():
    global run
    while run:
        frame = video_capture.read()
        if frame is None:
            st.write("Camera connection failed.")
            break

        frame = cv2.resize(frame, (640, 640))  # Reduced resolution for efficiency
        faces = app.get(frame)
        face_names = []
        json_to_export = {}

        for face in faces:
            name = "Unknown"
            face_embedding = face.embedding / np.linalg.norm(face.embedding)

            # Faster Distance Calculation using NumPy
            if known_face_embeddings:
                face_distances = np.linalg.norm(np.array(known_face_embeddings) - face_embedding, axis=1)
                best_match_index = np.argmin(face_distances)
                if face_distances[best_match_index] <= tolerance:
                    name = known_face_names[best_match_index]

                    # Prepare JSON for API
                    json_to_export = {
                        'name': name,
                        'hour': f'{time.localtime().tm_hour}:{time.localtime().tm_min}',
                        'date': f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}',
                        'picture_array': frame.tolist()
                    }

                    # Send data to API asynchronously
                    asyncio.create_task(send_data(json_to_export))

            face_names.append(name)

            # Draw Bounding Box
            box = face.bbox.astype(int)
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            cv2.putText(frame, name, (box[0] + 6, box[3] - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        FRAME_WINDOW.image(frame[:, :, ::-1])
        await asyncio.sleep(1)  # Process frame every second

# Async Function to Send Data to API
async def send_data(data):
    try:
        response = await asyncio.to_thread(requests.post, 'https://camera.kodefast.com/', json=data)
        print("API Status:", response.status_code)
    except Exception as e:
        print("Error sending data:", e)

# Start the Face Processing Loop
asyncio.run(process_faces())

st.write("Stopped")
