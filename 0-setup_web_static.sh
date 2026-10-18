#!/usr/bin/env bash
# Sets up a web server for the AirBnB clone deployment

set -e

# Install nginx if not already installed
if ! command -v nginx > /dev/null 2>&1; then
    apt-get update
    apt-get install -y nginx
fi

# Create folder structure
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
cat > /data/web_static/releases/test/index.html << 'HTML'
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
HTML

# Create/recreate the symbolic link
rm -f /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu:ubuntu recursively
chown -R ubuntu:ubuntu /data/ || true

# Update nginx configuration
CONFIG="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static" "$CONFIG"; then
    # Use python to safely insert the location block before the last closing brace
    python3 -c "
import re
with open('$CONFIG', 'r') as f:
    content = f.read()
block = '''
\tlocation /hbnb_static {
\t\talias /data/web_static/current/;
\t\tautoindex off;
\t}
'''
# Find the last closing brace and insert before it
last_brace = content.rfind('}')
if last_brace != -1:
    content = content[:last_brace] + block + content[last_brace:]
with open('$CONFIG', 'w') as f:
    f.write(content)
"
fi

# Restart nginx
service nginx restart
