FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install Flask requests
EXPOSE 10000
CMD ["flask", "run", "--host", "0.0.0.0", "-p", "10000"]
