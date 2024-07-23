FROM python:3.8-slim


WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn fpdf

EXPOSE 80

ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]