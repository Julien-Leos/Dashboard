FROM python:3.7-alpine
ADD . /server
WORKDIR /server/
ENV FLASK_APP server/app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt
CMD ["flask", "run"]