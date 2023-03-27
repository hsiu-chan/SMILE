FROM python:3.9.0
 
WORKDIR /app
 
ADD . /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
 
CMD python main.py
