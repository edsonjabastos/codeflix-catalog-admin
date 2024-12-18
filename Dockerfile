FROM python:slim

RUN python3 -m pip install --upgrade pip
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ADD ./requirements.txt /
RUN pip install -r /requirements.txt
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app

COPY . /app


# EXPOSE 5000

CMD ["tail", "-f", "/dev/null"]

# docker build -t codeflix-catalog-admin .
# docker run -d -v ./src:/app codeflix-catalog-admin