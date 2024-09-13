# from fastapi import FastAPI, HTTPException, UploadFile, File, Form
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pymongo import MongoClient
# import os
# import cv2
# import numpy as np
# import re
# from datetime import datetime

# # Initialize FastAPI app
# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust the allowed origins as needed
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # MongoDB configuration
# MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/Face_Recognitions')
# client = MongoClient(MONGO_URI)
# db = client.get_database('Face_Recognitions')  # Specify the database name explicitly

# # Collection name
# EMP_IMAGES_COLLECTION = 'Emp_Images'
# emp_images = db.get_collection(EMP_IMAGES_COLLECTION)

# # File path
# FILE_PATH = os.path.dirname(os.path.realpath(__file__))

# # Helper function to save images
# def save_image(path, image_array):
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     cv2.imwrite(path, np.array(image_array))

# # Receive data endpoint
# @app.post("/receive_data")
# async def receive_data(json_data: dict):
#     try:
#         # Check if the user exists for today
#         user_today = emp_images.find_one({
#             'date': json_data['date'],
#             'name': json_data['name']
#         })

#         if user_today:
#             print('User IN')
#             image_path = f"{FILE_PATH}/assets/img/{json_data['date']}/{json_data['name']}/departure.jpg"
#             save_image(image_path, json_data['picture_array'])

#             # Update user in MongoDB
#             emp_images.update_one(
#                 {'_id': user_today['_id']},
#                 {'$set': {'departure_time': json_data['hour'], 'departure_picture': image_path}}
#             )
#         else:
#             print('User OUT')
#             image_path = f"{FILE_PATH}/assets/img/history/{json_data['date']}/{json_data['name']}/arrival.jpg"
#             save_image(image_path, json_data['picture_array'])

#             # Insert new user document in MongoDB
#             emp_images.insert_one({
#                 'name': json_data['name'],
#                 'date': json_data['date'],
#                 'arrival_time': json_data['hour'],
#                 'arrival_picture': image_path
#             })

#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail="Internal Server Error")

#     return JSONResponse(content=json_data)

# # Get employee endpoint
# @app.get("/get_employee/{name}")
# async def get_employee(name: str):
#     try:
#         # Query MongoDB for user information
#         result = list(emp_images.find({'name': name}))

#         if result:
#             # Format data for response
#             answer_to_send = [{k: str(v) for k, v in user.items()} for user in result]
#         else:
#             answer_to_send = {'error': 'User not found...'}

#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail="Internal Server Error")

#     return JSONResponse(content=answer_to_send)

# # Add employee endpoint
# @app.post("/add_employee")
# async def add_employee(image: UploadFile = File(...), nameOfEmployee: str = Form(...)):
#     try:
#         # Store it in the folder of the known faces
#         file_path = os.path.join(f"assets/img/users/{nameOfEmployee}.jpg")
#         with open(file_path, "wb") as f:
#             f.write(await image.read())
#         answer = 'New employee successfully added'
#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail="Error while adding new employee. Please try later...")

#     return JSONResponse(content=answer)

# # Update employee endpoint
# @app.put("/update_employee/{name}")
# async def update_employee(name: str, new_name: str = Form(None), image: UploadFile = File(None)):
#     try:
#         update_fields = {}

#         # Update name
#         if new_name:
#             update_fields['name'] = new_name

#         # Update image
#         if image:
#             # Remove old image file
#             old_file_path = os.path.join(f'assets/img/users/{name}.jpg')
#             if os.path.exists(old_file_path):
#                 os.remove(old_file_path)

#             # Save new image file
#             new_file_path = os.path.join(f'assets/img/users/{new_name or name}.jpg')
#             with open(new_file_path, "wb") as f:
#                 f.write(await image.read())
#             update_fields['image_path'] = new_file_path

#         # Update MongoDB document
#         if update_fields:
#             emp_images.update_many({'name': name}, {'$set': update_fields})

#         # If name is updated, change file path for historical data as well
#         if new_name:
#             # Update historical image paths
#             emp_images.update_many(
#                 {'name': name},
#                 {'$set': {'name': new_name}}
#             )

#         answer = 'Employee information successfully updated'
#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail="Error while updating employee. Please try later...")

#     return JSONResponse(content=answer)

# # Delete employee endpoint
# @app.delete("/delete_employee/{name}")
# async def delete_employee(name: str):
#     try:
#         # Remove employee picture from user folder
#         file_path = os.path.join(f'assets/img/users/{name}.jpg')
#         os.remove(file_path)
#         answer = 'Employee successfully removed'
#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail="Error while deleting employee. Please try later...")
 
#     return JSONResponse(content=answer)

# # Run the FastAPI app
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=5000, log_level="debug")


# from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from pymongo import MongoClient
# import os
# import cv2
# import numpy as np
# import re
# from datetime import datetime

# # Initialize FastAPI app
# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust the allowed origins as needed
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # MongoDB configuration
# MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/Face_Recognitions')
# client = MongoClient(MONGO_URI)
# db = client.get_database('Face_Recognitions')  # Specify the database name explicitly

# # Collection name
# EMP_IMAGES_COLLECTION = 'Emp_Images'
# emp_images = db.get_collection(EMP_IMAGES_COLLECTION)

# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent

# # app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

# # File path
# FILE_PATH = os.path.dirname(os.path.realpath(__file__))
# app.mount("/assets", StaticFiles(directory=os.path.join(FILE_PATH, "assets")), name="static")

# # Static files and templates
# # app.mount("/static", StaticFiles(directory="static"), name="static")
# # templates = Jinja2Templates(directory="/templates")

# # Helper function to save images
# def save_image(path, image_array):
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     cv2.imwrite(path, np.array(image_array))

# # Serve the Jinja2 template
# @app.get("/")
# async def get_index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# # Receive data endpoint
# @app.post("/receive_data")
# async def receive_data(json_data: dict):
#     try:
#         # Check if the user exists for today
#         name = json_data['name'].lower()
#         user_today = emp_images.find_one({
#             'date': json_data['date'],
#             'name': name
#         })

#         if user_today:
#             print('User IN')
#             image_path = f"{FILE_PATH}/assets/img/{json_data['date']}/{json_data['name']}/departure.jpg"
#             save_image(image_path, json_data['picture_array'])

#             # Update user in MongoDB
#             emp_images.update_one(
#                 {'_id': user_today['_id']},
#                 {'$set': {'departure_time': json_data['hour'], 'departure_picture': image_path}}
#             )
#         else:
#             print('User OUT')
#             image_path = f"{FILE_PATH}/assets/img/history/{json_data['date']}/{json_data['name']}/arrival.jpg"
#             save_image(image_path, json_data['picture_array'])

#             # Insert new user document in MongoDB
#             emp_images.insert_one({
#                 'name': json_data['name'],
#                 'date': json_data['date'],
#                 'arrival_time': json_data['hour'],
#                 'arrival_picture': image_path
#             })

#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail="Internal Server Error")

#     return JSONResponse(content=json_data)

# # Get employee endpoint
# @app.get("/get_employee/{name}")
# async def get_employee(name: str):
#     try:
#         # Query MongoDB for user information
#         result = list(emp_images.find({'name': name}))
#         print(result)

#         if result:
#             # Format data for response
#             answer_to_send = [{k: str(v) for k, v in user.items()} for user in result]
#         else:
#             answer_to_send = {'error': 'User not found...'}

#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail="Internal Server Error")

#     return JSONResponse(content=answer_to_send)

# # Add employee endpoint
# @app.post("/add_employee")
# async def add_employee(image: UploadFile = File(...), nameOfEmployee: str = Form(...)):
#     try:
#         # Store it in the folder of the known faces
#         file_path = os.path.join(f"assets/img/users/{nameOfEmployee}.jpg")
#         with open(file_path, "wb") as f:
#             f.write(await image.read())
#         answer = 'New employee successfully added'
#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail="Error while adding new employee. Please try later...")

#     return JSONResponse(content=answer)

# # Update employee endpoint
# @app.put("/update_employee/{name}")
# async def update_employee(name: str, new_name: str = Form(None), image: UploadFile = File(None)):
#     try:
#         update_fields = {}

#         # Update name
#         if new_name:
#             update_fields['name'] = new_name

#         # Update image
#         if image:
#             # Remove old image file
#             old_file_path = os.path.join(f'assets/img/users/{name}.jpg')
#             if os.path.exists(old_file_path):
#                 os.remove(old_file_path)

#             # Save new image file
#             new_file_path = os.path.join(f'assets/img/users/{new_name or name}.jpg')
#             with open(new_file_path, "wb") as f:
#                 f.write(await image.read())
#             update_fields['image_path'] = new_file_path

#         # Update MongoDB document
#         if update_fields:
#             emp_images.update_many({'name': name}, {'$set': update_fields})

#         # If name is updated, change file path for historical data as well
#         if new_name:
#             # Update historical image paths
#             emp_images.update_many(
#                 {'name': name},
#                 {'$set': {'name': new_name}}
#             )

#         answer = 'Employee information successfully updated'
#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail="Error while updating employee. Please try later...")

#     return JSONResponse(content=answer)

# # Get employee list endpoint
# @app.get("/get_employee_list")
# async def get_employee_list():
#     try:
#         employee_list = {}
#         walk_count = 0
        
#         # Iterate over user folder to get employee list
#         for file_name in os.listdir(os.path.join(FILE_PATH, "assets", "img", "users")):
#             name = re.findall(r"(.*)\.jpg", file_name)
#             if name:
#                 employee_list[walk_count] = name[0]
#             walk_count += 1

#         return JSONResponse(content=employee_list)
    
#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail="Failed to retrieve employee list")

# # Delete employee endpoint
# @app.delete("/delete_employee/{name}")
# async def delete_employee(name: str):
#     try:
#         # file_path = os.path.join(f'/assets/img/users/{name}.jpg')
#         file_path = os.path.abspath(os.path.join('assets', 'img', 'users', f'{name}.jpg'))
#         print(file_path)
#         if os.path.exists(file_path):
#             os.remove(file_path)
#             answer = 'Employee successfully removed'
#         else:
#             answer = 'Employee photo not found'
#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail="Error while deleting employee. Please try later...")
#     return JSONResponse(content={"message": answer})

# # Run the FastAPI app
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8000, log_level="debug")


from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import os
import cv2
import numpy as np
import re
from datetime import datetime
 
# Initialize FastAPI app
app = FastAPI()
 
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust the allowed origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/Face_Recognitions')
client = MongoClient(MONGO_URI)
db = client.get_database('Face_Recognitions')  # Specify the database name explicitly
 
# Collection name
EMP_IMAGES_COLLECTION = 'Emp_Images'
emp_images = db.get_collection(EMP_IMAGES_COLLECTION)
 
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
 
# app.mount("/static", StaticFiles(directory="static", html=True), name="static")
 
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))
 
# File path
FILE_PATH = os.path.dirname(os.path.realpath(__file__))
app.mount("/assets", StaticFiles(directory=os.path.join(FILE_PATH, "assets")), name="static")
 
# Static files and templates
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="/templates")
 
# Helper function to save images
def save_image(path, image_array):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv2.imwrite(path, np.array(image_array))
 
# Serve the Jinja2 template
@app.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
 
# Receive data endpoint
@app.post("/receive_data")
async def receive_data(json_data: dict):
    try:
        # Check if the user exists for today
        name = json_data['name'].lower()
        user_today = emp_images.find_one({
            'date': json_data['date'],
            'name': name
        })
 
        if user_today:
            print('User IN')
            image_path = f"{FILE_PATH}/assets/img/{json_data['date']}/{json_data['name']}/departure.jpg"
            save_image(image_path, json_data['picture_array'])
 
            # Update user in MongoDB
            emp_images.update_one(
                {'_id': user_today['_id']},
                {'$set': {'departure_time': json_data['hour'], 'departure_picture': image_path}}
            )
        else:
            print('User OUT')
            image_path = f"{FILE_PATH}/assets/img/history/{json_data['date']}/{json_data['name']}/arrival.jpg"
            save_image(image_path, json_data['picture_array'])
 
            # Insert new user document in MongoDB
            emp_images.insert_one({
                'name': json_data['name'].lower(),
                'date': json_data['date'],
                'arrival_time': json_data['hour'],
                'arrival_picture': image_path
            })
 
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
 
    return JSONResponse(content=json_data)
 
# Get employee endpoint
@app.get("/get_employee/{name}")
async def get_employee(name: str):
    try:
        # Query MongoDB for user information
        result = list(emp_images.find({'name': name}))
        print(result)
 
        if result:
            # Format data for response
            answer_to_send = [{k: str(v) for k, v in user.items()} for user in result]
        else:
            answer_to_send = {'error': 'User not found...'}
 
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
 
    return JSONResponse(content=answer_to_send)
 
# Add employee endpoint
@app.post("/add_employee")
async def add_employee(image: UploadFile = File(...), nameOfEmployee: str = Form(...)):
    try:
        # Store it in the folder of the known faces
        file_path = os.path.join(f"assets/img/users/{nameOfEmployee}.jpg")
        with open(file_path, "wb") as f:
            f.write(await image.read())
        answer = 'New employee successfully added'
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Error while adding new employee. Please try later...")
 
    return JSONResponse(content=answer)
 
# Update employee endpoint
@app.put("/update_employee/{name}")
async def update_employee(name: str, new_name: str = Form(None), image: UploadFile = File(None)):
    try:
        update_fields = {}
 
        # Update name
        if new_name:
            update_fields['name'] = new_name
 
        # Update image
        if image:
            # Remove old image file
            old_file_path = os.path.join(f'assets/img/users/{name}.jpg')
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
 
            # Save new image file
            new_file_path = os.path.join(f'assets/img/users/{new_name or name}.jpg')
            with open(new_file_path, "wb") as f:
                f.write(await image.read())
            update_fields['image_path'] = new_file_path
 
        # Update MongoDB document
        if update_fields:
            emp_images.update_many({'name': name}, {'$set': update_fields})
 
        # If name is updated, change file path for historical data as well
        if new_name:
            # Update historical image paths
            emp_images.update_many(
                {'name': name},
                {'$set': {'name': new_name}}
            )
 
        answer = 'Employee information successfully updated'
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Error while updating employee. Please try later...")
 
    return JSONResponse(content=answer)
 
# Get employee list endpoint
@app.get("/get_employee_list")
async def get_employee_list():
    try:
        employee_list = {}
        walk_count = 0
       
        # Iterate over user folder to get employee list
        for file_name in os.listdir(os.path.join(FILE_PATH, "assets", "img", "users")):
            name = re.findall(r"(.*)\.jpg", file_name)
            if name:
                employee_list[walk_count] = name[0]
            walk_count += 1
 
        return JSONResponse(content=employee_list)
   
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve employee list")
 
# Delete employee endpoint
@app.delete("/delete_employee/{name}")
async def delete_employee(name: str):
    try:
        # file_path = os.path.join(f'/assets/img/users/{name}.jpg')
        file_path = os.path.abspath(os.path.join('assets', 'img', 'users', f'{name}.jpg'))
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            answer = 'Employee successfully removed'
        else:
            answer = 'Employee photo not found'
           
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Error while deleting employee. Please try later...")
    return JSONResponse(content={"message": answer})
 
# Run the FastAPI app
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level="debug")