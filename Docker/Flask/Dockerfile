FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN pip install --upgrade pip && pip install pymongo
WORKDIR /app 
COPY ./app /app
EXPOSE 5001
ENTRYPOINT ["python"]
CMD ["database.py"]