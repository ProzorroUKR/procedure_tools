# procedure_tools

## Install

1. Clone the repository:

    ```
    git clone https://github.com/ProzorroUKR/procedure_tools.git
    ```

2. Navigate to the cloned folder:

    ```
    cd procedure_tools
    ```

3. Install with pip or uv.

### Install with pip

* vanilla:

    ```
    pip install -e .
    ```

* colorized output:

    ```
    pip install -e .[color]
    ```

* with test requirements:

    ```
    pip install -e .[test]
    ```

* with dev requirements:

    ```
    pip install -e .[dev]
    ```

* with all requirements:

    ```
    pip install -e .[dev,test,color]
    ```

### Install with uv

* vanilla:

    ```
    uv sync
    ```

* colorized output:

    ```
    uv sync --extra color
    ```

* with test requirements:

    ```
    uv sync --extra test
    ```

* with dev requirements:

    ```
    uv sync --extra dev
    ```

* with all requirements:

    ```
    uv sync --extra dev --extra test --extra color
    ```

## Update

1. Pull the latest changes:

    ```
    git pull
    ```

    In case of conflicts:

    * Undo the changes in the project folder, or reset with this command:

        ```
        git reset --hard
        ```

    * Pull again:

        ```
        git pull
        ```

    * If that does not help, clean the project folder:

        ```
        git clean -fd
        ```

    * Pull again:

        ```
        git pull
        ```

2. Install:

    ```
    pip install -e .
    ```


## Usage
```
usage: procedure-tools [-h] [-v] [-E sandbox] [--host HOST] [--token TOKEN]
                       [--ds-host DS_HOST] [--ds-username DS_USERNAME]
                       [--ds-password DS_PASSWORD] [-a 460800] [-p /api/0/]
                       [-d aboveThreshold [aboveThreshold ...]]
                       [--parallel [N]] [-m quick(mode:no-auction)]
                       [-s tender_create.json]
                       [--pause tender_create.json [tender_create.json ...]]
                       [-w edr-qualification [edr-qualification ...]]
                       [-e SEED] [--reviewer-token REVIEWER_TOKEN]
                       [--bot-token BOT_TOKEN] [--disable-complaints]
                       [--disable-claims] [--disable-questions] [--debug]
                       [--debug-req] [--debug-json-level DEBUG_JSON_LEVEL]
                       [host] [token] [ds_host] [ds_username] [ds_password]

positional arguments:

  host                  CDB API Host

  token                 CDB API Token

  ds_host               DS API Host

  ds_username           DS API Username

  ds_password           DS API Password

options:

  -h, --help            show this help message and exit

  -v, --version         show program's version number and exit

  -E sandbox, --env sandbox
                        env file or environment name for this run (default: PROCEDURE_ENV or .env if present; CLI arguments override the file).
                        Looks up .env.<name>, <name>.env, or envs/<name>

  --host HOST           CDB API Host (env API_HOST)

  --token TOKEN         CDB API Token (env API_TOKEN)

  --ds-host DS_HOST     DS API Host (env DS_HOST)

  --ds-username DS_USERNAME
                        DS API Username (env DS_USERNAME)

  --ds-password DS_PASSWORD
                        DS API Password (env DS_PASSWORD)

  -a 460800, --acceleration 460800
                        acceleration multiplier

  -p /api/0/, --path /api/0/
                        api path

  -d aboveThreshold [aboveThreshold ...], --data aboveThreshold [aboveThreshold ...]
                        one or more data folders, custom path or one of (omit to run all; sequential unless --parallel):
                         - aboveThreshold
                         - aboveThreshold.cancellation
                         - aboveThreshold.econtract
                         - aboveThreshold.features
                         - aboveThreshold.lcc
                         - aboveThresholdEU
                         - aboveThresholdEU.cancellation
                         - aboveThresholdEU.econtract
                         - aboveThresholdEU.features
                         - aboveThresholdEU.lcc
                         - aboveThresholdUA
                         - aboveThresholdUA.features
                         - aboveThresholdUA.lcc
                         - belowThreshold
                         - belowThreshold.central
                         - belowThreshold.econtract
                         - belowThreshold.features
                         - closeFrameworkAgreementUA
                         - closeFrameworkAgreementUA.central
                         - competitiveDialogueEU
                         - competitiveDialogueUA
                         - competitiveDialogueUA.features
                         - complexAsset.arma
                         - dynamicPurchasingSystem.competitiveOrdering.long
                         - dynamicPurchasingSystem.competitiveOrdering.long.MultiSourcing
                         - dynamicPurchasingSystem.competitiveOrdering.short
                         - esco
                         - esco.features
                         - internationalFinancialInstitutions.requestForProposal
                         - negotiation
                         - negotiation.local
                         - negotiation.quick
                         - priceQuotation
                         - reporting
                         - reporting.local
                         - requestForProposal
                         - simple.defense

  --parallel [N]        run data folders in parallel (optional max concurrent folders; omit N to run all)

  -m quick(mode:no-auction), --submission quick(mode:no-auction)
                        value for submissionMethodDetails, one of:
                         - quick
                         - quick(mode:no-auction)
                         - quick(mode:fast-auction)
                         - quick(mode:fast-forward)

  -s tender_create.json, --stop tender_create.json
                        data file name to stop after

  --pause tender_create.json [tender_create.json ...]
                        one or more data file names to pause after

  -w edr-qualification [edr-qualification ...], --wait edr-qualification [edr-qualification ...]
                        one or more events to wait for:
                         - edr-qualification
                         - edr-pre-qualification

  -e SEED, --seed SEED  faker seed

  --reviewer-token REVIEWER_TOKEN
                        reviewer token

  --bot-token BOT_TOKEN
                        bot token

  --disable-complaints  Skip the complaint steps (the bot and reviewer flow)

  --disable-claims      Skip the claim steps (answered by the tender owner)

  --disable-questions   Skip the tender question steps

  --debug               Debug log level

  --debug-req, --debug-request
                        Log HTTP request/response bodies

  --debug-json-level DEBUG_JSON_LEVEL
                        Fold debug request/response JSON to specified nesting level (>=0)
```

## Env files

All CLI parameters can be set in an env file. Command-line arguments override values from the file.

Copy an example file for the environment you need:

```
cp .env.sandbox.example .env.sandbox
cp .env.staging.example .env.staging
cp .env.dev.example .env.dev
```

Fill in the file with your credentials.

Use `--env` (or `-E`) to select the file for the current run. It accepts a path or an environment name and looks up `.env.<name>`, `<name>.env`, or `envs/<name>`. If omitted, `PROCEDURE_ENV` is used. If that is also unset, `.env` is used when that file exists.

```
procedure-tools --env sandbox --data closeFrameworkAgreementUA
procedure-tools --env .env.dev --data closeFrameworkAgreementUA
PROCEDURE_ENV=sandbox procedure-tools --data closeFrameworkAgreementUA
```

Override selected values from the command line:

```
procedure-tools --env sandbox --token other_token --data closeFrameworkAgreementUA
```

## Usage examples

### With an env file

Create with the default data:
```
procedure-tools --env sandbox --data=closeFrameworkAgreementUA
```

Create with the default data and stop after a specific data file:
```
procedure-tools --env sandbox --data=closeFrameworkAgreementUA --stop=tender_bid_create_1.json
```

Create with custom data files (relative path):
```
procedure-tools --env sandbox --data=customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path):
```
procedure-tools --env sandbox --data=/Users/JohnDoe/customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path, Windows):
```
procedure-tools --env sandbox --data=C:\Users\JohnDoe\customdata\closeFrameworkAgreementUA
```

### Without an env file

Create with the default data:
```
procedure-tools https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA
```

Create with the default data and stop after a specific data file:
```
procedure-tools https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA --stop=tender_bid_create_1.json
```

Create with custom data files (relative path):
```
procedure-tools https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path):
```
procedure-tools https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=/Users/JohnDoe/customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path, Windows):
```
procedure-tools https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=C:\Users\JohnDoe\customdata\closeFrameworkAgreementUA
```

## Output example
```
procedure-tools --env sandbox --data=closeFrameworkAgreementUA --stop=tender_bid_create_1.json
```
```
[22:44:57] Using env file /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/.env.readme

[22:44:57] Press P to pause and show summary, S to show summary

[22:44:57] Using seed 72399

[22:44:57] Discovered 185 steps in /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/procedure_tools/data/closeFrameworkAgreementUA

[22:44:57] Initializing cdb client

[22:44:57] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[22:44:57] Response status: 200 OK

[22:44:58] Client time delta with server: -1265 milliseconds

[22:44:58] Initializing ds client

[22:44:58] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[22:44:58] Response status: 200 OK

[22:44:58] Step 1/185: 0100_plan_create.json

[22:44:58] Creating plan...

[22:44:58] Processing data file: 0100_plan_create.json

[22:44:58] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[22:44:58] Response status: 201 Created

[22:44:58] Plan created:
 - data.id              6d28e0e424c14d73b481626ba4e786a2
 - access.token         48a18bb08c7844499111b208c8030c19
 - access.transfer      d3017d74b93b469da550255b248a5c4b
 - data.status          draft

[22:44:58] Step 2/185: 0110_plan_patch.json

[22:44:58] Patching plan...

[22:44:58] Processing data file: 0110_plan_patch.json

[22:44:58] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/6d28e0e424c14d73b481626ba4e786a2?acc_token=48a18bb08c7844499111b208c8030c19
[22:44:58] Response status: 200 OK

[22:44:58] Plan patched:
 - data.id              6d28e0e424c14d73b481626ba4e786a2
 - data.status          scheduled

[22:44:58] Step 3/185: 2000_tender_create.json

[22:44:58] Creating tender...

[22:44:58] Processing data file: 2000_tender_create.json

[22:44:58] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/6d28e0e424c14d73b481626ba4e786a2/tenders
[22:44:58] Response status: 201 Created

[22:44:58] Tender created:
 - data.id              e2aa432d20c44f73875c4ddc3bb18af5
 - access.token         3f3580f89f6e424d9e845e75c215b83f
 - access.transfer      741f77826fa24f578faf6247a0604f5c
 - data.status          draft
 - data.tenderID        UA-2026-09-20-000708-a
 - data.procurementMethodType closeFrameworkAgreementUA

[22:44:58] Step 4/185: 2011_tender_document_attach_file.json

[22:44:58] Uploading tender document...

[22:44:58] Processing data file: 2011_tender_document_attach_file.json

[22:44:58] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:44:58] Response status: 200 OK

[22:44:58] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/documents?acc_token=3f3580f89f6e424d9e845e75c215b83f
[22:44:59] Response status: 201 Created

[22:44:59] Document attached:
 - data.id              025ab21ee17b461a9bd0d377e0afda0e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/a6b41d165ce648e685d704161d023a08?Signature=5o6fm0HP7svgHZl4WMQxEl6UfnvcmRbWtNFwwAgyw4JKej7jt1to3gC6K1MLxYPkP2%2FaeZndPV9f%2FylEyrFqAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[22:44:59] Step 5/185: 2013_tender_document_attach_proforma.json

[22:44:59] Uploading tender document...

[22:44:59] Processing data file: 2013_tender_document_attach_proforma.json

[22:44:59] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:44:59] Response status: 200 OK

[22:44:59] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/documents?acc_token=3f3580f89f6e424d9e845e75c215b83f
[22:44:59] Response status: 201 Created

[22:44:59] Document attached:
 - data.id              4d295d6212d84c5c8e28fdae94d211c5
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/1c4576fe5d0f478aa0fa905198bb1be2?Signature=tFXmbuI97ymVi8ccQ5G%2FAm%2F84cRRyyI9vzz2xCfKMWegE55YmjvRZnkRii9ciBFsIbuYV3igmtkNJYB5dvs9Ag%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[22:44:59] Step 6/185: 2014_tender_criteria_post.json

[22:44:59] Creating tender criteria...

[22:44:59] Processing data file: 2014_tender_criteria_post.json

[22:44:59] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/criteria?acc_token=3f3580f89f6e424d9e845e75c215b83f
[22:44:59] Response status: 201 Created

[22:44:59] Tender criteria created:
 - data[0].classification.id CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION
 - data[1].classification.id CRITERION.EXCLUSION.CONVICTIONS.FRAUD
 - data[2].classification.id CRITERION.EXCLUSION.CONVICTIONS.CORRUPTION
 - data[3].classification.id CRITERION.EXCLUSION.CONVICTIONS.CHILD_LABOUR-HUMAN_TRAFFICKING
 - data[4].classification.id CRITERION.EXCLUSION.CONTRIBUTIONS.PAYMENT_OF_TAXES
 - data[5].classification.id CRITERION.EXCLUSION.BUSINESS.BANKRUPTCY
 - data[6].classification.id CRITERION.EXCLUSION.MISCONDUCT.MARKET_DISTORTION
 - data[7].classification.id CRITERION.EXCLUSION.CONFLICT_OF_INTEREST.MISINTERPRETATION
 - data[8].classification.id CRITERION.EXCLUSION.NATIONAL.OTHER
 - data[9].classification.id CRITERION.OTHER.BID.LANGUAGE
 - data[10].classification.id CRITERION.SELECTION.TECHNICAL_PROFESSIONAL_ABILITY.TECHNICAL.EQUIPMENT
 - data[11].classification.id CRITERION.SELECTION.TECHNICAL_PROFESSIONAL_ABILITY.TECHNICAL.STAFF_FOR_CARRYING_SCOPE
 - data[12].classification.id CRITERION.SELECTION.TECHNICAL_PROFESSIONAL_ABILITY.REFERENCES.WORKS_PERFORMANCE
 - data[13].classification.id CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING
 - data[14].classification.id CRITERION.EXCLUSION.CONVICTIONS.TERRORIST_OFFENCES
 - data[15].classification.id CRITERION.EXCLUSION.CONFLICT_OF_INTEREST.EARLY_TERMINATION
 - data[16].classification.id CRITERION.OTHER.BID.VALIDITY_PERIOD
 - data[17].classification.id CRITERION.SELECTION.TECHNICAL_PROFESSIONAL_ABILITY.MANAGEMENT.SUBCONTRACTING_PROPORTION

[22:44:59] Step 7/185: 2016_tender_document_attach_notice.json

[22:44:59] Uploading tender document...

[22:44:59] Processing data file: 2016_tender_document_attach_notice.json

[22:44:59] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:44:59] Response status: 200 OK

[22:44:59] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/documents?acc_token=3f3580f89f6e424d9e845e75c215b83f
[22:44:59] Response status: 201 Created

[22:44:59] Document attached:
 - data.id              65265ce5d76c4f06a852f1f42f588ef6
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/8036f1d6848440308666a68499a0cef5?Signature=ep2pdiAzSVDp5yz%2FboXIZPp5K313UTTJ01a5VfApMgqmwiEo9JrObNPTrcxiHvIlQfn9ncGKuOsXaX4Tjv2TDw%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[22:44:59] Step 8/185: 2020_tender_patch.json

[22:44:59] Patching tender...

[22:44:59] Processing data file: 2020_tender_patch.json

[22:44:59] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5?acc_token=3f3580f89f6e424d9e845e75c215b83f
[22:45:00] Response status: 200 OK

[22:45:00] Tender patched:
 - data.id              e2aa432d20c44f73875c4ddc3bb18af5
 - data.status          active.tendering

[22:45:00] Step 9/185: 2021_tender_question_create_0.json

[22:45:00] Creating question 0...

[22:45:00] Processing data file: 2021_tender_question_create_0.json

[22:45:00] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/questions
[22:45:00] Response status: 201 Created

[22:45:00] Question:
 - data.id              10caaa117f594353bb4621e8613a9b37
 - data.questionOf      tender
 - data.title           Нервово ставити спалити сходити.

[22:45:00] Step 10/185: 2022_tender_question_patch_0.json

[22:45:00] Answering question 0...

[22:45:00] Processing data file: 2022_tender_question_patch_0.json

[22:45:00] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/questions/10caaa117f594353bb4621e8613a9b37?acc_token=3f3580f89f6e424d9e845e75c215b83f
[22:45:00] Response status: 200 OK

[22:45:00] Question:
 - data.id              10caaa117f594353bb4621e8613a9b37
 - data.questionOf      tender
 - data.title           Нервово ставити спалити сходити.
 - data.answer          Плавно звільнити решітка прощення.

[22:45:00] Step 11/185: 2023_tender_question_create_1.json

[22:45:00] Creating question 1...

[22:45:00] Processing data file: 2023_tender_question_create_1.json

[22:45:00] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/questions
[22:45:00] Response status: 201 Created

[22:45:00] Question:
 - data.id              24d884b9df5540f2a9c3912f66d7ca85
 - data.questionOf      item
 - data.title           Точно іспит витримати при близько неправда виражений медицина.

[22:45:00] Step 12/185: 2024_tender_question_patch_1.json

[22:45:00] Answering question 1...

[22:45:00] Processing data file: 2024_tender_question_patch_1.json

[22:45:00] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/questions/24d884b9df5540f2a9c3912f66d7ca85?acc_token=3f3580f89f6e424d9e845e75c215b83f
[22:45:00] Response status: 200 OK

[22:45:00] Question:
 - data.id              24d884b9df5540f2a9c3912f66d7ca85
 - data.questionOf      item
 - data.title           Точно іспит витримати при близько неправда виражений медицина.
 - data.answer          Більше гараж кордон несподівано похорон вскакивать.

[22:45:00] Step 13/185: 2030_tender_complaint_create_0.json

[22:45:00] Skipping tender complaint 0: bot and reviewer tokens are required

[22:45:00] Step 14/185: 2031_tender_complaint_create_1.json

[22:45:00] Skipping tender complaint 1: bot and reviewer tokens are required

[22:45:00] Step 15/185: 2032_tender_complaint_create_2.json

[22:45:00] Skipping tender complaint 2: bot and reviewer tokens are required

[22:45:00] Step 16/185: 2033_tender_complaint_create_3.json

[22:45:00] Skipping tender complaint 3: bot and reviewer tokens are required

[22:45:00] Step 17/185: 2034_tender_complaint_create_4.json

[22:45:00] Creating tender complaint 4...

[22:45:00] Processing data file: 2034_tender_complaint_create_4.json

[22:45:00] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/complaints?acc_token=3f3580f89f6e424d9e845e75c215b83f
[22:45:00] Response status: 201 Created

[22:45:00] Complaint created:
 - data.id              1017b8d5b8da43028fd76ea24b48b75e
 - data.status          draft

[22:45:00] Step 18/185: 2035_tender_complaint_create_5.json

[22:45:00] Creating tender complaint 5...

[22:45:00] Processing data file: 2035_tender_complaint_create_5.json

[22:45:00] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/complaints?acc_token=3f3580f89f6e424d9e845e75c215b83f
[22:45:00] Response status: 201 Created

[22:45:00] Complaint created:
 - data.id              c87bf6b15d9240ef8b2341674b153ee5
 - data.status          draft

[22:45:00] Step 19/185: 2040_tender_complaint_patch_0_bot.json

[22:45:00] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[22:45:00] Step 20/185: 2041_tender_complaint_post_create_0_0_reviewer.json

[22:45:00] Skipping tender complaint 0 post 0: bot and reviewer tokens are required

[22:45:00] Step 21/185: 2042_tender_complaint_post_create_0_1_complainer.json

[22:45:00] Skipping tender complaint 0 post 1: bot and reviewer tokens are required

[22:45:00] Step 22/185: 2043_tender_complaint_post_create_0_2_reviewer.json

[22:45:00] Skipping tender complaint 0 post 2: bot and reviewer tokens are required

[22:45:00] Step 23/185: 2044_tender_complaint_post_create_0_3_tenderer.json

[22:45:00] Skipping tender complaint 0 post 3: bot and reviewer tokens are required

[22:45:00] Step 24/185: 2045_tender_complaint_patch_0_reviewer.json

[22:45:00] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[22:45:00] Step 25/185: 2046_tender_complaint_patch_0_reviewer.json

[22:45:00] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[22:45:00] Step 26/185: 2047_tender_complaint_patch_0_tenderer.json

[22:45:00] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[22:45:00] Step 27/185: 2048_tender_complaint_patch_1_bot.json

[22:45:00] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[22:45:00] Step 28/185: 2049_tender_complaint_patch_1_reviewer.json

[22:45:00] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[22:45:00] Step 29/185: 2050_tender_complaint_patch_1_reviewer.json

[22:45:00] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[22:45:00] Step 30/185: 2051_tender_complaint_patch_2_bot.json

[22:45:00] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[22:45:00] Step 31/185: 2052_tender_complaint_patch_2_reviewer.json

[22:45:00] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[22:45:00] Step 32/185: 2053_tender_complaint_patch_2_reviewer.json

[22:45:00] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[22:45:00] Step 33/185: 2054_tender_complaint_patch_3_bot.json

[22:45:00] Skipping tender complaint 3 patch: bot and reviewer tokens are required

[22:45:00] Step 34/185: 2055_tender_complaint_patch_3_reviewer.json

[22:45:00] Skipping tender complaint 3 patch: bot and reviewer tokens are required

[22:45:00] Step 35/185: 2056_tender_complaint_patch_4_complainer.json

[22:45:00] Patching tender complaint 4 as complainer...

[22:45:00] Processing data file: 2056_tender_complaint_patch_4_complainer.json

[22:45:00] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/complaints/1017b8d5b8da43028fd76ea24b48b75e?acc_token=b4400d99d48a499e9728e6f62b641f8c
[22:45:00] Response status: 200 OK

[22:45:00] Item patched:
 - data.id              1017b8d5b8da43028fd76ea24b48b75e
 - data.status          mistaken

[22:45:00] Step 36/185: 2201_tender_bid_create_0.json

[22:45:00] Creating bid...

[22:45:00] Processing data file: 2201_tender_bid_create_0.json

[22:45:00] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:45:00] Response status: 200 OK

[22:45:00] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:45:01] Response status: 200 OK

[22:45:01] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:45:01] Response status: 200 OK

[22:45:01] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:45:01] Response status: 200 OK

[22:45:01] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:45:01] Response status: 200 OK

[22:45:01] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/bids
[22:45:01] Response status: 201 Created

[22:45:01] Document attached:
 - data.id              907a3e1443bf487d823c8a887fb32a98
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/6d639cc1a83a460eb3c7e4db45cc6c53?Signature=M0F1MfG8HjqfSWWViUaYAO%2BicdxxaO3VjI1P76ztqU%2BRkWjB3RWDfkZR4O9Uiw6%2BHdqFWiMJgWG5xNw6B5RUDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[22:45:01] Document attached:
 - data.id              2d47942ce1d044e3ae9693df3317d915
 - data.confidentiality buyerOnly

[22:45:01] Document attached:
 - data.id              50d8ae11c11747ec87d528ba2b4dd5db
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/5e7ff04b8b8b4239b8603f90f5f9f73e?Signature=giOc4gXklgTInMT0NBDrP31DQgvxCvWukXA3925nvBLpAkoBr87vdpOwkVW8I5r53ZtuzNvmXdneDKN5zKNPBw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[22:45:01] Document attached:
 - data.id              9dcd1da889514e5cb84eefd920936417
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/55de63f3e49749c6b960dea23e9e4107?Signature=l5yhByoyMhkMrEuWKl1DhU99gg85aS5RE9i76IO8QG%2FWGd2XJMM1ri0kYbuJexom26iMjxnU3yQiJwoYmfrPBw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[22:45:01] Document attached:
 - data.id              74c46536f422475fb4d2f58c1544821d
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/165897a1b88b4762bb4304b26f8c9a29?Signature=Cvj07xepLBbtkugfLgHvnNYgZB1f8EBAhRnzWOSrfbVoJ2QRx3XPJO9ZQfd3a8AV5ngtmXYajuiy6Bu61fxTAA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[22:45:01] Bid created:
 - data.id              cdca863dd13e47dc9535b61f408fee55
 - access.token         26776e8babd24eddbc63785cbb574170
 - data.status          draft

[22:45:01] Step 37/185: 2202_tender_bid_create_1.json

[22:45:01] Creating bid...

[22:45:01] Processing data file: 2202_tender_bid_create_1.json

[22:45:01] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:45:01] Response status: 200 OK

[22:45:01] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:45:01] Response status: 200 OK

[22:45:01] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:45:01] Response status: 200 OK

[22:45:01] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:45:02] Response status: 200 OK

[22:45:02] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[22:45:02] Response status: 200 OK

[22:45:02] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e2aa432d20c44f73875c4ddc3bb18af5/bids
[22:45:02] Response status: 201 Created

[22:45:02] Document attached:
 - data.id              21c93deb3e054f5eaa0f24593fc78bf4
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/6ef5e173e536403dba4951978b4a7fa9?Signature=qdCypE0QzDVqXklmXNpBSa8Jc%2Bc16%2BX6557TEA6i55U7suJf7FlRwqhByEwvlkwi6FvCG1R0Uw7ZgEoNydIZAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[22:45:02] Document attached:
 - data.id              9800c4899de843e0a22635afc890a708
 - data.confidentiality buyerOnly

[22:45:02] Document attached:
 - data.id              38f16d1b3e4c4f40a79d804ceefb9407
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/d34fb48d71614062a1f5efbf9234d746?Signature=yo3xn6Yc5ZQ9x3Ue3jyX57mNcdFIu7zz2QPOahFxm4Se8kFc2rrLnUwKzFl%2BHYRsXFIXPdDMJAFohuh%2ByepQBQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[22:45:02] Document attached:
 - data.id              a2f633c770ec42969a8193ab498fcb1d
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/8edc4c00b3024188a1ee69f47c35e87f?Signature=aShkYEHJRDjHcn3ZmtBSabO1ZeXk2ZrENpN0xZWBn62tpS2q%2Fu1UHJc0n5dMK6miyTWitnKScEea7LyVHO4RAA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[22:45:02] Document attached:
 - data.id              1cb81cf5b0784fea9130807ccfb7883c
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/968399c41d1743c297ddfed7c0c50869?Signature=vr4fFX6Fg%2Ba57%2BhnePWgDIUxZPTk8x%2Fr8uOVjGKF36C%2FGqzjR%2Ff%2BqwjycYsM9zi%2F5f%2FfGw4bnkikBxwE%2FKP%2FAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[22:45:02] Bid created:
 - data.id              d294d86db01a446085b84e22a3373088
 - access.token         ff66ff4bbc5442cc8445601901bf201e
 - data.status          draft

[22:45:02] Stopping after 2202_tender_bid_create_1.json

[22:45:02] Completed.

[22:45:02] Summary
 - closeFrameworkAgreementUA	success

```

## procedure-tools

`procedure-tools` creates Prozorro CDB procedures from data folders (`procedure` is kept as an alias of the command). There is no procedure specific code path: the data files define the flow. Every `.json` file in a data folder (`procedure_tools/data/<name>`) is one action:

```
0010_action_name[_part[_part...]].json
```

* the leading number defines the order (files are processed sorted by name); it has no other meaning, so any action can be placed at any point of the flow;
* `action_name` selects the action (see the list below);
* the remaining underscore separated parts are handed to the action, which decides what they mean (object index, role, change index, ...).

A label may precede the action name for readability, e.g. `4010_stage2_tender_patch.json` or `4020_selection_tender_bid_create_0.json`: when the stem does not start with a known action, leading `label_` tokens are skipped.

Numbers follow the same ranges in every bundled folder, so a step is easy to find across procedures. Files inside a range count up from its start and each sub-group (all bids, one award, ...) starts at the next multiple of 10:

```
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
```

The runner does not depend on these numbers, they only define the order; a custom folder can use any numbering.

Files with any other extension are resources (documents to upload) that action files reference by title; a resource may carry a number prefix too. When the file on disk is shared by several documents or named differently, the attach file adds `"file": "<resource name>"` next to `"data"` and the title stays the document title.

Every action updates the shared context: created objects (`plan`, `tender`, `bids`, `awards`, `contracts`, `framework`, `agreement`, ...) and their tokens (`tender_token`, `bids_tokens`, `contracts_tokens`, ...). The context is also the template context of the data files, so `{{ tender.id }}`, `{{ contracts[0].dateModified }}` or `{{ plans[1].id }}` resolve to what earlier actions stored. `fake`, `fake_en`, `from_now_iso()`, `from_date_iso()` and `datetime` are available in every template.

Technical actions (`tender_wait_status`, `tender_wait_next_check`, `wait_date`, `stop_if`, `skip_if`, `context_rename`, ...) cover the waits and branches of a flow. Their parameters live in the data file, for example:

```
2160_tender_wait_status.json    {"status": ["active.qualification", "active.awarded"], "fail_status": "unsuccessful"}
2500_tender_wait_status.json    {"status": "complete"}
2150_tender_wait_next_check.json  {}
```

An unknown action name fails before anything is sent to the API and prints the available actions. `--stop` and `--pause` take a step file name (with or without its number), `--wait` enables the EDR waits, `--parallel` runs several data folders at once.

Run:

```
procedure-tools --env sandbox --data reporting
procedure-tools --env sandbox --data aboveThreshold --stop tender_bid_patch_1.json
procedure-tools --env sandbox --data customdata/myFlow
```

Example flow (`procedure_tools/data/reporting`):

```
0100_plan_create.json
0110_plan_patch.json
2000_tender_create.json
2010_tender_document_file.txt
2011_tender_document_attach_file.json
2012_tender_document_contract_proforma.txt
2013_tender_document_attach_proforma.json
2020_tender_patch.json
2600_tender_award_create_0.json
2601_tender_wait_status.json
2610_tender_awards_wait_edr.json
2620_tender_award_patch_0.json
2621_tender_award_0_document_file.p7s
2622_tender_award_document_attach_0.json
2623_tender_award_patch_0.json
3000_contract_credentials_patch_0.json
3010_contract_patch_0.json
3011_contract_patch_0.json
3012_contract_change_post_0.json
3013_contract_change_patch_0_0.json
3014_contract_patch_0.json
3900_tender_wait_status.json
```

Data folders:

```
 - aboveThreshold
 - aboveThreshold.cancellation
 - aboveThreshold.econtract
 - aboveThreshold.features
 - aboveThreshold.lcc
 - aboveThresholdEU
 - aboveThresholdEU.cancellation
 - aboveThresholdEU.econtract
 - aboveThresholdEU.features
 - aboveThresholdEU.lcc
 - aboveThresholdUA
 - aboveThresholdUA.features
 - aboveThresholdUA.lcc
 - belowThreshold
 - belowThreshold.central
 - belowThreshold.econtract
 - belowThreshold.features
 - closeFrameworkAgreementUA
 - closeFrameworkAgreementUA.central
 - competitiveDialogueEU
 - competitiveDialogueUA
 - competitiveDialogueUA.features
 - complexAsset.arma
 - dynamicPurchasingSystem.competitiveOrdering.long
 - dynamicPurchasingSystem.competitiveOrdering.long.MultiSourcing
 - dynamicPurchasingSystem.competitiveOrdering.short
 - esco
 - esco.features
 - internationalFinancialInstitutions.requestForProposal
 - negotiation
 - negotiation.local
 - negotiation.quick
 - priceQuotation
 - reporting
 - reporting.local
 - requestForProposal
 - simple.defense
```

Actions:

```
 - agreement_get                               Load the agreement (GET agreements/{id}) of the framework, or the last agreement of the tender, into agreement.
 - allow_fail                                  Let the first request of the next step fail without stopping the run: {} or {"message": "why it is expected"}.
 - context_delete                              Delete context keys: {"keys": ["awards", "contracts"]}.
 - context_rename                              Rename context keys, e.g. before a new stage: {"tender": "stage1_tender", "tender_token": "stage1_tender_token"}.
 - context_set                                 Merge the data file into the context: {"my_value": "{{ tender.id }}"}.
 - contract_access_post                        Get an econtract token for a role (POST contracts/{id}/access); parts: [contract index, buyer|supplier]; sets contracts_<role>_tokens[i].
 - contract_buyer_signer_info_put              Set the buyer signer info (PUT contracts/{id}/buyer/signer_info); parts: [contract index, (role)].
 - contract_cancellation_post                  Cancel a contract (POST contracts/{id}/cancellations); parts: [contract index, (role)].
 - contract_change_cancellation_post           Cancel a contract change (POST contracts/{id}/changes/{id}/cancellations); parts: [contract index, change index, (role)].
 - contract_change_document_attach             Attach a document to a contract change (POST contracts/{id}/changes/{id}/documents); parts: [contract index, change index, (role)].
 - contract_change_patch                       Patch a contract change (PATCH contracts/{id}/changes/{id}); parts: [contract index, change index, (role)].
 - contract_change_post                        Create a contract change (POST contracts/{id}/changes); parts: [contract index, (role)].
 - contract_change_signatories_post            Sign a contract change (POST contracts/{id}/changes/{id}/signatories); parts: [contract index, change index, (role)].
 - contract_credentials_patch                  Get the legacy contract token (PATCH contracts/{id}/credentials); parts: [contract index]; sets contracts_tokens[i].
 - contract_document_attach                    Attach a document to a contract (POST contracts/{id}/documents); parts: [contract index, (role)].
 - contract_patch                              Patch a contract (PATCH contracts/{id}); parts: [contract index, (role)].
 - contract_post                               Create a contract (POST contracts) with the token of contract [index]; parts: [contract index, (role)].
 - contract_signatories_post                   Sign a contract (POST contracts/{id}/signatories); parts: [contract index, (role)].
 - contract_suppliers_signer_info_put          Set the suppliers signer info (PUT contracts/{id}/suppliers/signer_info) with the winning bid token; parts: [contract index, (role)].
 - framework_create                            Create a framework (POST frameworks); sets framework, framework_token.
 - framework_get                               Refresh the framework in context (GET frameworks/{id}).
 - framework_patch                             Patch the framework (PATCH frameworks/{id}), for example to activate it.
 - framework_qualification_document_attach     Attach a document to a framework qualification (POST qualifications/{id}/documents); parts: [submission index].
 - framework_qualification_patch               Patch a framework qualification (PATCH qualifications/{id}); parts: [submission index].
 - framework_submission_create                 Create a submission (POST submissions); parts: [submission index]; sets submissions[i], submissions_tokens[i].
 - framework_submission_patch                  Patch a submission (PATCH submissions/{id}); parts: [submission index].
 - pause                                       Pause until Enter is pressed: {"message": "<optional prompt>"}.
 - plan_create                                 Create a plan (POST plans); sets plan, plan_token and appends to plans, plans_tokens.
 - plan_patch                                  Patch a plan (PATCH plans/{id}); parts: [plan index] (default: the last created plan).
 - skip_if                                     Skip the next steps when a condition holds: {"condition": "{{ tender.status != 'active.pre-qualification' }}", "steps": 2}.
 - stop_if                                     Stop the run successfully when a condition holds: {"condition": "{{ constants.SIGNATURE_VERIFICATION_ENABLED }}", "message": "..."}.
 - tender_agreement_contract_patch             Patch the agreement contract of a bid (PATCH tenders/{id}/agreements/{id}/contracts/{id}); parts: [agreement index, bid index].
 - tender_agreement_document_attach            Attach a document to a tender agreement (POST tenders/{id}/agreements/{id}/documents); parts: [agreement index].
 - tender_agreement_patch                      Patch a tender agreement (PATCH tenders/{id}/agreements/{id}); parts: [agreement index].
 - tender_agreements_get                       Refresh the tender agreements in context (GET tenders/{id}/agreements).
 - tender_award_claim_create                   Create an award claim (POST tenders/{id}/awards/{id}/complaints with type claim); parts: [award index, claim index].
 - tender_award_claim_patch                    Patch an award claim as a role; parts: [award index, claim index, tenderer|complainer].
 - tender_award_claims_get                     List the claims of an award (GET tenders/{id}/awards/{id}/complaints, type claim); parts: [award index].
 - tender_award_complaint_create               Create an award complaint (POST tenders/{id}/awards/{id}/complaints); parts: [award index, complaint index].
 - tender_award_complaint_patch                Patch an award complaint as a role; parts: [award index, complaint index, bot|reviewer|tenderer|complainer].
 - tender_award_complaint_post_create          Post to an award complaint (POST tenders/{id}/awards/{id}/complaints/{id}/posts); parts: [award index, complaint index, post index, reviewer|tenderer|complainer].
 - tender_award_complaints_get                 List the complaints of an award (GET tenders/{id}/awards/{id}/complaints); parts: [award index].
 - tender_award_create                         Create an award (POST tenders/{id}/awards) in limited procedures; parts are a free label.
 - tender_award_document_attach                Attach a document to an award (POST tenders/{id}/awards/{id}/documents); parts: [award index, free label].
 - tender_award_patch                          Patch an award (PATCH tenders/{id}/awards/{id}); parts: [award index]; refreshes awards.
 - tender_awards_get                           Refresh the tender awards in context (GET tenders/{id}/awards).
 - tender_awards_wait_complaint_period         Wait for the end of the complaint period of all awards.
 - tender_awards_wait_edr                      Wait for the EDR identification documents of the awards; runs only with --wait edr-qualification.
 - tender_bid_create                           Create a bid (POST tenders/{id}/bids), uploading the documents listed in it; parts: [bid index]; sets bids[i], bids_tokens[i].
 - tender_bid_document_attach                  Attach a document to a bid (POST tenders/{id}/bids/{id}/documents); parts: [bid index, free label].
 - tender_bid_patch                            Patch a bid (PATCH tenders/{id}/bids/{id}); parts: [bid index].
 - tender_bid_res_post                         Post bid requirement responses (POST tenders/{id}/bids/{id}/requirement_responses); parts: [bid index].
 - tender_bids_get                             Load the tender bids into context (GET tenders/{id}/bids) when they were not created in this run.
 - tender_cancellation_complaint_create        Create a cancellation complaint (POST tenders/{id}/cancellations/{id}/complaints); parts: [cancellation index, complaint index].
 - tender_cancellation_complaint_patch         Patch a cancellation complaint as a role; parts: [cancellation index, complaint index, bot|reviewer|tenderer|complainer].
 - tender_cancellation_complaint_post_create   Post to a cancellation complaint; parts: [cancellation index, complaint index, post index, reviewer|tenderer|complainer].
 - tender_cancellation_complaints_get          List the complaints of a cancellation (GET tenders/{id}/cancellations/{id}/complaints); parts: [cancellation index].
 - tender_cancellation_create                  Create a draft cancellation (POST tenders/{id}/cancellations); parts: [cancellation index]; sets cancellations[i].
 - tender_cancellation_document_attach         Attach a document to a cancellation (POST tenders/{id}/cancellations/{id}/documents); parts: [cancellation index, free label].
 - tender_cancellation_patch                   Patch a cancellation (PATCH tenders/{id}/cancellations/{id}), e.g. to pending or unsuccessful; parts: [cancellation index].
 - tender_cancellation_wait_status             Wait for a cancellation to reach a status: {"status": "active"}; parts: [cancellation index].
 - tender_cancellations_get                    Refresh the tender cancellations in context (GET tenders/{id}/cancellations).
 - tender_claim_create                         Create a tender claim (POST tenders/{id}/complaints with type claim); parts: [claim index].
 - tender_claim_patch                          Patch a tender claim as a role; parts: [claim index, tenderer|complainer].
 - tender_claims_get                           List the tender claims (GET tenders/{id}/complaints, type claim) and refresh them in context.
 - tender_complaint_create                     Create a tender complaint (POST tenders/{id}/complaints); parts: [complaint index].
 - tender_complaint_patch                      Patch a tender complaint as a role; parts: [complaint index, bot|reviewer|tenderer|complainer].
 - tender_complaint_post_create                Post to a tender complaint (POST tenders/{id}/complaints/{id}/posts); parts: [complaint index, post index, reviewer|tenderer|complainer].
 - tender_complaints_get                       List the tender complaints (GET tenders/{id}/complaints) and refresh them in context.
 - tender_contracts_get                        Load the tender contracts into contracts (GET tenders/{id}/contracts, then GET contracts/{id} for each).
 - tender_create                               Create a tender (POST tenders, or POST plans/{id}/tenders when a plan is in context); sets tender, tender_token, tender_config.
 - tender_credentials_patch                    Take over the second stage tender (PATCH tenders/{stage2TenderID}/credentials); the previous tender moves to stage1_tender.
 - tender_criteria_post                        Create tender criteria (POST tenders/{id}/criteria); sets criteria.
 - tender_document_attach                      Attach a document to the tender (POST tenders/{id}/documents); parts are a free label; appends to tender_documents.
 - tender_document_put                         Replace a tender document with a new version (PUT tenders/{id}/documents/{id}); parts: [tender_documents index] or a label, then the last attached document with the same title is replaced.
 - tender_get                                  Refresh the tender in context (GET tenders/{id}).
 - tender_patch                                Patch the tender (PATCH tenders/{id}), for example to switch its status.
 - tender_plan_post                            Connect a plan to the tender (POST tenders/{id}/plans); the data file holds the plan id, e.g. {{ plans[1].id }}.
 - tender_qualification_claim_create           Create a qualification claim (POST tenders/{id}/qualifications/{id}/complaints with type claim); parts: [qualification index, claim index].
 - tender_qualification_claim_patch            Patch a qualification claim as a role; parts: [qualification index, claim index, tenderer|complainer].
 - tender_qualification_claims_get             List the claims of a qualification (GET tenders/{id}/qualifications/{id}/complaints, type claim); parts: [qualification index].
 - tender_qualification_complaint_create       Create a qualification complaint (POST tenders/{id}/qualifications/{id}/complaints); parts: [qualification index, complaint index].
 - tender_qualification_complaint_patch        Patch a qualification complaint as a role; parts: [qualification index, complaint index, bot|reviewer|tenderer|complainer].
 - tender_qualification_complaint_post_create  Post to a qualification complaint (POST tenders/{id}/qualifications/{id}/complaints/{id}/posts); parts: [qualification index, complaint index, post index, reviewer|tenderer|complainer].
 - tender_qualification_complaints_get         List the complaints of a qualification (GET tenders/{id}/qualifications/{id}/complaints); parts: [qualification index].
 - tender_qualification_document_attach        Attach a document to a tender qualification (POST tenders/{id}/qualifications/{id}/documents); parts: [qualification index].
 - tender_qualification_patch                  Patch a tender qualification (PATCH tenders/{id}/qualifications/{id}); parts: [qualification index].
 - tender_qualifications_get                   Refresh the tender qualifications in context (GET tenders/{id}/qualifications).
 - tender_qualifications_wait_edr              Wait for the EDR identification documents of the qualifications; runs only with --wait edr-pre-qualification.
 - tender_question_create                      Ask a tender question (POST tenders/{id}/questions); parts: [question index]; sets questions[i].
 - tender_question_patch                       Answer a tender question (PATCH tenders/{id}/questions/{id}) as the tender owner; parts: [question index].
 - tender_wait_auction                         Wait for the auction participation urls of the active bids; skipped for mode:no-auction submissions.
 - tender_wait_next_check                      Wait for the next chronograph check of the tender (its next_check date), if any.
 - tender_wait_status                          Wait for a tender status: {"status": "x" or [...], "fail_status": "y" (optional), "delay": seconds (default 1)}.
 - wait_date                                   Wait until a date: {"date": "<iso date, templates allowed>", "description": "<optional log text>"}.
 - wait_seconds                                Sleep for a number of seconds: {"seconds": 5}.
```

## Update the README

1. Copy the `.env.readme.example` file to `.env.readme`:

```
cp .env.readme.example .env.readme
```

2. Fill in `.env.readme` with your credentials.

3. Run the script to generate the README:
```
./README.sh
```

## Run the tests

1. Copy the `.env.test.example` file to `.env.test`:

```
cp .env.test.example .env.test
```

2. Fill in `.env.test` with your credentials.

3. Run the tests:

```
pytest
```
