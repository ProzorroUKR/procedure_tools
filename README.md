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
                       [--disable-data aboveThreshold [aboveThreshold ...]]
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
                         - openTendering.EU
                         - openTendering.EU.econtract
                         - openTendering.UA
                         - openTendering.UA.central
                         - priceQuotation
                         - reporting
                         - reporting.local
                         - requestForProposal
                         - simple.defense
                         - simpleAsset.arma

  --disable-data aboveThreshold [aboveThreshold ...]
                        one or more data folders to skip (env DISABLE_DATA); they stay in the summary as disabled

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

  --debug               Debug log level; also logs the timing of every request (connect, send, wait, download)

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
[08:51:45] Using env file /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/.env.readme

[08:51:45] Using seed 389061

[08:51:45] Discovered 188 steps in /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/procedure_tools/data/closeFrameworkAgreementUA

[08:51:45] Initializing cdb client

[08:51:45] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[08:51:45] Response status: 200 OK

[08:51:46] Client time delta with server: -1147 milliseconds

[08:51:46] Initializing ds client

[08:51:46] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[08:51:46] Response status: 200 OK

[08:51:46] Step 1/188: 0100_plan_create.json

[08:51:46] Creating plan...

[08:51:46] Processing data file: 0100_plan_create.json

[08:51:46] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[08:51:46] Response status: 201 Created

[08:51:46] Plan created:
 - data.id              68d94137de1147ac960414c632ac23c1
 - access.token         cec1b960cc0e4f6bac71cd5e7f5b8fb6
 - access.transfer      b46a0e0be5bf437895d2adae3c85d35f
 - data.status          draft

[08:51:46] Step 2/188: 0110_plan_patch.json

[08:51:46] Patching plan...

[08:51:46] Processing data file: 0110_plan_patch.json

[08:51:46] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/68d94137de1147ac960414c632ac23c1?acc_token=cec1b960cc0e4f6bac71cd5e7f5b8fb6
[08:51:46] Response status: 200 OK

[08:51:46] Plan patched:
 - data.id              68d94137de1147ac960414c632ac23c1
 - data.status          scheduled

[08:51:46] Step 3/188: 2000_tender_create.json

[08:51:46] Creating tender...

[08:51:46] Processing data file: 2000_tender_create.json

[08:51:46] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/68d94137de1147ac960414c632ac23c1/tenders
[08:51:46] Response status: 201 Created

[08:51:46] Tender created:
 - data.id              1cb2fe0ff2134942a0da50629f4eb4c3
 - access.token         79dd14419e254471819bd613d798d970
 - access.transfer      e21a8005fd08436a902165af9283a92c
 - data.status          draft
 - data.tenderID        UA-2026-11-09-000002-a
 - data.procurementMethodType closeFrameworkAgreementUA

[08:51:46] Step 4/188: 2011_tender_document_attach_file.json

[08:51:46] Uploading tender document...

[08:51:46] Processing data file: 2011_tender_document_attach_file.json

[08:51:46] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:47] Response status: 200 OK

[08:51:47] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/documents?acc_token=79dd14419e254471819bd613d798d970
[08:51:47] Response status: 201 Created

[08:51:47] Document attached:
 - data.id              31466fb2e3404c57943fb88896fcc065
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/ed523aa071284dd1826f992b12c55193?Signature=fvqunHzksuTXacpEuC0iUKEI3%2FcaFuTKacajv%2FCdZkdNYsFSuoh7FOdMKuplnT2wRiIoVKCcxxA4hVgAWnRpAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[08:51:47] Step 5/188: 2013_tender_document_attach_proforma.json

[08:51:47] Uploading tender document...

[08:51:47] Processing data file: 2013_tender_document_attach_proforma.json

[08:51:47] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:47] Response status: 200 OK

[08:51:47] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/documents?acc_token=79dd14419e254471819bd613d798d970
[08:51:47] Response status: 201 Created

[08:51:47] Document attached:
 - data.id              34a82603d9fc486f978de52d2c7385ab
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/69740979d4f74aba87ba08a16dca752b?Signature=%2BYriiQ33vmaqZ7a8ygRWT14WJQWy%2Fxmb91uCIa5rZ8DSwBLZ%2FyRwZoEnJbnvNcwVELz%2Bw%2FHXO4FpPkdk%2FfOpCQ%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[08:51:47] Step 6/188: 2014_tender_criteria_post.json

[08:51:47] Creating tender criteria...

[08:51:47] Processing data file: 2014_tender_criteria_post.json

[08:51:47] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/criteria?acc_token=79dd14419e254471819bd613d798d970
[08:51:47] Response status: 201 Created

[08:51:47] Tender criteria created:
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

[08:51:47] Step 7/188: 2016_tender_document_attach_notice.json

[08:51:47] Uploading tender document...

[08:51:47] Processing data file: 2016_tender_document_attach_notice.json

[08:51:47] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:48] Response status: 200 OK

[08:51:48] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/documents?acc_token=79dd14419e254471819bd613d798d970
[08:51:48] Response status: 201 Created

[08:51:48] Document attached:
 - data.id              7465b98dce504c4e94f4fb87d382da62
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/aa763211679745a294b789350ba6a116?Signature=4MeKg10x5H%2BWqZV%2FBL0CrpcT2Mci4p2zeje7OdEb5Y2FPC4R%2B5oTrY0mjBpmy0lPFsAC7G%2FdgVD4Lq5UQzxUBg%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[08:51:48] Step 8/188: 2020_tender_patch.json

[08:51:48] Patching tender...

[08:51:48] Processing data file: 2020_tender_patch.json

[08:51:48] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3?acc_token=79dd14419e254471819bd613d798d970
[08:51:48] Response status: 200 OK

[08:51:48] Tender patched:
 - data.id              1cb2fe0ff2134942a0da50629f4eb4c3
 - data.status          active.tendering

[08:51:48] Step 9/188: 2021_tender_question_create_0.json

[08:51:48] Creating question 0...

[08:51:48] Processing data file: 2021_tender_question_create_0.json

[08:51:48] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/questions
[08:51:48] Response status: 201 Created

[08:51:48] Question:
 - data.id              1c45579ad8c44a5e8db698215bb0074c
 - data.questionOf      tender
 - data.title           Плід зміна здригнутися летіти встати звільнення.

[08:51:48] Step 10/188: 2022_tender_question_patch_0.json

[08:51:48] Answering question 0...

[08:51:48] Processing data file: 2022_tender_question_patch_0.json

[08:51:48] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/questions/1c45579ad8c44a5e8db698215bb0074c?acc_token=79dd14419e254471819bd613d798d970
[08:51:48] Response status: 200 OK

[08:51:48] Question:
 - data.id              1c45579ad8c44a5e8db698215bb0074c
 - data.questionOf      tender
 - data.title           Плід зміна здригнутися летіти встати звільнення.
 - data.answer          Прірва порт ніч господиня виблискувати ланцюжок тисяча. Єврейський гуляти хотіти природний.

[08:51:48] Step 11/188: 2023_tender_question_create_1.json

[08:51:48] Creating question 1...

[08:51:48] Processing data file: 2023_tender_question_create_1.json

[08:51:48] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/questions
[08:51:48] Response status: 201 Created

[08:51:48] Question:
 - data.id              25053f410f4245b9b2ae1c4231323697
 - data.questionOf      item
 - data.title           Незручно неправда палець провал надати що тривога вітрина.

[08:51:48] Step 12/188: 2024_tender_question_patch_1.json

[08:51:48] Answering question 1...

[08:51:48] Processing data file: 2024_tender_question_patch_1.json

[08:51:48] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/questions/25053f410f4245b9b2ae1c4231323697?acc_token=79dd14419e254471819bd613d798d970
[08:51:48] Response status: 200 OK

[08:51:48] Question:
 - data.id              25053f410f4245b9b2ae1c4231323697
 - data.questionOf      item
 - data.title           Незручно неправда палець провал надати що тривога вітрина.
 - data.answer          Порт відповідність розгубитися.

[08:51:48] Step 13/188: 2030_tender_complaint_create_0.json

[08:51:48] Skipping tender complaint 0: bot and reviewer tokens are required

[08:51:48] Step 14/188: 2031_tender_complaint_create_1.json

[08:51:48] Skipping tender complaint 1: bot and reviewer tokens are required

[08:51:48] Step 15/188: 2032_tender_complaint_create_2.json

[08:51:48] Skipping tender complaint 2: bot and reviewer tokens are required

[08:51:48] Step 16/188: 2033_tender_complaint_create_3.json

[08:51:48] Skipping tender complaint 3: bot and reviewer tokens are required

[08:51:48] Step 17/188: 2034_tender_complaint_create_4.json

[08:51:48] Creating tender complaint 4...

[08:51:48] Processing data file: 2034_tender_complaint_create_4.json

[08:51:48] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/complaints?acc_token=79dd14419e254471819bd613d798d970
[08:51:48] Response status: 201 Created

[08:51:48] Complaint created:
 - data.id              632fb20cfe83441c86d44cfda0412331
 - data.status          draft

[08:51:48] Step 18/188: 2035_tender_complaint_create_5.json

[08:51:48] Creating tender complaint 5...

[08:51:48] Processing data file: 2035_tender_complaint_create_5.json

[08:51:48] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/complaints?acc_token=79dd14419e254471819bd613d798d970
[08:51:49] Response status: 201 Created

[08:51:49] Complaint created:
 - data.id              9140750e596b486bac641fff0be4c479
 - data.status          draft

[08:51:49] Step 19/188: 2040_tender_complaint_patch_0_bot.json

[08:51:49] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[08:51:49] Step 20/188: 2041_tender_complaint_post_create_0_0_reviewer.json

[08:51:49] Skipping tender complaint 0 post 0: bot and reviewer tokens are required

[08:51:49] Step 21/188: 2042_tender_complaint_post_create_0_1_complainer.json

[08:51:49] Skipping tender complaint 0 post 1: bot and reviewer tokens are required

[08:51:49] Step 22/188: 2043_tender_complaint_post_create_0_2_reviewer.json

[08:51:49] Skipping tender complaint 0 post 2: bot and reviewer tokens are required

[08:51:49] Step 23/188: 2044_tender_complaint_post_create_0_3_tenderer.json

[08:51:49] Skipping tender complaint 0 post 3: bot and reviewer tokens are required

[08:51:49] Step 24/188: 2045_tender_complaint_patch_0_reviewer.json

[08:51:49] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[08:51:49] Step 25/188: 2046_tender_complaint_patch_0_reviewer.json

[08:51:49] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[08:51:49] Step 26/188: 2047_tender_complaint_patch_0_tenderer.json

[08:51:49] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[08:51:49] Step 27/188: 2048_tender_complaint_patch_1_bot.json

[08:51:49] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[08:51:49] Step 28/188: 2049_tender_complaint_patch_1_reviewer.json

[08:51:49] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[08:51:49] Step 29/188: 2050_tender_complaint_patch_1_reviewer.json

[08:51:49] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[08:51:49] Step 30/188: 2051_tender_complaint_patch_2_bot.json

[08:51:49] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[08:51:49] Step 31/188: 2052_tender_complaint_patch_2_reviewer.json

[08:51:49] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[08:51:49] Step 32/188: 2053_tender_complaint_patch_2_reviewer.json

[08:51:49] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[08:51:49] Step 33/188: 2054_tender_complaint_patch_3_bot.json

[08:51:49] Skipping tender complaint 3 patch: bot and reviewer tokens are required

[08:51:49] Step 34/188: 2055_tender_complaint_patch_3_reviewer.json

[08:51:49] Skipping tender complaint 3 patch: bot and reviewer tokens are required

[08:51:49] Step 35/188: 2056_tender_complaint_patch_4_complainer.json

[08:51:49] Patching tender complaint 4 as complainer...

[08:51:49] Processing data file: 2056_tender_complaint_patch_4_complainer.json

[08:51:49] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/complaints/632fb20cfe83441c86d44cfda0412331?acc_token=0bdaaf3b28034757b172425b74ee20ae
[08:51:49] Response status: 200 OK

[08:51:49] Item patched:
 - data.id              632fb20cfe83441c86d44cfda0412331
 - data.status          mistaken

[08:51:49] Step 36/188: 2201_tender_bid_create_0.json

[08:51:49] Creating bid...

[08:51:49] Processing data file: 2201_tender_bid_create_0.json

[08:51:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:49] Response status: 200 OK

[08:51:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:49] Response status: 200 OK

[08:51:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:49] Response status: 200 OK

[08:51:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:50] Response status: 200 OK

[08:51:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:50] Response status: 200 OK

[08:51:50] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/bids
[08:51:50] Response status: 201 Created

[08:51:50] Document attached:
 - data.id              0ff051b8deef4461b800dc64dcfd0045
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/7f05e2a478d74a0382c68cab6e3e3246?Signature=PeyOw%2FLO0YQUtjQcrd8vrdG6NjV1gvS7PsmmT2uLcBGRsuhO%2FbjwrYF5zxEFmVkosJ0zCvoPlY0fSpuIL7GmCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[08:51:50] Document attached:
 - data.id              d6cd12ef85884730ac3ee262c0bee757
 - data.confidentiality buyerOnly

[08:51:50] Document attached:
 - data.id              65655ded218741b7a8749c9d51200a43
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/cd582e3e9ca6436b88525bc86d4f1ce7?Signature=pRCbpZJEQ1ZQsl0MJvKAJCR2c4ijjwbx4igmIom5b6G2Fz8YCvIgoGMM48adN5%2FTlUxyuQJAJZIR3EsR%2BAzNBg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[08:51:50] Document attached:
 - data.id              c55e855fc4ff4632b4b4aa9a89202e18
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/56195d3fc90b4e3ab882d462cfd8f4c7?Signature=%2FEdY7dV86IB%2BjwlrVYLxhmIA8MhpEjN3%2Blq3gip0jwrB0AOkV87%2B42toGYwdIZuEMrrYYtHT5kY28LPQZpSkBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[08:51:50] Document attached:
 - data.id              1ebe95a9e3f14bbba0d0c2a00a3b10d2
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/a7738449bcf1474caaa6372e8da91840?Signature=afSv76KUHl%2BrmrtBjVwVThRzhy9gd%2B2gbGbhhraRxxMAF%2B%2FHVFQxQtcSxKrtnNVKFmFDgum4Xj%2BgrdNojYRdBQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[08:51:50] Bid created:
 - data.id              92a70eb442f44398a84c21e3f66a2df1
 - access.token         aab56ecd81784162817adbcd75cecea9
 - data.status          draft

[08:51:50] Step 37/188: 2202_tender_bid_create_1.json

[08:51:50] Creating bid...

[08:51:50] Processing data file: 2202_tender_bid_create_1.json

[08:51:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:50] Response status: 200 OK

[08:51:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:50] Response status: 200 OK

[08:51:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:50] Response status: 200 OK

[08:51:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:50] Response status: 200 OK

[08:51:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[08:51:51] Response status: 200 OK

[08:51:51] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cb2fe0ff2134942a0da50629f4eb4c3/bids
[08:51:51] Response status: 201 Created

[08:51:51] Document attached:
 - data.id              e395354611c74c04932c5669a9ab1bb5
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/ce252d862e0444cbb7569a207a833350?Signature=PxS8E6UeweDeVzO5%2BEHZW4O1Dp40FJxqTWfKWUuVFyxZfdMPthKFeD%2BW7hN%2FUnJP4Z5E96M9uf%2B6CqGC5oowCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[08:51:51] Document attached:
 - data.id              5b7316b4b3af47bdbb76485c226bd363
 - data.confidentiality buyerOnly

[08:51:51] Document attached:
 - data.id              0dd67dcb0e5247c9be48238011fc4e27
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/4eef62841f66419a9d0b36ab802f505f?Signature=zmlL12pVD4DSwm1C6MyiadCJ4l604%2BiuOTSciDhmiC5BvslP5dJ8cMmxlHi%2BjboxRFZzr%2Bn3NK8zF7rP7IY%2BCg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[08:51:51] Document attached:
 - data.id              098fa0a54fdd46478f7622b9a95f457b
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/fc0d5aa224b54811be3bca946ec4e494?Signature=hLxPcRvLYE4fPl7cQ%2FwVerspriGi904o%2FSS6R2YP4GtRwOStA0D6No0upXTaIDgaPIvmYrhOuRd%2BYrUZcj5eCQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[08:51:51] Document attached:
 - data.id              0693e73232d7487d859f093956a2fe2a
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/611a912cdb92491f897ce758c5f9e0b9?Signature=raT14fiOpExD%2BlkXr8k8FuvcczyHjxHVt24qrpE2TGjX%2FZrCqKMe%2Ftw4Fwy%2B7b8f1xp%2BCDLF4o3hlDc0m9hHBg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[08:51:51] Bid created:
 - data.id              d0d62ecfed8a4c9ab2b17dfd7f6fe9f9
 - access.token         faf1832cf7b744d78a2b8cb578e65c9b
 - data.status          draft

[08:51:51] Stopping after 2202_tender_bid_create_1.json

[08:51:51] Completed.

[08:51:51] Summary
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

An unknown action name fails before anything is sent to the API and prints the available actions. `--stop` and `--pause` take a step file name (with or without its number), `--wait` enables the EDR waits, `--parallel` runs several data folders at once, `--disable-data` (env `DISABLE_DATA`) leaves the listed folders out of a run and shows them as `disabled` in the summary.

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
 - openTendering.EU
 - openTendering.EU.econtract
 - openTendering.UA
 - openTendering.UA.central
 - priceQuotation
 - reporting
 - reporting.local
 - requestForProposal
 - simple.defense
 - simpleAsset.arma
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
