# DON'T CREATE IMAGE USING THIS CODE...
$ TRYING TO FIGURE OUT BEST PRACTICE TO DO THIS


FROM python:3.7

WORKDIR /app

COPY . /app


RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["quart"]
CMD ["./run.sh", "--host=0.0.0.0"]
