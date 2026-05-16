FROM python:3.11-slim
WORKDIR /app
RUN useradd -u 1001 -m appuser
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser . .
USER appuser
ENV FLASK_ENV=production
ENV PORT=5000
ENV DB_PATH=/tmp/tasks.db
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"
CMD ["python", "src/main.py"]
