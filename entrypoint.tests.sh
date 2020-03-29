#!/bin/bash
service rabbitmq-server start
nameko run risk &
nose2