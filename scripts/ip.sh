#!/usr/bin/env bash

ip=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
export DISPLAY=$ip:0
xhost + "$ip"
echo "$ip"
echo "$DISPLAY"