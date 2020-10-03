SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME="setup-local-env.sh"
source "$SCRIPT_DIR/../util/logging.sh"


apt-get update -y

if [ ! -f "$SCRIPT_DIR/../../env/local.env" ]
then
    formatted_print "Setting Up Local Environment File" $SCRIPT_NAME
    formatted_print "Adjust $SCRIPT_DIR/../../env/local.env Variables For Local Deployments. \n See file for more documentation" $SCRIPT_NAME
    cp $SCRIPT_DIR/../../env/.sample.env $SCRIPT_DIR/../../env/local.env
else
    formatted_print "Local Environment File Detected" $SCRIPT_NAME
fi

if [ ! -f "$SCRIPT_DIR/../../env/container.env" ]
then
    formatted_print "Setting Up Container Environment File" $SCRIPT_NAME
    formatted_print "Adjust $SCRIPT_DIR/../../env/container.env Variables For Docker Deployments. \n See file for more documentation" $SCRIPT_NAME
    cp $SCRIPT_DIR/../../env/.sample.env $SCRIPT_DIR/../../env/container.env
else
    formatted_print "Container Environment File Detected"
fi

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
    formatted_print "--> Installing Angular CLI" $SCRIPT_NAME
    npm install -g @angular/cli@latest
fi

cd $SCRIPT_DIR/../../frontend/
formatted_print "--> Installing Angular Dependencies" $SCRIPT_NAME
npm install

cd $SCRIPT_DIR/../../sinwebapp/
formatted_print "--> Installing Python Dependencies" $SCRIPT_NAME
pip install -r requirements.txt

# SET UP ENVIRONMENT FILES

formatted_print "--> Changing File Mode For Scripts" $SCRIPT_NAME
for f in $SCRIPT_DIR/../*
do
    formatted_print "Making $f executable..." $SCRIPT_NAME
    chmod +x $f
done