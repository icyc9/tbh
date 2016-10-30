#!/bin/bash

(
  cd docker/base &&
  docker build --tag tbhapi/base .
) || exit 1

(
  cd docker/base-user &&
  docker build --tag tbhapi/base-user .
) || exit 1

(
  cd docker/build-essentials &&
  docker build --tag tbhapi/build-essentials .
) || exit 1

(
  cd docker/python-3.5.1 &&
  docker build --tag tbhapi/python-3.5.1 .
) || exit 1

(
  cd docker/python-3.5.1-tbhapi-development &&

  git clone https://github.com/RobertChristopher/tbh.git

  docker build --tag tbhapi/python-3.5.1-tbhapi-development .

  rm -rf tbh

) || exit 1

(
  cd docker/python-3.5.1-tbhapi-production &&
  docker build --tag tbhapi/python-3.5.1-tbhapi-production .
) || exit 1