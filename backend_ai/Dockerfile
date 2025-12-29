FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .

RUN pip install fastapi uvicorn langchain langchain-community
COPY . .

CMD ["python", "backend/ai.py"]