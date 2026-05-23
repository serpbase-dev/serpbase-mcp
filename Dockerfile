FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .

ENV SERPBASE_BASE_URL=https://api.serpbase.dev
CMD ["serpbase-mcp"]
