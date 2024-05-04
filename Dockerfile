FROM node:21-alpine AS frontend-build
WORKDIR /tmp/build
COPY ./frontend/ .
RUN npm install && npm run build

FROM python:3.9-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update && apt install -y tshark

COPY ./backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./backend/ ./backend

COPY --from=frontend-build /tmp/build/dist/ ./backend/static/

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
