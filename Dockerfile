FROM python:3.9
WORKDIR /home/app

COPY requirements.txt .

RUN apt update -qq
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]