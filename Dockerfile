FROM alpine:3.19
RUN apk add --no-cache nmap nmap-scripts python3
COPY src/ /app/
WORKDIR /app
ENTRYPOINT ["python3", "main.py"]