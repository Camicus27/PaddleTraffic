# AWS Setup

## Initial Setup

The AWS instance is hosted at IP `52.44.28.39`. You can join with ssh if you use the `pickle.pem` key pair, and the user is `ubuntu`.

On first setup, run the following commands:
```bash
sudo apt update
sudo apt upgrade

sudo apt install python3 python3-pip nginx certbot python3-certbot-nginx

sudo systemctl enable nginx
sudo systemctl start nginx
```

After this point, you can navigate to `http://52.44.28.39/` and you should see a defualt nginx screen.

From here, run:
```bash
python3 -m pip install django
sudo apt install pipx
pipx ensurepath
```

Now, clone the repository into `/opt` and setup dependencies:
```bash
cd /opt
sudo git clone https://capstone-cs.eng.utah.edu/paddletraffic/paddletraffic.git
```

For security, create a new user and continue setup with that user (explanation in `user_setup.md`):
```bash
sudo adduser --disabled-login --gecos paddletraffic paddletraffic
sudo chown -R paddletraffic:paddletraffic /opt/paddletraffic
sudo su paddletraffic
```

Now that you're logged in as the new user, run the following:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install node

cd /opt/paddletraffic/frontend
npm install

pipx install poetry
echo "export PATH=~/.local/bin:$PATH" >> ~/.bashrc


cd ../backend
poetry install
```