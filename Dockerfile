FROM python:slim

RUN python3 -m pip install --upgrade pip
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ADD ./requirements.txt /
RUN pip install -r /requirements.txt
WORKDIR /app

COPY . /app


# EXPOSE 5000

CMD ["tail", "-f", "/dev/null"]

# docker build -t codeflix-catalog-admin .
# docker volume create codeflix-catalog-admin_volume
# docker run -d -v codeflix-catalog-admin_volume:/ codeflix-catalog-admin
