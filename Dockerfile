FROM python:3.12
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "./main.py" ]
