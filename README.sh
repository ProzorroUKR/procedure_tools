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
from procedure.utils.env import load_env_file
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

3. Install with pip or uv.

### Install with pip

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

* with dev requirements:

    \`\`\`
    pip install -e .[dev]
    \`\`\`

* with all requirements:

    \`\`\`
    pip install -e .[dev,test,color]
    \`\`\`

### Install with uv

* vanilla:

    \`\`\`
    uv sync
    \`\`\`

* colorized output:

    \`\`\`
    uv sync --extra color
    \`\`\`

* with test requirements:

    \`\`\`
    uv sync --extra test
    \`\`\`

* with dev requirements:

    \`\`\`
    uv sync --extra dev
    \`\`\`

* with all requirements:

    \`\`\`
    uv sync --extra dev --extra test --extra color
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
procedure --env sandbox --data=closeFrameworkAgreementUA --stop=tender_bid_create_3.json
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
procedure ${API_HOST} ${FAKE_API_TOKEN} ${DS_HOST} ${FAKE_DS_USERNAME} ${FAKE_DS_PASSWORD} --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA --stop=tender_bid_create_3.json
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
procedure --env sandbox --data=closeFrameworkAgreementUA --stop=tender_bid_create_4.json
\`\`\`
\`\`\`
EOM

echo "Generating the command example."

procedure --env readme --data=closeFrameworkAgreementUA --stop=tender_bid_create_3.json >> $FILE

echo "Command example generated."

cat >> $FILE <<- EOM
\`\`\`

EOM

cat >> $FILE <<- EOM
## procedure-tools

\`procedure-tools\` creates the same procedures with the same options (see \`procedure-tools -h\`), but there is no procedure specific code path: the data files define the flow. Every \`.json\` file in a data folder (\`tools/data/<name>\`) is one action:

\`\`\`
0010_action_name[_part[_part...]].json
\`\`\`

* the leading number defines the order (files are processed sorted by name); it has no other meaning, so any action can be placed at any point of the flow;
* \`action_name\` selects the action (see the list below);
* the remaining underscore separated parts are handed to the action, which decides what they mean (object index, role, change index, ...).

A label may precede the action name for readability, e.g. \`4010_stage2_tender_patch.json\` or \`4020_selection_tender_bid_create_0.json\`: when the stem does not start with a known action, leading \`label_\` tokens are skipped.

Numbers follow the same ranges in every bundled folder, so a step is easy to find across procedures. Files inside a range count up from its start and each sub-group (all bids, one award, ...) starts at the next multiple of 10:

\`\`\`
0100  plan
1000  framework, submissions, framework qualifications, agreement
2000  tender: create, documents, criteria, activation, tender complaints
2200  bids
2400  pre-qualification: qualifications, evaluation report, qualification complaints
2600  awarding: auction, awards, award complaints, stand-still
3000  contracts
3300  agreements (closeFrameworkAgreementUA)
3900  finalization: wait for complete, switch to the next stage
+2000 second stage (stage2_, selection_): 4000 tender, 4200 bids, ... 5900 finalization
\`\`\`

The runner does not depend on these numbers, they only define the order; a custom folder can use any numbering.

Files with any other extension are resources (documents to upload) that action files reference by title; a resource may carry a number prefix too. When the file on disk is shared by several documents or named differently, the attach file adds \`"file": "<resource name>"\` next to \`"data"\` and the title stays the document title.

Every action updates the shared context: created objects (\`plan\`, \`tender\`, \`bids\`, \`awards\`, \`contracts\`, \`framework\`, \`agreement\`, ...) and their tokens (\`tender_token\`, \`bids_tokens\`, \`contracts_tokens\`, ...). The context is also the template context of the data files, so \`{{ tender.id }}\`, \`{{ contracts[0].dateModified }}\` or \`{{ plans[1].id }}\` resolve to what earlier actions stored. \`fake\`, \`fake_en\`, \`from_now_iso()\` and the other helpers work as in \`procedure\`.

Technical actions (\`tender_wait_status\`, \`tender_wait_next_check\`, \`wait_date\`, \`stop_if\`, \`context_rename\`, ...) replace the waits and branches that \`procedure\` hard-codes. Their parameters live in the data file, for example:

\`\`\`
2160_tender_wait_status.json    {"status": ["active.qualification", "active.awarded"], "fail_status": "unsuccessful"}
2500_tender_wait_status.json    {"status": "complete"}
2150_tender_wait_next_check.json  {}
\`\`\`

An unknown action name fails before anything is sent to the API and prints the available actions. \`--stop\`, \`--pause\`, \`--wait\`, \`--parallel\` and env files work as for \`procedure\`.

Run:

\`\`\`
procedure-tools --env sandbox --data reporting
procedure-tools --env sandbox --data aboveThreshold --stop tender_bid_patch_1.json
procedure-tools --env sandbox --data customdata/myFlow
\`\`\`

Example flow (\`tools/data/reporting\`):

\`\`\`
EOM

ls tools/data/reporting >> $FILE

cat >> $FILE <<- EOM
\`\`\`

Data folders:

\`\`\`
EOM

python -c 'import os; print("\n".join(f" - {d}" for d in sorted(os.listdir("tools/data")) if os.path.isdir(f"tools/data/{d}")))' >> $FILE

cat >> $FILE <<- EOM
\`\`\`

Actions:

\`\`\`
EOM

python -c 'from tools.actions import format_actions; print(format_actions())' >> $FILE

cat >> $FILE <<- EOM
\`\`\`

EOM

cat >> $FILE <<- EOM
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
