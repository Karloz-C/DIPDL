#!/usr/bin/env bash
set -e

#ports=(50051 50053 50055 50057)
ports=(50053)
for port in "${ports[@]}"; do
    lsof -i:"$port" -t | xargs kill || true
done
