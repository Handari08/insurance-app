FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --shell /usr/sbin/nologin app
COPY --chown=app:app . .

USER app

EXPOSE 8501

CMD ["bash", "-c", "uvicorn app:app --host 127.0.0.1 --port 8000 & api_pid=$!; streamlit run ui.py --server.address 0.0.0.0 --server.port 8501 & ui_pid=$!; trap 'kill \"$api_pid\" \"$ui_pid\" 2>/dev/null || true' TERM INT; wait -n \"$api_pid\" \"$ui_pid\"; status=$?; kill \"$api_pid\" \"$ui_pid\" 2>/dev/null || true; wait; exit \"$status\""]