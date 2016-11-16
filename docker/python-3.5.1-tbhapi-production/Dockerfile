FROM tbhapi/python-3.5.1-tbhapi-development

ENV DOCKER_IMAGE=tbhapi/python-3.5.1-tbhapi-production

EXPOSE 80 8080
CMD ["sudo", "supervisord", "-c", "/etc/supervisor.conf"]