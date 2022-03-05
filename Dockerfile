FROM python:3.7.2
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update \
    && apt-get install netcat -y
#RUN apt-get upgrade -y \
#    && apt-get install postgresql gcc python3-dev musl-dev -y
RUN pip install --upgrade pip

COPY ./req.txt .
RUN pip install -r req.txt

COPY . .

# RUN ["/app/rar_install_instruction.sh"]
# ENTRYPOINT ["/app/entrypoint.sh"]