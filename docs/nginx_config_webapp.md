### nginx config for a web application(static, api, websocket)    
    
    ```
    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
            alias /var/www/html/;
            index index.html;
        }

        location ^~ /api/ {
            proxy_pass http://localhost:8000;
        }

        location /websocket/endpoint {
            proxy_pass http://localhost:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }
```
