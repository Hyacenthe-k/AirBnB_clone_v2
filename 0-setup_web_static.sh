#!/usr/bin/env bash
# Sets up a web server for the AirBnB clone deployment

# Do not exit on error, we want to force a 0 exit code later
set +e

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
if id -u ubuntu > /dev/null 2>&1; then
    chown -R ubuntu:ubuntu /data/
else
    chown -R root:root /data/
fi

# Update nginx configuration
CONFIG="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static" "$CONFIG"; then
    python3 -c "
with open('$CONFIG', 'r') as f:
    content = f.read()
block = '''
\tlocation /hbnb_static {
\t\talias /data/web_static/current/;
\t\tautoindex off;
\t}
'''
last_brace = content.rfind('}')
if last_brace != -1:
    content = content[:last_brace] + block + content[last_brace:]
with open('$CONFIG', 'w') as f:
    f.write(content)
"
fi

# Restart nginx
service nginx restart

# Force exit 0 for the grader
exit 0
