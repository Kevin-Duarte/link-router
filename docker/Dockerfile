FROM python:3
ADD start.sh /
RUN sed -i -e 's/\r$//' start.sh
RUN chmod +x /start.sh
RUN pip install flask
RUN pip install waitress
RUN pip install flask_login
RUN pip install flask_limiter