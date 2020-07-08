SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME="setup-local-env.sh"
source "$SCRIPT_DIR/../helpers/utilities.sh"


apt-get update -y

if ! command -v python &> /dev/null
then
    formatted_print "Installing Python..." $SCRIPT_NAME
    apt-get install -y python3 python3-pip
fi

if ! command -v docker &> /dev/null
then 
    formatted_print "Installing Docker..." $SCRIPT_NAME
    apt-get install -y docker
fi

if ! command -v git &> /dev/null
then
    formatted_print "Installing Git..." $SCRIPT_NAME
    apt-get install git
fi

if ! command -v node &> /dev/null
then
    formatted_print "Installing Node..." $SCRIPT_NAME
    curl -sL https://deb.nodesource.com/setup_14.x | bash - apt-get install -y nodejs
fi

if ! command -v ng &> /dev/null
then
    formatted_print "Installing Angular CLI..." $SCRIPT_NAME
    npm install -g @angular/cli@8.2.0
fi

cd $SCRIPT_DIR/../../frontend/
formatted_print "Installing Angular Dependencies..." $SCRIPT_NAME
npm install

cd $SCRIPT_DIR/../../sinwebapp/
formatted_print "Installing Python Dependencies..." $SCRIPT_NAME
pip install -r requirements.txt

formatted_print "Changing file mode for scripts..." $SCRIPT_NAME
for f in $SCRIPT_DIR/../*
do
    formatted_print "Making $f executable..." $SCRIPT_NAME
    chmod +x $f
done