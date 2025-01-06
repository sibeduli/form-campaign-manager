FROM python:3.9-slim

WORKDIR /home/abdul-personal-project/form-campaign-manager
ADD . /home/abdul-personal-project/form-campaign-manager

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
