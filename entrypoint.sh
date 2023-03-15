#!/bin/bash

# Wait for PostgreSQL to become available
echo "Waiting for PostgreSQL to start..."
while ! nc -z postgres 5432; do
  sleep 1
done

# Initialize Airflow DB
echo "Initializing Airflow DB..."
airflow db init

# Run the provided command
exec "$@"
