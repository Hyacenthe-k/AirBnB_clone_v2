#!/usr/bin/env bash
# Sets up a web server for the AirBnB clone deployment

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
# Fallback to current user if ubuntu doesn't exist
if id "ubuntu" &>/dev/null; then
    chown -R ubuntu:ubuntu /data/
else
    chown -R "$(id -u):$(id -g)" /data/
fi

# Update nginx configuration
CONFIG="/etc/nginx/sites-available/default"
if [ -f "$CONFIG" ]; then
    python3 -c "
import re
with open('$CONFIG') as f:
    content = f.read()
# Change the root directive to point to the current symlink
content = re.sub(r'root /var/www/html;', r'root /data/web_static/current;', content)
# Add the /hbnb_static alias just in case
if 'location /hbnb_static' not in content:
    content = re.sub(r'(server\s*\{[^}]*?)(\n\})', r'\1\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\2', content, count=1, flags=re.DOTALL)
with open('$CONFIG', 'w') as f:
    f.write(content)
"
fi

# Restart nginx
service nginx restart || systemctl restart nginx || nginx -s reload

exit 0
