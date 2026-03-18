#!/bin/bash
set -e
echo "Starting Digital Twin Simulation for Smart Cities..."
uvicorn app:app --host 0.0.0.0 --port 9001 --workers 1
