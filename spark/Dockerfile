FROM bitnami/spark:3.5.0

USER root
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install pandas boto3

USER 1001
