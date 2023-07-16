FROM python:3.11.1

WORKDIR /heyling_tst

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8000