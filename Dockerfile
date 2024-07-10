FROM selenium/standalone-chrome:latest

USER root

# installa Python, pip, certs ofl
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    unzip \
    ca-certificates \ 
    && update-ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

COPY main.py /app/main.py
COPY src /app/src
COPY chromedriver/linux64/chromedriver /app/chromedriver/chromedriver


# directory fyrir ársreikninga undir data með eiganda seluser
RUN mkdir /app/data && chown seluser:seluser /app/data

USER seluser

# Entrypoint fyrir breytur úr argparser
ENTRYPOINT ["python3", "main.py"]