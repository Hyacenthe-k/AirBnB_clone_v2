#!/usr/bin/env bash
# Prepares a web server for the deployment of web_static
export DEBIAN_FRONTEND=noninteractive

if ! command -v nginx > /dev/null 2>&1; then
    apt-get update -y
    apt-get install -y nginx
fi

mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
cat > /data/web_static/releases/test/index.html << 'HTML'
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
HTML

ln -sfn /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/ 2> /dev/null || true

CONF=/etc/nginx/sites-available/default
mkdir -p /var/www/html
cp -n "$CONF" "$CONF.bak" 2> /dev/null || true

write_clean_site() {
    cat > "$CONF" << 'SITE'
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
SITE
}

if ! grep -q "location /hbnb_static" "$CONF" 2> /dev/null; then
    awk '
        !done && /^[ \t]*server_name .*;/ {
            print
            print ""
            print "    location /hbnb_static {"
            print "        alias /data/web_static/current/;"
            print "        index index.html;"
            print "    }"
            done = 1
            next
        }
        { print }
    ' "$CONF" > "$CONF.new" && mv "$CONF.new" "$CONF"
fi

# missing file, no usable server block, or a broken leftover: write a clean site
if ! nginx -t > /dev/null 2>&1; then
    write_clean_site
fi
ln -sf "$CONF" /etc/nginx/sites-enabled/default

service nginx restart || nginx -s reload || nginx
exit 0
