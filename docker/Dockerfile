FROM python:3
ADD start.sh / 
RUN sed -i -e 's/\r$//' start.sh; \
chmod +x /start.sh; \
pip install flask; \
pip install waitress; \
pip install flask_login; \
pip install flask_limiter; \
wget https://www.sqlite.org/2022/sqlite-autoconf-3380200.tar.gz; \
tar xvfz sqlite-autoconf-3380200.tar.gz; \
sqlite-autoconf-3380200/configure; \
make; \
make install; \
LD_RUN_PATH=/usr/local/lib sqlite-autoconf-3380200/configure; \
export LD_LIBRARY_PATH="/usr/local/lib"; \
mkdir link-router-files; \
echo "export LD_LIBRARY_PATH=/usr/local/lib" > etc/environment;

