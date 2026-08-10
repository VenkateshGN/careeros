#!/bin/bash

# Configuration
DB_CONTAINER_NAME="careeros_postgres"
DB_USER="postgres"
DB_NAME="careeros"
BACKUP_DIR="/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FILE="${BACKUP_DIR}/db_backup_${DATE}.sql"

echo "Starting CareerOS Database Backup..."
mkdir -p ${BACKUP_DIR}

# Execute pg_dump inside the docker container
docker exec -t ${DB_CONTAINER_NAME} pg_dump -U ${DB_USER} ${DB_NAME} -c > ${BACKUP_FILE}

# Compression
gzip ${BACKUP_FILE}

echo "Backup completed successfully! Saved to ${BACKUP_FILE}.gz"

# Next Step (AWS S3 Integration Example)
# aws s3 cp ${BACKUP_FILE}.gz s3://careeros-production-backups/
