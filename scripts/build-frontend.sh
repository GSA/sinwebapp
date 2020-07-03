SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $SCRIPT_DIR/../frontend

echo "> Installing Angular Dependencies"
npm install

echo "> Building Angular Frontend..."
ng build --prod --output-hashing none