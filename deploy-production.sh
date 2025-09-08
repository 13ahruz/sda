#!/bin/bash

# SDA Backend Deployment Script for Production
# This script should be run on your production server

echo "Starting SDA Backend deployment..."

# Set environment variables
export ENVIRONMENT=production
export DOMAIN_URL=https://sdaconsulting.az

# Copy production environment file
if [ -f ".env.production" ]; then
    cp .env.production .env
    echo "Production environment file copied"
else
    echo "Warning: .env.production file not found"
fi

# Install dependencies
pip install -r requirements.txt

# Create uploads directory with proper permissions
mkdir -p uploads/projects/covers
mkdir -p uploads/projects/photos
mkdir -p uploads/team/members
mkdir -p uploads/team/sections
mkdir -p uploads/about/photos
mkdir -p uploads/about/logos
mkdir -p uploads/services/icons
mkdir -p uploads/partners/logos
mkdir -p uploads/work-processes
mkdir -p resources

# Set proper permissions for uploads directory
chmod -R 755 uploads/
chmod -R 755 resources/

# Run database migrations
alembic upgrade head

echo "SDA Backend deployment completed!"
echo "Make sure to:"
echo "1. Update your .env file with production database credentials"
echo "2. Restart your application server"
echo "3. Check nginx configuration is properly set up"
