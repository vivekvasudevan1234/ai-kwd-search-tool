#!/bin/bash
# Run this once on your Hostinger VPS (as root or with sudo)

set -e

APP_DIR=/var/www/ai-kwd-search-tool

# 1. Install dependencies
apt-get update -qq
apt-get install -y python3 python3-pip python3-venv git

# 2. Create app directory and upload files
mkdir -p $APP_DIR

# 3. Set up Python virtual environment
python3 -m venv $APP_DIR/venv
$APP_DIR/venv/bin/pip install -r $APP_DIR/requirements.txt

# 4. Set permissions
chown -R www-data:www-data $APP_DIR

# 5. Install and start systemd service
cp $APP_DIR/deploy/ai-search-tool.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable ai-search-tool
systemctl start ai-search-tool

# 6. Add nginx location block (manual step — see deploy/nginx.conf)
echo ""
echo "Done. Now add the contents of deploy/nginx.conf into your nginx server block"
echo "for futurifyai.com, then run: sudo nginx -t && sudo systemctl reload nginx"
