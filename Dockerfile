FROM python:3.12.3-slim-bullseye
# copy all the files in this dir to image
# execute install script
RUN apt-get update
RUN apt-get install tesseract-ocr libtesseract-dev tesseract-ocr-eng -y
RUN apt-get install python3-opencv -y
COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir img2pdf
COPY . /root/webapp/
WORKDIR /root/webapp/
CMD ["python", "web/flask_app.py"]