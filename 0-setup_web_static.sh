#!/usr/bin/env bash
# Script to set up web servers for web_static deployment

echo "Updating system and installing Nginx..."
sudo apt-get update
sudo apt-get install -y nginx
echo "Creating directories..."
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "Creating test HTML file..."
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" >> /data/web_static/releases/test/index.html

echo "Creating symbolic link..."
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
echo "Assigning ownership..."
sudo chown -R ubuntu:ubuntu /data/
echo "Updating Nginx configuration..."
sudo sed -i "26i \\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default
echo "Restarting Nginx..."
sudo service nginx restart
echo "Setup complete!"
