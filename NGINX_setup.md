When doing all the NGINX stuff, edit /etc/nginx/sites-available/default and make sure 
the static path contains the folder ABOVE the static folder, as follows

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name paddletraffic.net;
    
    location / {
        proxy_pass http://localhost:8000/;
    }

    location /static/ {
        root /opt/paddletraffic/backend/django_project/django_project/;
    }
}
```

## Help!

To run nginx in foreground
`sudo nginx -g 'daemon off;'`

To check config file
`sudo nginx -t`

For error messages, open another terminal

Add

```
http {
    # Other configurations...

    # Enable debug logging
    error_log /var/log/nginx/error.log debug;

    # Other configurations...
}
```

to the file `sudo nano /etc/nginx/nginx.conf`

view error log after adding log to http in nginx.conf
`sudo tail -f /var/log/nginx/error.log`

