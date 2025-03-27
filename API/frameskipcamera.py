# import streamlit as st
# import cv2, queue, threading, time
# import requests, os, re
# import numpy as np
# from insightface.app import FaceAnalysis

# # Bufferless VideoCapture
# class VideoCapture:
#     def __init__(self, name):
#         self.cap = cv2.VideoCapture(name, cv2.CAP_DSHOW)  # Use DirectShow backend
#         self.q = queue.Queue()
#         t = threading.Thread(target=self._reader)
#         t.daemon = True
#         t.start()

#     def _reader(self):
#         while True:
#             ret, frame = self.cap.read()
#             if not ret:
#                 break
#             if not self.q.empty():
#                 try:
#                     self.q.get_nowait()  # discard previous (unprocessed) frame
#                 except queue.Empty:
#                     pass
#             self.q.put(frame)

#     def read(self):
#         return self.q.get()


# # Initialize the VideoCapture
# video_capture = VideoCapture(0)

# # Initialize ArcFace
# app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
# app.prepare(ctx_id=0, det_size=(640, 640))

# # Load known faces
# known_face_embeddings = []
# known_face_names = []
# known_faces_filenames = []

# cwd = os.getcwd()
# fpath = os.path.join(cwd, "assets", "img", "users")
# walks = os.walk(fpath)

# for dirpath, dirnames, filenames in walks:
#     known_faces_filenames.extend(filenames)
#     break

# def normalize_embedding(embedding):
#     norm = np.linalg.norm(embedding)
#     return embedding / norm if norm > 0 else embedding

# for filename in known_faces_filenames:
#     face = cv2.imread(os.path.join(fpath, filename))
#     faces = app.get(face)

#     if faces:
#         embedding = normalize_embedding(faces[0].embedding)
#         print(f"Generated embedding for {filename}: {embedding[:5]}...")  # Print a sample of the embedding
#         known_face_names.append(re.sub("[0-9]", '', filename[:-4]))
#         known_face_embeddings.append(embedding)
#     else:
#         print(f"No face found in {filename}")

# print("Known faces loaded:", known_face_names)

# face_names = []
# process_this_frame = True

# # Define tolerance parameter
# tolerance = st.slider('Set Tolerance', 0.1, 1.0, 0.6)

# # Streamlit app
# st.title("Real-time Face Recognition")
# run = st.checkbox('Run')

# FRAME_WINDOW = st.image([])

# while run:
#     frame = video_capture.read()
#     frame = cv2.resize(frame, (640, 640))

#     faces = app.get(frame)  # Run face detection first
#     if faces:  # Only process the frame if faces are detected
#         face_names = []
#         json_to_export = {}

#         for face in faces:
#             name = "Unknown"
#             face_embedding = normalize_embedding(face.embedding)
#             face_distances = [np.linalg.norm(known_embedding - face_embedding) for known_embedding in known_face_embeddings]
            
#             # Debugging
#             print(f"Distances: {face_distances}")
            
#             if face_distances:
#                 best_match_index = np.argmin(face_distances)
#                 print(f"Best match index: {best_match_index}, Distance: {face_distances[best_match_index]}")
                
#                 if face_distances[best_match_index] <= tolerance:
#                     name = known_face_names[best_match_index]
#                     json_to_export['name'] = name
#                     json_to_export['hour'] = f'{time.localtime().tm_hour}:{time.localtime().tm_min}'
#                     json_to_export['date'] = f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}'
#                     json_to_export['picture_array'] = frame.tolist()

#                     r = requests.post(url='http://127.0.0.1:8000/receive_data', json=json_to_export)
#                     print("Status: ", r.status_code)

#             face_names.append(name)
#         print("Detected face names:", face_names)

#         # Draw boxes and names only when faces are detected
#         for face, name in zip(faces, face_names):
#             box = face.bbox.astype(int)
#             cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
#             font = cv2.FONT_HERSHEY_DUPLEX
#             cv2.putText(frame, name, (box[0] + 6, box[3] - 6), font, 1.0, (255, 255, 255), 1)
        
#         # Update the frame only when faces are detected
#         FRAME_WINDOW.image(frame[:, :, ::-1])
#     else:
#         print("No faces detected; skipping frame update.")

# st.write("Stopped")


# import streamlit as st
# import cv2, queue, threading, time
# import requests, os, re
# import numpy as np
# from insightface.app import FaceAnalysis

# # Bufferless VideoCapture with IP Camera support
# class VideoCapture:
#     def __init__(self, source):
#         self.cap = cv2.VideoCapture(source, cv2.CAP_DSHOW if isinstance(source, int) else cv2.CAP_FFMPEG)  # Use DirectShow for webcams, FFMPEG for RTSP
#         self.q = queue.Queue()
#         t = threading.Thread(target=self._reader)
#         t.daemon = True
#         t.start()

#     def _reader(self):
#         while True:
#             ret, frame = self.cap.read()
#             if not ret:
#                 break
#             if not self.q.empty():
#                 try:
#                     self.q.get_nowait()  # discard previous (unprocessed) frame
#                 except queue.Empty:
#                     pass
#             self.q.put(frame)

#     def read(self):
#         return self.q.get()

# # IP camera credentials and URL setup
# username = "admin"
# password = "HgtlKKD%40%232022"
# ip = "103.140.18.68"
# port = 554
# channel = "1"
# stream = "01"
# rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/Streaming/channels/{channel}{stream}"

# # Streamlit app setup
# st.title("Real-time Face Recognition")
# camera_source = st.selectbox('Select Camera Source', ['Webcam', 'IP Camera'])
# run = st.checkbox('Run')

# # Initialize the VideoCapture based on user selection
# video_capture = VideoCapture(0 if camera_source == 'Webcam' else rtsp_url)

# # Initialize ArcFace
# app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
# app.prepare(ctx_id=0, det_size=(640, 640))

# # Load known faces
# known_face_embeddings = []
# known_face_names = []
# known_faces_filenames = []

# cwd = os.getcwd()
# fpath = os.path.join(cwd, "assets", "img", "users")
# walks = os.walk(fpath)

# for dirpath, dirnames, filenames in walks:
#     known_faces_filenames.extend(filenames)
#     break

# def normalize_embedding(embedding):
#     norm = np.linalg.norm(embedding)
#     return embedding / norm if norm > 0 else embedding

# for filename in known_faces_filenames:
#     face = cv2.imread(os.path.join(fpath, filename))
#     faces = app.get(face)

#     if faces:
#         embedding = normalize_embedding(faces[0].embedding)
#         print(f"Generated embedding for {filename}: {embedding[:5]}...")  # Print a sample of the embedding
#         known_face_names.append(re.sub("[0-9]", '', filename[:-4]))
#         known_face_embeddings.append(embedding)
#     else:
#         print(f"No face found in {filename}")

# print("Known faces loaded:", known_face_names)

# face_names = []
# process_this_frame = True

# # Define tolerance parameter
# tolerance = st.slider('Set Tolerance', 0.1, 1.0, 0.6)

# FRAME_WINDOW = st.image([])

# while run:
#     frame = video_capture.read()
#     frame = cv2.resize(frame, (640, 640))

#     faces = app.get(frame)  # Run face detection first
#     if faces:  # Only process the frame if faces are detected
#         face_names = []
#         json_to_export = {}

#         for face in faces:
#             name = "Unknown"
#             face_embedding = normalize_embedding(face.embedding)
#             face_distances = [np.linalg.norm(known_embedding - face_embedding) for known_embedding in known_face_embeddings]
            
#             # Debugging
#             print(f"Distances: {face_distances}")
            
#             if face_distances:
#                 best_match_index = np.argmin(face_distances)
#                 print(f"Best match index: {best_match_index}, Distance: {face_distances[best_match_index]}")
                
#                 if face_distances[best_match_index] <= tolerance:
#                     name = known_face_names[best_match_index]
#                     json_to_export['name'] = name
#                     json_to_export['hour'] = f'{time.localtime().tm_hour}:{time.localtime().tm_min}'
#                     json_to_export['date'] = f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}'
#                     json_to_export['picture_array'] = frame.tolist()

#                     r = requests.post(url='http://127.0.0.1:8000/receive_data', json=json_to_export)
#                     print("Status: ", r.status_code)

#             face_names.append(name)
#         print("Detected face names:", face_names)

#         # Draw boxes and names only when faces are detected
#         for face, name in zip(faces, face_names):
#             box = face.bbox.astype(int)
#             cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
#             font = cv2.FONT_HERSHEY_DUPLEX
#             cv2.putText(frame, name, (box[0] + 6, box[3] - 6), font, 1.0, (255, 255, 255), 1)
        
#         # Update the frame only when faces are detected
#         FRAME_WINDOW.image(frame[:, :, ::-1])
#     else:
#         print("No faces detected; skipping frame update.")

# st.write("Stopped")


# import streamlit as st
# import cv2, queue, threading, time
# import requests, os, re
# import numpy as np
# from insightface.app import FaceAnalysis
# import onnxruntime

# # Bufferless VideoCapture for IP Camera
# class VideoCapture:
#     def __init__(self, source):
#         # Use FFMPEG backend for RTSP streams
#         self.cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
#         self.q = queue.Queue()
#         t = threading.Thread(target=self._reader)
#         t.daemon = True
#         t.start()

#     def _reader(self):
#         while True:
#             ret, frame = self.cap.read()
#             if not ret:
#                 print("Failed to grab frame.")
#                 break
#             if not self.q.empty():
#                 try:
#                     self.q.get_nowait()  # discard previous (unprocessed) frame
#                 except queue.Empty:
#                     pass
#             self.q.put(frame)

#     def read(self):
#         if not self.q.empty():
#             return self.q.get()
#         else:
#             print("No frames in queue.")
#             return None

# # IP camera credentials and URL setup
# username = "admin"
# password = "HgtlKKD@#2022"
# ip = "103.140.18.68"
# port = 554
# channel = "1"
# stream = "01"
# rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/Streaming/channels/{channel}{stream}"

# # Initialize the VideoCapture with IP camera
# video_capture = VideoCapture(rtsp_url)

# # Initialize ArcFace
# app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
# app.prepare(ctx_id=0, det_size=(640, 640))

# # Load known faces
# known_face_embeddings = []
# known_face_names = []
# known_faces_filenames = []

# cwd = os.getcwd()
# fpath = os.path.join(cwd, "assets", "img", "users")
# walks = os.walk(fpath)

# for dirpath, dirnames, filenames in walks:
#     known_faces_filenames.extend(filenames)
#     break

# def normalize_embedding(embedding):
#     norm = np.linalg.norm(embedding)
#     return embedding / norm if norm > 0 else embedding

# for filename in known_faces_filenames:
#     face = cv2.imread(os.path.join(fpath, filename))
#     faces = app.get(face)

#     if faces:
#         embedding = normalize_embedding(faces[0].embedding)
#         print(f"Generated embedding for {filename}: {embedding[:5]}...")  # Print a sample of the embedding
#         known_face_names.append(re.sub("[0-9]", '', filename[:-4]))
#         known_face_embeddings.append(embedding)
#     else:
#         print(f"No face found in {filename}")

# print("Known faces loaded:", known_face_names)

# face_names = []
# process_this_frame = True

# # Set the tolerance value
# tolerance = 1.00

# # Streamlit app setup
# st.title("Real-time Face Recognition")
# run = st.checkbox('Run')

# FRAME_WINDOW = st.image([])

# while run:
#     frame = video_capture.read()
#     if frame is not None:
#         # Resize the frame to fit display requirements
#         frame = cv2.resize(frame, (640, 640))

#         faces = app.get(frame)  # Run face detection first
#         if faces:  # Only process the frame if faces are detected
#             face_names = []
#             json_to_export = {}

#             for face in faces:
#                 name = "Unknown"
#                 face_embedding = normalize_embedding(face.embedding)
#                 face_distances = [np.linalg.norm(known_embedding - face_embedding) for known_embedding in known_face_embeddings]

#                 # Debugging
#                 print(f"Distances: {face_distances}")

#                 if face_distances:
#                     best_match_index = np.argmin(face_distances)
#                     print(f"Best match index: {best_match_index}, Distance: {face_distances[best_match_index]}")

#                     if face_distances[best_match_index] <= tolerance:
#                         name = known_face_names[best_match_index]
#                         json_to_export['name'] = name
#                         json_to_export['hour'] = f'{time.localtime().tm_hour}:{time.localtime().tm_min}'
#                         json_to_export['date'] = f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}'
#                         json_to_export['picture_array'] = frame.tolist()

#                         r = requests.post(url='http://127.0.0.1:8000/receive_data', json=json_to_export)
#                         print("Status: ", r.status_code)

#                 face_names.append(name)
#             print("Detected face names:", face_names)

#             # Draw boxes and names only when faces are detected
#             for face, name in zip(faces, face_names):
#                 box = face.bbox.astype(int)
#                 cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
#                 font = cv2.FONT_HERSHEY_DUPLEX
#                 cv2.putText(frame, name, (box[0] + 6, box[3] - 6), font, 1.0, (255, 255, 255), 1)

#             # Update the frame only when faces are detected
#             FRAME_WINDOW.image(frame[:, :, ::-1])  # Convert BGR to RGB for Streamlit display
#         else:
#             print("No faces detected; skipping frame update.")
#             # Display the frame even if no faces are detected
#             FRAME_WINDOW.image(frame[:, :, ::-1])
#     else:
#         st.write("No frame available from IP camera.")

# st.write("Stopped")


# import streamlit as st
# import cv2, queue, threading, time, asyncio
# import requests, os
# import numpy as np
# from insightface.app import FaceAnalysis
# from pymongo import MongoClient

# # MongoDB Connection
# MONGO_URI = os.getenv('db_url')
# client = MongoClient(MONGO_URI)
# db = client["Face_Recognitions"]
# collection = db["face_embeddings"]

# known_face_embeddings = []
# known_face_names = []

# # Load face embeddings from MongoDB
# stored_faces_count = collection.count_documents({})
# if stored_faces_count > 0:
#     for face in collection.find({}):
#         known_face_names.append(face["name"])
#         known_face_embeddings.append(np.array(face["embedding"]))
#     print(f"Loaded {stored_faces_count} face embeddings from MongoDB.")
# else:
#     print("No stored embeddings found in MongoDB.")
#     exit()

# # Video Capture Class with Threading
# class VideoCapture:
#     def __init__(self, source=0):
#         self.cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
#         if not self.cap.isOpened():
#             st.error("Error: Unable to open RTSP stream.")
#             return
#         self.q = queue.Queue()
#         self.running = True
#         t = threading.Thread(target=self._reader, daemon=True)
#         t.start()

#     def _reader(self):
#         while self.running:
#             ret, frame = self.cap.read()
#             if not ret:
#                 st.error("Error: Failed to read frame from RTSP stream.")
#                 self.running = False
#                 break
#             if not self.q.empty():
#                 self.q.get_nowait()
#             self.q.put(frame)

#     def read(self):
#         if hasattr(self, 'q') and not self.q.empty():
#             return self.q.get()
#         return None

#     def release(self):
#         self.running = False
#         self.cap.release()

# # Update with your RTSP camera URL
# username = "admin"
# password = "HgtlKKD%40%232022"
# ip = "103.140.18.68"
# port = 554
# channel = "1"
# stream = "01"
# rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/Streaming/channels/{channel}{stream}" 

# video_capture = VideoCapture(rtsp_url)

# # Initialize ArcFace Model
# app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])  
# app.prepare(ctx_id=0, det_size=(320, 320))

# # Streamlit UI
# st.title("Real-time Face Recognition")
# run = st.checkbox('Run')
# FRAME_WINDOW = st.empty()
# tolerance = 1.00

# # Face Processing Function (Sync, Not Async)
# def process_faces():
#     global run
#     while run:
#         frame = video_capture.read()
#         if frame is None:
#             st.warning("Waiting for video feed...")
#             continue

#         frame = cv2.resize(frame, (320, 320))  
#         faces = app.get(frame)
#         face_names = []

#         for face in faces:
#             name = "Unknown"
#             face_embedding = face.embedding / np.linalg.norm(face.embedding)

#             # Compare with known faces
#             if known_face_embeddings:
#                 face_distances = np.linalg.norm(np.array(known_face_embeddings) - face_embedding, axis=1)
#                 best_match_index = np.argmin(face_distances)
#                 if face_distances[best_match_index] <= tolerance:
#                     name = known_face_names[best_match_index]

#                     # Prepare JSON for API
#                     json_to_export = {
#                         'name': name,
#                         'hour': f'{time.localtime().tm_hour}:{time.localtime().tm_min}',
#                         'date': f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}',
#                         'picture_array': frame.tolist()
#                     }

#                     # Send data to API (async call inside thread)
#                     threading.Thread(target=send_data, args=(json_to_export,)).start()

#             face_names.append(name)

#             # Draw Bounding Box
#             box = face.bbox.astype(int)
#             cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
#             cv2.putText(frame, name, (box[0] + 6, box[3] - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

#         FRAME_WINDOW.image(frame[:, :, ::-1], channels="RGB")

# # Function to Send Data to API
# def send_data(data):
#     try:
#         response = requests.post('http://127.0.0.1:8000/receive_data', json=data)
#         print("API Status:", response.status_code)
#     except Exception as e:
#         print("Error sending data:", e)

# # Start Processing
# if run:
#     process_faces()
# else:
#     video_capture.release()
#     st.write("Camera stopped.")



import streamlit as st
import cv2, queue, threading, time, asyncio
import requests, os, re
import numpy as np
from insightface.app import FaceAnalysis
# import onnxruntime
from pymongo import MongoClient
from dotenv import load_dotenv
 
load_dotenv()


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
st.title("Real-time Face Recognition")
run = st.checkbox('Run')
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
        response = await asyncio.to_thread(requests.post, 'http://127.0.0.1:8000/receive_data', json=data)
        print("API Status:", response.status_code)
    except Exception as e:
        print("Error sending data:", e)

# Start the Face Processing Loop
if run:
    asyncio.run(process_faces())

st.write("Stopped")
