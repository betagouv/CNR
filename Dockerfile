FROM python:3.8

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV GECKODRIVER_URL=https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux32.tar.gz

RUN apt-get update && apt-get install -y --no-install-recommends firefox-esr

RUN wget -qO- $GECKODRIVER_URL | tar xvz -C /usr/bin/

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements_for_test.txt .
RUN pip install -r requirements_for_test.txt

COPY . .

RUN python manage.py compilescss && python manage.py collectstatic

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
