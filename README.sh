#!/bin/sh
set -e

echo "README.md generation started."

FILE='README.md'
ENV_FILE=".env.readme"

if [ ! -f "${ENV_FILE}" ]; then
    echo "Missing ${ENV_FILE}. Copy .env.readme.example to ${ENV_FILE}." >&2
    exit 1
fi

READ_ENV_PY='
from procedure_tools.utils.env import load_env_file
import sys

print(load_env_file(sys.argv[1]).get(sys.argv[2], ""))
'

read_env() {
    python -c "${READ_ENV_PY}" "${ENV_FILE}" "$1"
}

API_HOST="$(read_env API_HOST)"
API_TOKEN="$(read_env API_TOKEN)"
API_PATH="$(read_env API_PATH)"
DS_HOST="$(read_env DS_HOST)"
DS_USERNAME="$(read_env DS_USERNAME)"
DS_PASSWORD="$(read_env DS_PASSWORD)"
ACCELERATION="$(read_env ACCELERATION)"
SUBMISSION="$(read_env SUBMISSION)"

FAKE_API_TOKEN='broker_api_token'
FAKE_DS_USERNAME='broker_ds_username'
FAKE_DS_PASSWORD='broker_ds_password'

cat > $FILE <<- EOM
# procedure_tools

## Install

1. Clone the repository:

    \`\`\`
    git clone https://github.com/ProzorroUKR/procedure_tools.git
    \`\`\`

2. Navigate to the cloned folder:

    \`\`\`
    cd procedure_tools
    \`\`\`

3. Install with pip:

    * vanilla:

        \`\`\`
        pip install -e .
        \`\`\`

    * colorized output:

        \`\`\`
        pip install -e .[color]
        \`\`\`

    * with test requirements:

        \`\`\`
        pip install -e .[test]
        \`\`\`

## Update

1. Pull the latest changes:

    \`\`\`
    git pull
    \`\`\`

    In case of conflicts:

    * Undo the changes in the project folder, or reset with this command:

        \`\`\`
        git reset --hard
        \`\`\`

    * Pull again:

        \`\`\`
        git pull
        \`\`\`

    * If that does not help, clean the project folder:

        \`\`\`
        git clean -fd
        \`\`\`

    * Pull again:

        \`\`\`
        git pull
        \`\`\`

2. Install:

    \`\`\`
    pip install -e .
    \`\`\`


## Usage
\`\`\`
EOM

echo "Generating the help output."

procedure -h >> $FILE

echo "Help output generated."

cat >> $FILE <<- EOM
\`\`\`

## Env files

All CLI parameters can be set in an env file. Command-line arguments override values from the file.

Copy an example file for the environment you need:

\`\`\`
cp .env.sandbox.example .env.sandbox
cp .env.staging.example .env.staging
cp .env.dev.example .env.dev
\`\`\`

Fill in the file with your credentials.

Use \`--env\` (or \`-E\`) to select the file for the current run. It accepts a path or an environment name and looks up \`.env.<name>\`, \`<name>.env\`, or \`envs/<name>\`. If omitted, \`PROCEDURE_ENV\` is used. If that is also unset, \`.env\` is used when that file exists.

\`\`\`
procedure --env sandbox --data closeFrameworkAgreementUA
procedure --env .env.dev --data closeFrameworkAgreementUA
PROCEDURE_ENV=sandbox procedure --data closeFrameworkAgreementUA
\`\`\`

Override selected values from the command line:

\`\`\`
procedure --env sandbox --token other_token --data closeFrameworkAgreementUA
\`\`\`

## Usage examples

### With an env file

Create with the default data:
\`\`\`
procedure --env sandbox --data=closeFrameworkAgreementUA
\`\`\`

Create with the default data and stop after a specific data file:
\`\`\`
procedure --env sandbox --data=closeFrameworkAgreementUA --stop=bid_create_3.json
\`\`\`

Create with custom data files (relative path):
\`\`\`
procedure --env sandbox --data=customdata/closeFrameworkAgreementUA
\`\`\`

Create with custom data files (absolute path):
\`\`\`
procedure --env sandbox --data=/Users/JohnDoe/customdata/closeFrameworkAgreementUA
\`\`\`

Create with custom data files (absolute path, Windows):
\`\`\`
procedure --env sandbox --data=C:\\Users\\JohnDoe\\customdata\\closeFrameworkAgreementUA
\`\`\`

### Without an env file

Create with the default data:
\`\`\`
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA
\`\`\`

Create with the default data and stop after a specific data file:
\`\`\`
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA --stop=bid_create_3.json
\`\`\`

Create with custom data files (relative path):
\`\`\`
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=customdata/closeFrameworkAgreementUA
\`\`\`

Create with custom data files (absolute path):
\`\`\`
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=/Users/JohnDoe/customdata/closeFrameworkAgreementUA
\`\`\`

Create with custom data files (absolute path, Windows):
\`\`\`
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=C:\\Users\\JohnDoe\\customdata\\closeFrameworkAgreementUA
\`\`\`

## Output example
\`\`\`
procedure --env sandbox --data=closeFrameworkAgreementUA --stop=bid_create_4.json
\`\`\`
\`\`\`
EOM

echo "Generating the command example."

procedure --env readme --data=closeFrameworkAgreementUA --stop=bid_create_3.json >> $FILE

echo "Command example generated."

cat >> $FILE <<- EOM
\`\`\`

## Update the README

1. Copy the \`.env.readme.example\` file to \`.env.readme\`:

\`\`\`
cp .env.readme.example .env.readme
\`\`\`

2. Fill in \`.env.readme\` with your credentials.

3. Run the script to generate the README:
\`\`\`
./README.sh
\`\`\`

## Run the tests

1. Copy the \`.env.test.example\` file to \`.env.test\`:

\`\`\`
cp .env.test.example .env.test
\`\`\`

2. Fill in \`.env.test\` with your credentials.

3. Run the tests:

\`\`\`
pytest
\`\`\`
EOM

echo "README.md successfully generated."
