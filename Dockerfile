FROM python:3.12.3-slim-bullseye
# copy all the files in this dir to image
COPY . .
# execute install script
RUN pip install --no-cache-dir -r requirements.txt