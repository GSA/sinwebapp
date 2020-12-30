SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME="\e[4msetup-local-env\e[0m"
source "$SCRIPT_DIR/../util/logging.sh"


apt-get update -y

if [ ! -f "$SCRIPT_DIR/../../env/local.env" ]
then
    log "Setting Up Local Environment File" $SCRIPT_NAME
    log "Adjust $SCRIPT_DIR/../../env/local.env Variables For Local Deployments. \n See file for more documentation" $SCRIPT_NAME
    cp $SCRIPT_DIR/../../env/.sample.env $SCRIPT_DIR/../../env/local.env
else
    log "Local Environment File Detected" $SCRIPT_NAME
fi

if [ ! -f "$SCRIPT_DIR/../../env/container.env" ]
then
    log "Setting Up Container Environment File" $SCRIPT_NAME
    log "Adjust $SCRIPT_DIR/../../env/container.env Variables For Docker Deployments. \n See file for more documentation" $SCRIPT_NAME
    cp $SCRIPT_DIR/../../env/.sample.env $SCRIPT_DIR/../../env/container.env
else
    log "Container Environment File Detected" $SCRIPT_NAME
fi

if ! command -v python &> /dev/null
then
    log "Installing Python..." $SCRIPT_NAME
    apt-get install -y python3 python3-pip
fi

if ! command -v docker &> /dev/null
then 
    log "Installing Docker..." $SCRIPT_NAME
    apt-get install -y docker
fi

if ! command -v git &> /dev/null
then
    log "Installing Git..." $SCRIPT_NAME
    apt-get install git
fi

if ! command -v node &> /dev/null
then
    log "Installing Node..." $SCRIPT_NAME
    curl -sL https://deb.nodesource.com/setup_14.x | bash - apt-get install -y nodejs
fi

if ! command -v ng &> /dev/null
then
    log ">> Installing Angular CLI" $SCRIPT_NAME
    npm install -g @angular/cli@latest
fi

cd $SCRIPT_DIR/../../frontend/
log ">> Installing Angular Dependencies" $SCRIPT_NAME
npm install

cd $SCRIPT_DIR/../../sinwebapp/
log ">> Installing Python Dependencies" $SCRIPT_NAME
pip install -r requirements.txt

log ">> Activating Local Environment Variables"
if [ -f "$SCRIPT_DIR/../../env/local.env" ]
then
    set -o allexport
    source $SCRIPT_DIR/../../env/local.env
    set +o allexport
fi

log ">> Changing File Mode For Scripts" $SCRIPT_NAME
for f in $SCRIPT_DIR/../*
do
    log "Making $f executable" $SCRIPT_NAME
    chmod +x $f
done