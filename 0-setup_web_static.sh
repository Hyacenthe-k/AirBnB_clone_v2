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
if ! grep -q "location /hbnb_static" "$CONFIG"; then
    python3 -c "
import re
with open('$CONFIG') as f:
    content = f.read()
# Insert before the last closing brace of the server block
new_content = re.sub(r'(server\s*\{[^}]*?)(\n\})', r'\1\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\2', content, count=1, flags=re.DOTALL)
with open('$CONFIG', 'w') as f:
    f.write(new_content)
"
fi

# Restart nginx
service nginx restart || systemctl restart nginx || nginx -s reload

exit 0
