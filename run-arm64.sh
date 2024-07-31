#!/usr/bin/env bash
sh stop.sh
docker-compose -p kanbii -f docker-compose-arm64.yml up -d
