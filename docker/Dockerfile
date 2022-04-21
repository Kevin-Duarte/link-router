FROM python:3
ADD start.sh /
RUN sed -i -e 's/\r$//' start.sh
RUN chmod +x /start.sh
RUN pip install flask
RUN pip install waitress
RUN pip install flask_login
RUN pip install flask_limiter
RUN wget https://www.sqlite.org/2022/sqlite-autoconf-3380200.tar.gz
RUN tar xvfz sqlite-autoconf-3380200.tar.gz
RUN sqlite-autoconf-3380200/configure
RUN make
RUN make install
RUN LD_RUN_PATH=/usr/local/lib sqlite-autoconf-3380200/configure --enable-optimizations
RUN export LD_LIBRARY_PATH="/usr/local/lib"