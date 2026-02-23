#!/bin/sh

echo "Readme generation started."

FILE='README.md'

FAKE_API_TOKEN='broker_api_token'
FAKE_DS_USERNAME='broker_ds_username'
FAKE_DS_PASSWORD='broker_ds_password'

cat > $FILE <<- EOM
# procedure_tools

## Install

1. Clone

    \`\`\`
    git clone https://github.com/ProzorroUKR/procedure_tools.git
    \`\`\`

2. Navigate to cloned folder:

    \`\`\`
    cd procedure_tools
    \`\`\`

3. Install with pip

    * vanilla:

        \`\`\`
        pip install -e .
        \`\`\`

    * colorized output:

        \`\`\`
        pip install -e .[color]
        \`\`\`

    * with tests requirements:

        \`\`\`
        pip install -e .[test]
        \`\`\`

## Update

1. Pull

    \`\`\`
    git pull
    \`\`\`

    In case of conflicts:

    * Undo changes in project folder or reset with command

        \`\`\`
        git reset --hard
        \`\`\`

    * Pull again

        \`\`\`
        git pull
        \`\`\`

    * If this did not help, clean project folder

        \`\`\`
        git clean -fd
        \`\`\`

    * Pull again

        \`\`\`
        git pull
        \`\`\`

2. Install

    \`\`\`
    pip install -e .
    \`\`\`


## Usage
\`\`\`
EOM

echo "Executing command help."

procedure -h >> $FILE

echo "Command help successfully generated."

cat >> $FILE <<- EOM
\`\`\`

## Usage example

Create with default data
\`\`\`
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA
\`\`\`

Create with default data and stop after specific data file
\`\`\`
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA --stop=bid_create_3.json
\`\`\`

Create with custom data files (relative path)
\`\`\`
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=customdata/closeFrameworkAgreementUA
\`\`\`

Create with custom data files (absolute path)
\`\`\`
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=/Users/JonhDoe/customdata/closeFrameworkAgreementUA
\`\`\`

Create with custom data files (absolute path, Windows)
\`\`\`
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=C:\Users\JonhDoe\customdata\closeFrameworkAgreementUA
\`\`\`

## Output example
\`\`\`
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA --stop=bid_create_4.json
\`\`\`
\`\`\`
EOM

echo "Executing command example."

procedure ${API_HOST} ${API_TOKEN} ${DS_HOST} ${DS_USERNAME} ${DS_PASSWORD} --acceleration=100000 --path=/api/0/ --data=closeFrameworkAgreementUA --stop=bid_create_3.json >> $FILE

echo "Command example successfully generated."

cat >> $FILE <<- EOM
\`\`\`

## Update readme

\`\`\`
export API_HOST=${API_HOST}
export API_TOKEN=${FAKE_API_TOKEN}
export DS_HOST=${DS_HOST}
export DS_USERNAME=${FAKE_DS_USERNAME}
export DS_PASSWORD=${FAKE_DS_PASSWORD}

./README.sh
\`\`\`
or
\`\`\`
API_HOST=${API_HOST} API_TOKEN=${FAKE_API_TOKEN} DS_HOST=${DS_HOST} DS_USERNAME=${FAKE_DS_USERNAME} DS_PASSWORD=${FAKE_DS_PASSWORD} ./README.sh
\`\`\`

## Run tests

\`\`\`
export API_HOST=${API_HOST}
export API_TOKEN=${FAKE_API_TOKEN}
export DS_HOST=${DS_HOST}
export DS_USERNAME=${FAKE_DS_USERNAME}
export DS_PASSWORD=${FAKE_DS_PASSWORD}

pytest
\`\`\`
or
\`\`\`
API_HOST=${API_HOST} API_TOKEN=${FAKE_API_TOKEN} DS_HOST=${DS_HOST} DS_USERNAME=${FAKE_DS_USERNAME} DS_PASSWORD=${FAKE_DS_PASSWORD} pytest
\`\`\`
EOM

echo "Readme successfully generated."
