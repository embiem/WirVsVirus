FROM python:3.8-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

CMD ["wirvsvirus", "api"]