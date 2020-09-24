FROM tiangolo/uwsgi-nginx-flask:python3.8

# RUN pip install --upgrade pip && pip install pymongo && pip install zope.interface
RUN pip install --upgrade pip
RUN mkdir database_file
WORKDIR /app 
COPY ./app /app
RUN pip install -r ./requirements.txt
# RUN pip install flask-jwt-extended && pip install pytz && pip install memory-profiler
RUN pip install flask-jwt-extended && pip install pytz
EXPOSE 5001
# RUN python -m memory_profiler main_api.py
ENTRYPOINT ["python"]
# CMD ["database.py"]
CMD ["main_api.py"]