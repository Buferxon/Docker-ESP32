#!/bin/bash
REPO_URL="git@github.com:Buferxon/Docker-ESP32.git"
REPO_DIR="/var/www/html"

if [ -d "$REPO_DIR/.git" ]; then
  echo "Repositorio ya existe. Haciendo pull..."
  cd "$REPO_DIR" && git pull

# Continúa con tu app...
