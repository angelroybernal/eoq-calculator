FROM debian:buster

RUN apt-get update && \
    apt-get install python3 python3-pip \
    python3-setuptools \ 
    -y --no-install-recommends &&\
    rm -rf /var/lib/apt/lists/*

COPY ./ /opt/code

WORKDIR /opt/code

RUN python3 -m pip install -r requirements.txt

EXPOSE 8501

CMD ["/usr/local/bin/streamlit", "run", "eoq_calculator.py"]