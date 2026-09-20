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
                       [--disable-claims] [--debug] [--debug-req]
                       [--debug-json-level DEBUG_JSON_LEVEL]
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
                         - aboveThreshold.econtract
                         - aboveThreshold.features
                         - aboveThreshold.lcc
                         - aboveThresholdEU
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
[15:42:48] Using env file /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/.env.readme

[15:42:48] Press P to pause and show summary, S to show summary

[15:42:48] Using seed 573191

[15:42:48] Discovered 158 steps in /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/procedure_tools/data/closeFrameworkAgreementUA

[15:42:48] Initializing cdb client

[15:42:48] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[15:42:48] Response status: 200 OK

[15:42:48] Client time delta with server: -604 milliseconds

[15:42:48] Initializing ds client

[15:42:48] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[15:42:48] Response status: 200 OK

[15:42:48] Step 1/158: 0100_plan_create.json

[15:42:48] Creating plan...

[15:42:48] Processing data file: 0100_plan_create.json

[15:42:48] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[15:42:48] Response status: 201 Created

[15:42:48] Plan created:
 - data.id              ec7fe4915e8144378d74a6c4b5a991dc
 - access.token         d3dc542193dc4a20b1c2ec6b5cd86613
 - access.transfer      7e97db4675ee4f27b194bdc66c1a67f7
 - data.status          draft

[15:42:48] Step 2/158: 0110_plan_patch.json

[15:42:48] Patching plan...

[15:42:48] Processing data file: 0110_plan_patch.json

[15:42:48] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/ec7fe4915e8144378d74a6c4b5a991dc?acc_token=d3dc542193dc4a20b1c2ec6b5cd86613
[15:42:48] Response status: 200 OK

[15:42:48] Plan patched:
 - data.id              ec7fe4915e8144378d74a6c4b5a991dc
 - data.status          scheduled

[15:42:48] Step 3/158: 2000_tender_create.json

[15:42:48] Creating tender...

[15:42:48] Processing data file: 2000_tender_create.json

[15:42:48] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/ec7fe4915e8144378d74a6c4b5a991dc/tenders
[15:42:49] Response status: 201 Created

[15:42:49] Tender created:
 - data.id              5dae25aa93044493b3490da1b418cf8c
 - access.token         c7eb6828f80740549cb5949d8a7ea93c
 - access.transfer      0bbdfa49eae44a2a86432f0f8999f087
 - data.status          draft
 - data.tenderID        UA-2026-09-20-000371-a
 - data.procurementMethodType closeFrameworkAgreementUA

[15:42:49] Step 4/158: 2011_tender_document_attach_file.json

[15:42:49] Uploading tender document...

[15:42:49] Processing data file: 2011_tender_document_attach_file.json

[15:42:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:49] Response status: 200 OK

[15:42:49] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/5dae25aa93044493b3490da1b418cf8c/documents?acc_token=c7eb6828f80740549cb5949d8a7ea93c
[15:42:49] Response status: 201 Created

[15:42:49] Document attached:
 - data.id              eda6d1ee728342ad987764ea2c16c443
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/7116024a49e442a584c33d82401022f0?Signature=8mv3lE6tJAkaDxsC8Avinr5ClFVkLO0MbcJ5xA%2BLzLzeKnGm03PpoqyCy464ZYV8Pu1KKugts%2FpgwNZl96YYAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:42:49] Step 5/158: 2013_tender_document_attach_proforma.json

[15:42:49] Uploading tender document...

[15:42:49] Processing data file: 2013_tender_document_attach_proforma.json

[15:42:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:49] Response status: 200 OK

[15:42:49] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/5dae25aa93044493b3490da1b418cf8c/documents?acc_token=c7eb6828f80740549cb5949d8a7ea93c
[15:42:49] Response status: 201 Created

[15:42:49] Document attached:
 - data.id              83cfb8bd16db4d33a4f6aaf63b69efef
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/193ac18d92474f3e9e1cc8b130765ba2?Signature=vw0l8c%2FDZUC9JGgBuAykNB7k%2B4YVybQsCbPP1dDYEQ9sNuQzMiHeItzDlMEippr0C2kM88SbPugXNVrw%2FK80AA%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[15:42:49] Step 6/158: 2014_tender_criteria_post.json

[15:42:49] Creating tender criteria...

[15:42:49] Processing data file: 2014_tender_criteria_post.json

[15:42:49] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/5dae25aa93044493b3490da1b418cf8c/criteria?acc_token=c7eb6828f80740549cb5949d8a7ea93c
[15:42:50] Response status: 201 Created

[15:42:50] Tender criteria created:
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

[15:42:50] Step 7/158: 2016_tender_document_attach_notice.json

[15:42:50] Uploading tender document...

[15:42:50] Processing data file: 2016_tender_document_attach_notice.json

[15:42:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:50] Response status: 200 OK

[15:42:50] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/5dae25aa93044493b3490da1b418cf8c/documents?acc_token=c7eb6828f80740549cb5949d8a7ea93c
[15:42:50] Response status: 201 Created

[15:42:50] Document attached:
 - data.id              87383019ff254ae9a5472c50af33725e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/e7c420f9f6a34674a48c54349603906c?Signature=MMLAVMLu7hkpFnJYZ3lHo%2ByRYzT8gmkyVvb6h%2BYhhzQP%2F0b%2FOZ02Wt8qdcCrKT73IAmtCVwPXKLkE8Q4xY59AQ%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[15:42:50] Step 8/158: 2020_tender_patch.json

[15:42:50] Patching tender...

[15:42:50] Processing data file: 2020_tender_patch.json

[15:42:50] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/5dae25aa93044493b3490da1b418cf8c?acc_token=c7eb6828f80740549cb5949d8a7ea93c
[15:42:50] Response status: 200 OK

[15:42:50] Tender patched:
 - data.id              5dae25aa93044493b3490da1b418cf8c
 - data.status          active.tendering

[15:42:50] Step 9/158: 2030_tender_complaint_create_0.json

[15:42:50] Skipping tender complaint 0: bot and reviewer tokens are required

[15:42:50] Step 10/158: 2031_tender_complaint_create_1.json

[15:42:50] Skipping tender complaint 1: bot and reviewer tokens are required

[15:42:50] Step 11/158: 2032_tender_complaint_create_2.json

[15:42:50] Skipping tender complaint 2: bot and reviewer tokens are required

[15:42:50] Step 12/158: 2033_tender_complaint_create_3.json

[15:42:50] Skipping tender complaint 3: bot and reviewer tokens are required

[15:42:50] Step 13/158: 2034_tender_complaint_create_4.json

[15:42:50] Skipping tender complaint 4: bot and reviewer tokens are required

[15:42:50] Step 14/158: 2035_tender_complaint_create_5.json

[15:42:50] Skipping tender complaint 5: bot and reviewer tokens are required

[15:42:50] Step 15/158: 2040_tender_complaint_patch_0_bot.json

[15:42:50] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[15:42:50] Step 16/158: 2041_tender_complaint_patch_0_reviewer.json

[15:42:50] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[15:42:50] Step 17/158: 2042_tender_complaint_patch_0_reviewer.json

[15:42:50] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[15:42:50] Step 18/158: 2043_tender_complaint_patch_0_tenderer.json

[15:42:50] Skipping tender complaint 0 patch: bot and reviewer tokens are required

[15:42:50] Step 19/158: 2044_tender_complaint_patch_1_bot.json

[15:42:50] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[15:42:50] Step 20/158: 2045_tender_complaint_patch_1_reviewer.json

[15:42:50] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[15:42:50] Step 21/158: 2046_tender_complaint_patch_1_reviewer.json

[15:42:50] Skipping tender complaint 1 patch: bot and reviewer tokens are required

[15:42:50] Step 22/158: 2047_tender_complaint_patch_2_bot.json

[15:42:50] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[15:42:50] Step 23/158: 2048_tender_complaint_patch_2_reviewer.json

[15:42:50] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[15:42:50] Step 24/158: 2049_tender_complaint_patch_2_reviewer.json

[15:42:50] Skipping tender complaint 2 patch: bot and reviewer tokens are required

[15:42:50] Step 25/158: 2050_tender_complaint_patch_3_bot.json

[15:42:50] Skipping tender complaint 3 patch: bot and reviewer tokens are required

[15:42:50] Step 26/158: 2051_tender_complaint_patch_3_reviewer.json

[15:42:50] Skipping tender complaint 3 patch: bot and reviewer tokens are required

[15:42:50] Step 27/158: 2052_tender_complaint_patch_4_complainer.json

[15:42:50] Skipping tender complaint 4 patch: bot and reviewer tokens are required

[15:42:50] Step 28/158: 2201_tender_bid_create_0.json

[15:42:50] Creating bid...

[15:42:50] Processing data file: 2201_tender_bid_create_0.json

[15:42:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:51] Response status: 200 OK

[15:42:51] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:51] Response status: 200 OK

[15:42:51] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:51] Response status: 200 OK

[15:42:51] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:51] Response status: 200 OK

[15:42:51] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:51] Response status: 200 OK

[15:42:51] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/5dae25aa93044493b3490da1b418cf8c/bids
[15:42:51] Response status: 201 Created

[15:42:51] Document attached:
 - data.id              1e53bec06e014727900914ee4f590cb4
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/d0127371d28b47e886215ecd9ff98ee5?Signature=54INELFdjmdUa0RuLVZWDLjWnQhnbzqpFs9CybPRP02LsEq6EH6CRgGCc14QyX6K3YMW5EUWuy3APHTdIdJiAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:42:51] Document attached:
 - data.id              9987f01494584645b91fa58a9b931f18
 - data.confidentiality buyerOnly

[15:42:51] Document attached:
 - data.id              f9b9f66e64ae426db85e0686c9919fdb
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/b8c50c35b1e34a62898bd23dcee041bf?Signature=S5r5AQOUAhifLePDUknXldtmbmmVoALXBzildVQRXebyh0OXFhYjbsTwuAVvvABTDowHMxbAda7oUBFhU%2BCKBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:42:51] Document attached:
 - data.id              c0df4c6564154cecb17cfea2892348f8
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/16544b43fcf64bfdae7594cecb3c9be1?Signature=Z9hVKxjrDKlJFwoODkJMVfK71mF4%2F6Ul0u%2B0arbifdDqpU6e4IFluq2WTD%2Be0wzek1bBV8EMoC3kkvu85W1vBg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:42:51] Document attached:
 - data.id              6d579f487ad741f38364f045e78d1cac
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/15b62f0acac34e0a97cfcb5f41a19bfd?Signature=ZyJHeQPawietBedK6666xsjxJ8KRqgWy%2BJMEYyi0Z2BWrw26aF%2B2jUuXkjkD37Npop2%2B2StoBr%2BWLMEXBO5vCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:42:51] Bid created:
 - data.id              ae105c00e7b3496480d16dd69c73e92e
 - access.token         16e47fe91adc434daeae2ee867678a55
 - data.status          draft

[15:42:51] Step 29/158: 2202_tender_bid_create_1.json

[15:42:51] Creating bid...

[15:42:51] Processing data file: 2202_tender_bid_create_1.json

[15:42:51] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:52] Response status: 200 OK

[15:42:52] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:52] Response status: 200 OK

[15:42:52] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:52] Response status: 200 OK

[15:42:52] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:52] Response status: 200 OK

[15:42:52] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:42:52] Response status: 200 OK

[15:42:52] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/5dae25aa93044493b3490da1b418cf8c/bids
[15:42:52] Response status: 201 Created

[15:42:52] Document attached:
 - data.id              69765bb4cadb4837856c643e2d7284ff
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/36e22e4600b84badbbfb6a8d6fbcf42a?Signature=UQgIPP6XDVMJwh5y9gMqC9mfptzOoVQHbZG3KH6CKYXBFXzUfhkrp9A1VONGohO9bB0H1tRpNFMsPy52S1BjCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:42:52] Document attached:
 - data.id              1b0997c8ec754ca6bb8afb4adc012665
 - data.confidentiality buyerOnly

[15:42:52] Document attached:
 - data.id              010e8395560b43ec8a6f648c1ab8f4aa
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/4d7835377d1348ed8111f1dd76d1051f?Signature=MafMDanRf69YZWB5obWZ9TYXyZ%2BSId3UoQOiUFWWJyQ2%2BZar9KDQAH07P9PRxYBrh7U7nR8qBGj9WkRbGl%2BKDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:42:52] Document attached:
 - data.id              4bd89e3876714b86bf04a5cdb137692d
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/5e4a48a8793048c99b7a9c7a0b62fca2?Signature=GcSS%2B%2Fzn3LLqGIipI%2BQ5j%2F%2BOiwSsc6E7jN26vVl%2F4Ihcvsv90mmxYcsuRcM7BQBIeCKcqWTzOTLXFeI12PquAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:42:52] Document attached:
 - data.id              e37e7f5d8d824b64a8c3cc60ae9ed24c
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/af124b23d92244dea0f72778256ea717?Signature=JtFw%2F4jgd%2F94qSmaq8lKGxzaHLUVkNJ4k1ECRgojnr8ugpJC8VFGBPrUjpcVZwy0X0IeAdEa8kKSubcM6p3aAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:42:52] Bid created:
 - data.id              e27df025fd89496fbce92b40c3688a7f
 - access.token         6f20bb28f88e45159a47e8fdfabd0b7e
 - data.status          draft

[15:42:52] Stopping after 2202_tender_bid_create_1.json

[15:42:52] Completed.

[15:42:52] Summary
 - closeFrameworkAgreementUA	success

```

## procedure-tools

`procedure-tools` creates Prozorro CDB procedures from data folders. There is no procedure specific code path: the data files define the flow. Every `.json` file in a data folder (`procedure_tools/data/<name>`) is one action:

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
 - aboveThreshold.econtract
 - aboveThreshold.features
 - aboveThreshold.lcc
 - aboveThresholdEU
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
