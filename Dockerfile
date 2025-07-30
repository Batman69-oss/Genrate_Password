FROM alpine:3.20
RUN apk update
RUN apk add python3
RUN apk add py3-pip
WORKDIR	/Genrate_Pass
COPY requirements.txt .
COPY flask-app.py .
RUN python3 -m venv myvenv
ENV PATH="/Genrate_Pass/myvenv/bin:$PATH"
RUN pip install -r requirements.txt
CMD ["sh", "-c", " source myvenv/bin/activate ;  python flask-app.py"]

