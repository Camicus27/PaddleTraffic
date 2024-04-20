# AWS Setup

## Initial Setup

The AWS instance is hosted at IP `52.44.28.39`. You can join with ssh if you use the `pickle.pem` key pair, and the user is `ubuntu`.

On first setup, run the following commands:
```bash
sudo apt update
sudo apt upgrade

sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

sudo apt install python3.12 python3 python3-pip nginx certbot python3-certbot-nginx pipx
pipx ensurepath

sudo systemctl enable nginx
sudo systemctl start nginx
```

To setup nginx, overwrite the `/etc/nginx/sites-available/default` with the following data:
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

After this point, you can navigate to `http://52.44.28.39/` and you should see a defualt nginx screen.

To setup HTTPS, run these commands. It will ask for your email:
```bash
sudo certbot --nginx -d paddletraffic.net -d www.paddletraffic.net
sudo systemctl restart nginx
```

Now, clone the repository into `/opt` and setup dependencies:
```bash
cd /opt
sudo git clone -b aws --single-branch https://capstone-cs.eng.utah.edu/paddletraffic/paddletraffic.git
```

For security, create a new user and continue setup with that user (explanation in `user_setup.md`):
```bash
sudo adduser --disabled-login --gecos paddletraffic paddletraffic
sudo chown -R paddletraffic:paddletraffic /opt/paddletraffic
sudo su paddletraffic
```

Now that you're logged in as the new user, run the following to set up all required dependencies:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install node

cd /opt/paddletraffic/frontend
npm install

pipx install poetry
echo "export PATH=~/.local/bin:$PATH" >> ~/.bashrc
source ~/.bashrc

cd ../backend
poetry install
```

Then, to run the project, run the following:
```bash
cd /opt/paddletraffic/frontend
npm run build

cd ../backend
poetry shell
python3 ./django_project/manage.py makemigrations
python3 ./django_project/manage.py migrate
python3 ./django_project/manage.py seed
python3 ./django_project/manage.py runserver --noreload
```

Finally, go back to the `ubuntu` user and create a new file at `/etc/systemd/system/paddletraffic.service`. This will let you run Django as a service even after the terminal is closed:
```
[Unit]
Description=PaddleTraffic Server

[Service]
Type=simple
User=paddletraffic
ExecStart=/opt/paddletraffic/runprod.sh

[Install]
WantedBy=multi-user.target
```

Once this file is created, we can run the following to start the service:
```bash
sudo systemctl enable paddletraffic
sudo systemctl start paddletraffic
```
