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
[15:50:31] Using env file /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/.env.readme

[15:50:31] Using seed 454109

[15:50:31] Discovered 188 steps in /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/procedure_tools/data/closeFrameworkAgreementUA

[15:50:31] Initializing cdb client

[15:50:31] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[15:50:31] Response status: 200 OK

[15:50:32] Client time delta with server: -1447 milliseconds

[15:50:32] Initializing ds client

[15:50:32] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[15:50:32] Response status: 200 OK

[15:50:32] Step 1/188: 0100_plan_create.json

[15:50:32] Creating plan...

[15:50:32] Processing data file: 0100_plan_create.json

[15:50:32] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[15:50:32] Response status: 201 Created

[15:50:32] Plan created:
 - data.id              7dda60a27b2b40f086e2eca5fb790dbb
 - access.token         55c138876bfc4cb292181e74e8e11a2c
 - access.transfer      6902710e1f9443558e50e2b789464746
 - data.status          draft

[15:50:32] Step 2/188: 0110_plan_patch.json

[15:50:32] Patching plan...

[15:50:32] Processing data file: 0110_plan_patch.json

[15:50:32] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/7dda60a27b2b40f086e2eca5fb790dbb?acc_token=55c138876bfc4cb292181e74e8e11a2c
[15:50:32] Response status: 200 OK

[15:50:32] Plan patched:
 - data.id              7dda60a27b2b40f086e2eca5fb790dbb
 - data.status          scheduled

[15:50:32] Step 3/188: 2000_tender_create.json

[15:50:32] Creating tender...

[15:50:32] Processing data file: 2000_tender_create.json

[15:50:33] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/7dda60a27b2b40f086e2eca5fb790dbb/tenders
[15:50:33] Response status: 201 Created

[15:50:33] Tender created:
 - data.id              78019225fba64309a15f3bccdb1c3ae8
 - access.token         8e16579bfaa44fdf9bafda99297c2d8f
 - access.transfer      6734743242e64156ae2879deeccb3a34
 - data.status          draft
 - data.tenderID        UA-2026-10-27-000089-a
 - data.procurementMethodType closeFrameworkAgreementUA

[15:50:33] Step 4/188: 2011_tender_document_attach_file.json

[15:50:33] Uploading tender document...

[15:50:33] Processing data file: 2011_tender_document_attach_file.json

[15:50:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:33] Response status: 200 OK

[15:50:33] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/documents?acc_token=8e16579bfaa44fdf9bafda99297c2d8f
[15:50:33] Response status: 201 Created

[15:50:33] Document attached:
 - data.id              23126374552d4808bfb3ca5d67f58119
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/c3f4a2869bb445c6883064da6affd8b4?Signature=WWiMNEI6%2BEGehcYqgPV6f3IFuHjyEb0kOgAImEO0wfcT2NC4rtejNNR5BZ%2FydO723%2FaUPXzZdB81qTB8QUYSBQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:50:33] Step 5/188: 2013_tender_document_attach_proforma.json

[15:50:33] Uploading tender document...

[15:50:33] Processing data file: 2013_tender_document_attach_proforma.json

[15:50:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:34] Response status: 200 OK

[15:50:34] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/documents?acc_token=8e16579bfaa44fdf9bafda99297c2d8f
[15:50:34] Response status: 201 Created

[15:50:34] Document attached:
 - data.id              e8dce6959916434faa8e16968630e7fd
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/c02b7aeadde946d59307ec1394c783b2?Signature=%2FtHv9v3ZkUGEp4NjpPHR%2B78Y%2F%2BeZgy9GgmguiqykedfIZljNi5M%2FLdHQjkUcSi%2BEj%2FPbD8Ux6CwY734UwBkmDA%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[15:50:34] Step 6/188: 2014_tender_criteria_post.json

[15:50:34] Creating tender criteria...

[15:50:34] Processing data file: 2014_tender_criteria_post.json

[15:50:34] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/criteria?acc_token=8e16579bfaa44fdf9bafda99297c2d8f
[15:50:34] Response status: 201 Created

[15:50:34] Tender criteria created:
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

[15:50:34] Step 7/188: 2016_tender_document_attach_notice.json

[15:50:34] Uploading tender document...

[15:50:34] Processing data file: 2016_tender_document_attach_notice.json

[15:50:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:35] Response status: 200 OK

[15:50:35] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/documents?acc_token=8e16579bfaa44fdf9bafda99297c2d8f
[15:50:35] Response status: 201 Created

[15:50:35] Document attached:
 - data.id              92c5a3a805594b7c8dd1a16288397bb6
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/60e779aa00ea43c9bcb4274f03b33b4c?Signature=6EuXfVXB4ih58p41EgLlvBpBZZxVzTuwgtYhIzD%2Bm7yqDDYHCJ%2FyvSfyd%2FJ11ezp3%2FI%2Feo0dJYBvrTLgC5DbCQ%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[15:50:35] Step 8/188: 2020_tender_patch.json

[15:50:35] Patching tender...

[15:50:35] Processing data file: 2020_tender_patch.json

[15:50:35] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8?acc_token=8e16579bfaa44fdf9bafda99297c2d8f
[15:50:35] Response status: 200 OK

[15:50:35] Tender patched:
 - data.id              78019225fba64309a15f3bccdb1c3ae8
 - data.status          active.tendering

[15:50:35] Step 9/188: 2021_tender_question_create_0.json

[15:50:35] Creating question 0...

[15:50:35] Processing data file: 2021_tender_question_create_0.json

[15:50:35] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/questions
[15:50:35] Response status: 201 Created

[15:50:35] Question:
 - data.id              60237e2e23984af494db8bc72ce8629f
 - data.questionOf      tender
 - data.title           ЧервʼЯк сумний недолік райком.

[15:50:35] Step 10/188: 2022_tender_question_patch_0.json

[15:50:35] Answering question 0...

[15:50:35] Processing data file: 2022_tender_question_patch_0.json

[15:50:35] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/questions/60237e2e23984af494db8bc72ce8629f?acc_token=8e16579bfaa44fdf9bafda99297c2d8f
[15:50:35] Response status: 200 OK

[15:50:35] Question:
 - data.id              60237e2e23984af494db8bc72ce8629f
 - data.questionOf      tender
 - data.title           ЧервʼЯк сумний недолік райком.
 - data.answer          Податковий місце олівець неправда чоловічок летіти. Рідкий квапливий зарплата.

[15:50:35] Step 11/188: 2023_tender_question_create_1.json

[15:50:35] Creating question 1...

[15:50:35] Processing data file: 2023_tender_question_create_1.json

[15:50:35] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/questions
[15:50:35] Response status: 201 Created

[15:50:35] Question:
 - data.id              880ca0a5f7004e4f83a75ae3e40623c5
 - data.questionOf      item
 - data.title           Спалити полум'я хлопець деякий намір ручка олівець.

[15:50:35] Step 12/188: 2024_tender_question_patch_1.json

[15:50:35] Answering question 1...

[15:50:35] Processing data file: 2024_tender_question_patch_1.json

[15:50:35] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/questions/880ca0a5f7004e4f83a75ae3e40623c5?acc_token=8e16579bfaa44fdf9bafda99297c2d8f
[15:50:36] Response status: 200 OK

[15:50:36] Question:
 - data.id              880ca0a5f7004e4f83a75ae3e40623c5
 - data.questionOf      item
 - data.title           Спалити полум'я хлопець деякий намір ручка олівець.
 - data.answer          Спосіб черговий тьмяний блін. Щось щось навіщо пити набір перед.

[15:50:36] Step 13/188: 2030_tender_complaint_create_0.json

[15:50:36] Skipping tender complaint 0: bot and reviewer tokens are required

[15:50:36] Step 14/188: 2031_tender_complaint_create_1.json

[15:50:36] Skipping tender complaint 1: bot and reviewer tokens are required

[15:50:36] Step 15/188: 2032_tender_complaint_create_2.json

[15:50:36] Skipping tender complaint 2: bot and reviewer tokens are required

[15:50:36] Step 16/188: 2033_tender_complaint_create_3.json

[15:50:36] Skipping tender complaint 3: bot and reviewer tokens are required

[15:50:36] Step 17/188: 2034_tender_complaint_create_4.json

[15:50:36] Creating tender complaint 4...

[15:50:36] Processing data file: 2034_tender_complaint_create_4.json

[15:50:36] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/complaints?acc_token=8e16579bfaa44fdf9bafda99297c2d8f
[15:50:36] Response status: 201 Created

[15:50:36] Complaint created:
 - data.id              69457a052fac4dee973f289086861b6a
 - data.status          draft

[15:50:36] Step 18/188: 2035_tender_complaint_create_5.json

[15:50:36] Creating tender complaint 5...

[15:50:36] Processing data file: 2035_tender_complaint_create_5.json

[15:50:36] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/complaints?acc_token=8e16579bfaa44fdf9bafda99297c2d8f
[15:50:36] Response status: 201 Created

[15:50:36] Complaint created:
 - data.id              546facc8b0e14c4184d88baf7338e0c6
 - data.status          draft

[15:50:36] Step 19/188: 2040_tender_complaint_patch_0_bot.json

[15:50:36] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[15:50:36] Step 20/188: 2041_tender_complaint_post_create_0_0_reviewer.json

[15:50:36] Skipping tender complaint 0 post 0: bot and reviewer tokens are required

[15:50:36] Step 21/188: 2042_tender_complaint_post_create_0_1_complainer.json

[15:50:36] Skipping tender complaint 0 post 1: bot and reviewer tokens are required

[15:50:36] Step 22/188: 2043_tender_complaint_post_create_0_2_reviewer.json

[15:50:36] Skipping tender complaint 0 post 2: bot and reviewer tokens are required

[15:50:36] Step 23/188: 2044_tender_complaint_post_create_0_3_tenderer.json

[15:50:36] Skipping tender complaint 0 post 3: bot and reviewer tokens are required

[15:50:36] Step 24/188: 2045_tender_complaint_patch_0_reviewer.json

[15:50:36] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[15:50:36] Step 25/188: 2046_tender_complaint_patch_0_reviewer.json

[15:50:36] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[15:50:36] Step 26/188: 2047_tender_complaint_patch_0_tenderer.json

[15:50:36] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[15:50:36] Step 27/188: 2048_tender_complaint_patch_1_bot.json

[15:50:36] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[15:50:36] Step 28/188: 2049_tender_complaint_patch_1_reviewer.json

[15:50:36] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[15:50:36] Step 29/188: 2050_tender_complaint_patch_1_reviewer.json

[15:50:36] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[15:50:36] Step 30/188: 2051_tender_complaint_patch_2_bot.json

[15:50:36] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[15:50:36] Step 31/188: 2052_tender_complaint_patch_2_reviewer.json

[15:50:36] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[15:50:36] Step 32/188: 2053_tender_complaint_patch_2_reviewer.json

[15:50:36] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[15:50:36] Step 33/188: 2054_tender_complaint_patch_3_bot.json

[15:50:36] Skipping tender complaint 3 patch: bot and reviewer tokens are required

[15:50:36] Step 34/188: 2055_tender_complaint_patch_3_reviewer.json

[15:50:36] Skipping tender complaint 3 patch: bot and reviewer tokens are required

[15:50:36] Step 35/188: 2056_tender_complaint_patch_4_complainer.json

[15:50:36] Patching tender complaint 4 as complainer...

[15:50:36] Processing data file: 2056_tender_complaint_patch_4_complainer.json

[15:50:36] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/complaints/69457a052fac4dee973f289086861b6a?acc_token=3bc88e7d65b047fba8d60023cce29bc3
[15:50:36] Response status: 200 OK

[15:50:36] Item patched:
 - data.id              69457a052fac4dee973f289086861b6a
 - data.status          mistaken

[15:50:36] Step 36/188: 2201_tender_bid_create_0.json

[15:50:36] Creating bid...

[15:50:36] Processing data file: 2201_tender_bid_create_0.json

[15:50:36] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:36] Response status: 200 OK

[15:50:36] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:37] Response status: 200 OK

[15:50:37] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:37] Response status: 200 OK

[15:50:37] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:37] Response status: 200 OK

[15:50:37] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:37] Response status: 200 OK

[15:50:37] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/bids
[15:50:37] Response status: 201 Created

[15:50:37] Document attached:
 - data.id              fbd79c31711d48d6a37fc8e6d7a4963b
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/e5fc0ad38e7d4d69b4dfba4ed015ced4?Signature=p9pSjQHlSN7vJ%2BFOOFplGf6B4i1p10wAxJsVtk4dDpUVKHg4Fy1Xs8Xg6ApX15TzJWZYpHCHcBh%2BqNnt09HzDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:50:37] Document attached:
 - data.id              6c2dee81031f474cb3923d1d99a9127e
 - data.confidentiality buyerOnly

[15:50:37] Document attached:
 - data.id              0f819ae3dc494906a53c7550243319ee
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/9aa3c3161ca94829b769d8e6d5641ce8?Signature=Dm1wDUlrjJIDMZyayL%2FkO9FKHTIy3zsZKr9ZvAcBE5VDRD6YTFsOvNu7SH5aNpFRT02C9RcERwwicZdQ2WmPCg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:50:37] Document attached:
 - data.id              25093a9738364a97ab119e936451f055
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/4a63356c18274d988ac3fde413860fe5?Signature=4j7CIZlT8sDCUBTtQu2g9AlleKJfk%2Fq%2Fr5JHFqMwfKh8hhWE7IkxqtBPImpPbRQM%2BvwNqZVbC0PWGMRXJPSYDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:50:37] Document attached:
 - data.id              d8d64fcfa5814436954b627a9cbb3832
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/dba79eb50cb845c099f9f9d4c24dd9b0?Signature=0luUUFG06YTtlHgFGEucr9A8JFEGiyov65JXyvc%2BgB83etzNcfzcGnd83XEAuGmFhFDKmZtko9uaDl7rcq4kCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:50:37] Bid created:
 - data.id              813ade5429394565944a073b80fcf73b
 - access.token         7969fd8081db4032accd13e52bcadc45
 - data.status          draft

[15:50:37] Step 37/188: 2202_tender_bid_create_1.json

[15:50:37] Creating bid...

[15:50:37] Processing data file: 2202_tender_bid_create_1.json

[15:50:37] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:37] Response status: 200 OK

[15:50:37] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:38] Response status: 200 OK

[15:50:38] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:38] Response status: 200 OK

[15:50:38] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:38] Response status: 200 OK

[15:50:38] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:50:38] Response status: 200 OK

[15:50:38] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/78019225fba64309a15f3bccdb1c3ae8/bids
[15:50:38] Response status: 201 Created

[15:50:38] Document attached:
 - data.id              7876634cf42543dbb0e244da12973483
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/63cefaaed621402fbae32fd7f87bdd4c?Signature=wRBk37%2BuwxMJTgQosc0lCNZQdATZfP0PN3N5ZBwY3ROPjGv05tN4H4%2FmBSVSKGeDUJE35PK0QcxgVQt%2FrYrwAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:50:38] Document attached:
 - data.id              8a50c1648f4c49b29847c988ffd2fde4
 - data.confidentiality buyerOnly

[15:50:38] Document attached:
 - data.id              2213f5aaca8d46ac9678aa63593677bb
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/d9a52276bb0b4cc3bd3dba1e457ddd3f?Signature=Ktwom4sDvJztiH1VoMxbn6AOXLKvgfnOZdgszVgQW3AGRgVAxJTTNiCHcgA0kFdCgMreRloGZO9r26L2E%2BuNBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:50:38] Document attached:
 - data.id              deb662bcaf0341329c9938ad81cf3697
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/8f4bc38ee46c42f0921703f6983953cd?Signature=4E7nt0JKQ5jrCUs3V36wFUE5TUFbiLlbLbcYxAQ4M9X05bXtZiMSiqQQSBB0EK%2Bh9Sr9T4OgbTn8GDjGav9HAg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:50:38] Document attached:
 - data.id              8ea5f136736d4f96a7d6b11fb98bc16e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/ad514052ffdb4b40a53586b2aed376fc?Signature=3D%2Fr5Q4ri9QQA9D6mfvnP6NMTSO9gO8Rxw8uN8nCVovcd4ITBLOOLIMNxzTlmYBNT1hzT%2FLZpqiU0SKf9rlyAg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:50:38] Bid created:
 - data.id              7fb8867833dc4696a1a9d55e40116e14
 - access.token         5c98ab2759fd42eb838b7fed8261c17f
 - data.status          draft

[15:50:38] Stopping after 2202_tender_bid_create_1.json

[15:50:38] Completed.

[15:50:38] Summary
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
