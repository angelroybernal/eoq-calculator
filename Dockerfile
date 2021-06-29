FROM python:3.7.9

COPY ./ /opt/code

WORKDIR /opt/code

RUN python -m pip install -r requirements.txt

EXPOSE 8501

CMD ["/usr/local/bin/streamlit", "run", "eoq_calculator.py"]
