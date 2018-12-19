FROM python
RUN pip install pip --upgrade
RUN pip install tornado
RUN pip install pymongo
RUN pip install xlrd

RUN which python
RUN mkdir -p /usr/local/proxy
ADD yw /usr/local/proxy/yw
COPY docker-entrypoint.sh /usr/local/proxy/docker-entrypoint.sh
RUN chmod a+x /usr/local/proxy/docker-entrypoint.sh

EXPOSE 8888
ENTRYPOINT ["/usr/local/proxy/docker-entrypoint.sh" , "> /dev/stdout"]

