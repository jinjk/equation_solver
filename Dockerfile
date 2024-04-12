FROM python:3.12.3-slim-bullseye
# copy all the files in this dir to image
# execute install script
COPY . .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "web/flask_app.py"]