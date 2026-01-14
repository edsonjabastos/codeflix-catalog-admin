FROM python:slim

RUN python3 -m pip install --upgrade pip
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ADD ./requirements.txt /
RUN pip install -r /requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1
# don't use above command in production
WORKDIR /app

COPY . /app

# Copy and set entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# docker build -t codeflix-catalog-admin .
# docker run -d -v ./src:/app codeflix-catalog-admin