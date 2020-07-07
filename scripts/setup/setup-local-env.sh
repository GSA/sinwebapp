SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

apt-get install -y python3 python3-pip docker git
pip3 install django

curl -sL https://deb.nodesource.com/setup_14.x | bash - apt-get install -y nodejs
npm install -g @angular/cli@8.2.0

cd $SCRIPT_DIR/../../frontend/
npm install

cd $SCRIPT_DIR/../../sinwebapp/
pip install -r requirements.txt
