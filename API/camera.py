# import streamlit as st
# import cv2, queue, threading, time
# import requests, os, re
# import numpy as np
# from insightface.app import FaceAnalysis
# from insightface.model_zoo import get_model

# # Bufferless VideoCapture
# class VideoCapture:
#     def __init__(self, name):
#         self.cap = cv2.VideoCapture(name, cv2.CAP_DSHOW)  # Use DirectShow backend
#         self.q = queue.Queue()
#         t = threading.Thread(target=self._reader)
#         t.daemon = True
#         t.start()

#     # Read frames as soon as they are available, keeping only the most recent one
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

#     if process_this_frame:
#         faces = app.get(frame)
#         face_names = []
#         json_to_export = {}

#         for face in faces:
#             name = "Unknown"
#             face_embedding = normalize_embedding(face.embedding)  # Normalize the face embedding
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
#         print("Detected face names:", face_names)  # Debugging print    

#     for face, name in zip(faces, face_names):
#         box = face.bbox.astype(int)
#         cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
#         print("Detected Face Box:", box)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(frame, name, (box[0] + 6, box[3] - 6), font, 1.0, (255, 255, 255), 1)

#     FRAME_WINDOW.image(frame[:, :, ::-1])

# st.write("Stopped")


import streamlit as st
import cv2, queue, threading, time
import requests, os, re
import numpy as np
from insightface.app import FaceAnalysis


# Bufferless VideoCapture for RTSP stream
class VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)  # Initialize the RTSP stream
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # Read frames as soon as they are available, keeping only the most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


# Update with your RTSP camera URL
username = "admin"
password = "HgtlKKD%40%232022"  # URL encoded characters like %40 for '@'
ip = "103.140.18.68"
port = 554
channel = "1"
stream = "01"

# Create the RTSP URL
rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/Streaming/channels/{channel}{stream}"
video_capture = VideoCapture(rtsp_url)

# Initialize ArcFace
app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

# Load known faces
known_face_embeddings = []
known_face_names = []
known_faces_filenames = []

cwd = os.getcwd()
fpath = os.path.join(cwd, "assets", "img", "users")
walks = os.walk(fpath)

for dirpath, dirnames, filenames in walks:
    known_faces_filenames.extend(filenames)
    break

def normalize_embedding(embedding):
    norm = np.linalg.norm(embedding)
    return embedding / norm if norm > 0 else embedding

for filename in known_faces_filenames:
    face = cv2.imread(os.path.join(fpath, filename))
    faces = app.get(face)

    if faces:
        embedding = normalize_embedding(faces[0].embedding)
        print(f"Generated embedding for {filename}: {embedding[:5]}...")  # Print a sample of the embedding
        known_face_names.append(re.sub("[0-9]", '', filename[:-4]))
        known_face_embeddings.append(embedding)
    else:
        print(f"No face found in {filename}")

print("Known faces loaded:", known_face_names)

face_names = []
process_this_frame = True

# Define tolerance parameter
tolerance = st.slider('Set Tolerance', 0.1, 1.0, 0.6)

# Streamlit app
st.title("Real-time Face Recognition")
run = st.checkbox('Run')

FRAME_WINDOW = st.image([])

while run:
    frame = video_capture.read()
    if frame is None:  # Check if frame is read correctly
        st.write("Failed to retrieve frame from the camera. Check your connection.")
        break
    
    frame = cv2.resize(frame, (640, 640))

    if process_this_frame:
        faces = app.get(frame)
        face_names = []
        json_to_export = {}

        for face in faces:
            name = "Unknown"
            face_embedding = normalize_embedding(face.embedding)  # Normalize the face embedding
            face_distances = [np.linalg.norm(known_embedding - face_embedding) for known_embedding in known_face_embeddings]

            # Debugging
            print(f"Distances: {face_distances}")

            if face_distances:
                best_match_index = np.argmin(face_distances)
                print(f"Best match index: {best_match_index}, Distance: {face_distances[best_match_index]}")

                if face_distances[best_match_index] <= tolerance:
                    name = known_face_names[best_match_index]
                    json_to_export['name'] = name
                    json_to_export['hour'] = f'{time.localtime().tm_hour}:{time.localtime().tm_min}'
                    json_to_export['date'] = f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}'
                    json_to_export['picture_array'] = frame.tolist()

                    r = requests.post(url='http://127.0.0.1:8000/receive_data', json=json_to_export)
                    print("Status: ", r.status_code)

            face_names.append(name)
        print("Detected face names:", face_names)  # Debugging print    

    for face, name in zip(faces, face_names):
        box = face.bbox.astype(int)
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
        print("Detected Face Box:", box)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (box[0] + 6, box[3] - 6), font, 1.0, (255, 255, 255), 1)

    FRAME_WINDOW.image(frame[:, :, ::-1])

st.write("Stopped")
