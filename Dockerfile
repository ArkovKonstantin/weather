FROM python:3
ADD . /home/weather
WORKDIR /home/weather
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python3 run.py
