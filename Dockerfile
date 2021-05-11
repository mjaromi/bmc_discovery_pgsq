FROM python:3.9.5-alpine3.13

COPY . .

RUN pip3 install -r requirements && chmod +x app.py

ENTRYPOINT [ "/app.py" ]