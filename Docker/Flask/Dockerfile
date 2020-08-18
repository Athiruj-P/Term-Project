FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN pip install --upgrade pip && pip install pymongo && pip install zope.interface
RUN mkdir database_file
WORKDIR /app 
COPY ./app /app
EXPOSE 5001
ENTRYPOINT ["python"]
# CMD ["database.py"]
CMD ["main_api.py"]