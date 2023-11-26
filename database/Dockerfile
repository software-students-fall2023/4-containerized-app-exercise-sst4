FROM mongo:latest
EXPOSE 27017
RUN python -m unittest ./tests/*
CMD ["mongod", "db.py"]