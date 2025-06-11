FROM Ubuntu:22.04

# setting up environment
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app
COPY . /app

# install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
    

# install python packages
RUN pip3 install -r requirements.txt

# set the entrypoint
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]
