FROM sconecuratedimages/kubernetes:python-3.7.3-alpine3.10-scone4.2
#FROM python:3.7

#RUN mkdir /app
#ADD . /app/
ADD . /


RUN pip install -r requirements.txt
WORKDIR /app
EXPOSE 5000
CMD ["python3", "app.py"]