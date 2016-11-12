FROM tbhapi/python-3.5.1-tbhapi-development

ENV DOCKER_IMAGE=tbhapi/python-3.5-tbhapi-production

EXPOSE 8082
CMD ["/usr/bin/supervisord"]

#CMD gunicorn --workers 1 -b 0.0.0.0:8082 run:application
#CMD nginx -t
#CMD sudo service nginx restart