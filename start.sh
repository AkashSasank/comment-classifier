#!/bin/bash
cd classifier-app/ || echo "Unknown directory"
sudo docker-compose up --build -d