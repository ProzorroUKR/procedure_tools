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

3. Install with pip or uv

### Install with pip:

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

### Install with uv:

    * vanilla:

    ```
    uv sync
    ```

    * with color requirements:

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
usage: procedure [-h] [-v] [-E sandbox] [--host HOST] [--token TOKEN]
                 [--ds-host DS_HOST] [--ds-username DS_USERNAME]
                 [--ds-password DS_PASSWORD] [-a 460800] [-p /api/0/]
                 [-d aboveThresholdUA [aboveThresholdUA ...]] [--parallel [N]]
                 [-m quick(mode:no-auction)] [-s tender_create.json]
                 [--pause tender_create.json [tender_create.json ...]]
                 [-w edr-qualification [edr-qualification ...]] [-e SEED]
                 [--reviewer-token REVIEWER_TOKEN] [--bot-token BOT_TOKEN]
                 [--debug] [--debug-req] [--debug-json-level DEBUG_JSON_LEVEL]
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

  -d aboveThresholdUA [aboveThresholdUA ...], --data aboveThresholdUA [aboveThresholdUA ...]
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
procedure --env sandbox --data closeFrameworkAgreementUA
procedure --env .env.dev --data closeFrameworkAgreementUA
PROCEDURE_ENV=sandbox procedure --data closeFrameworkAgreementUA
```

Override selected values from the command line:

```
procedure --env sandbox --token other_token --data closeFrameworkAgreementUA
```

## Usage examples

### With an env file

Create with the default data:
```
procedure --env sandbox --data=closeFrameworkAgreementUA
```

Create with the default data and stop after a specific data file:
```
procedure --env sandbox --data=closeFrameworkAgreementUA --stop=bid_create_3.json
```

Create with custom data files (relative path):
```
procedure --env sandbox --data=customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path):
```
procedure --env sandbox --data=/Users/JohnDoe/customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path, Windows):
```
procedure --env sandbox --data=C:\Users\JohnDoe\customdata\closeFrameworkAgreementUA
```

### Without an env file

Create with the default data:
```
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA
```

Create with the default data and stop after a specific data file:
```
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA --stop=bid_create_3.json
```

Create with custom data files (relative path):
```
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path):
```
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=/Users/JohnDoe/customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path, Windows):
```
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=C:\Users\JohnDoe\customdata\closeFrameworkAgreementUA
```

## Output example
```
procedure --env sandbox --data=closeFrameworkAgreementUA --stop=bid_create_4.json
```
```
[14:24:21] Using env file /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/.env.readme

[14:24:21] Press P to pause and show summary, S to show summary

[14:24:21] Using seed 132865

[14:24:21] Initializing cdb client

[14:24:21] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[14:24:22] Response status: 200 OK

[14:24:22] Client time delta with server: -445 milliseconds

[14:24:22] Initializing ds client

[14:24:22] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[14:24:22] Response status: 200 OK

[14:24:22] Creating framework...

[14:24:22] Processing data file: framework_create.json

[14:24:22] Skipping...

[14:24:22] Creating plan...

[14:24:22] Processing data file: plan_create.json

[14:24:22] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[14:24:22] Response status: 201 Created

[14:24:22] Plan created:
 - data.id              ad74dd40639e403abafa68f76e3a35bb
 - access.token         303d5956fc78412f8778651f3cfc763e
 - access.transfer      3b21496d15364811896be4b577273cda
 - data.status          draft

[14:24:22] Patching plan...

[14:24:22] Processing data file: plan_patch.json

[14:24:22] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/ad74dd40639e403abafa68f76e3a35bb?acc_token=303d5956fc78412f8778651f3cfc763e
[14:24:22] Response status: 200 OK

[14:24:22] Plan patched:
 - data.id              ad74dd40639e403abafa68f76e3a35bb
 - data.status          scheduled

[14:24:22] Creating tender...

[14:24:22] Processing data file: tender_create.json

[14:24:22] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/ad74dd40639e403abafa68f76e3a35bb/tenders
[14:24:23] Response status: 201 Created

[14:24:23] Tender created:
 - data.id              ca1d43e2e74c4f5aa9ca9848b1ec156e
 - access.token         1987eadedb064acfa28510554cee7b86
 - access.transfer      635094c88f5c43c2a12d1da70009dccf
 - data.status          draft
 - data.tenderID        UA-2026-09-15-000006-a
 - data.procurementMethodType closeFrameworkAgreementUA

[14:24:23] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/ca1d43e2e74c4f5aa9ca9848b1ec156e
[14:24:23] Response status: 200 OK

[14:24:23] Processing data file: tender_document_attach.json

[14:24:23] Processing data file: tender_document_file.txt

[14:24:23] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:23] Response status: 200 OK

[14:24:23] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/ca1d43e2e74c4f5aa9ca9848b1ec156e/documents?acc_token=1987eadedb064acfa28510554cee7b86
[14:24:23] Response status: 201 Created

[14:24:23] Document attached:
 - data.id              abd916c311644ab98724f0c67056a3d8
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/c30b0e8a933c4eccaa065becfe87f3f6?Signature=%2BoQz6H7afJf7%2BqWe9Q0qNxz7Iqv0hbHMLdpy7NOF8nEsyj9koLPXPJPmpqaUcr8vyq2U0%2F0YfPRwSjZuVtXBDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:23] Processing data file: contract_proforma_attach.json

[14:24:23] Processing data file: contract_proforma.txt

[14:24:23] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:24] Response status: 200 OK

[14:24:24] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/ca1d43e2e74c4f5aa9ca9848b1ec156e/documents?acc_token=1987eadedb064acfa28510554cee7b86
[14:24:24] Response status: 201 Created

[14:24:24] Document attached:
 - data.id              c9caeb519b644cedaa5214eeba82b5b8
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/61b01615bad045799198940ec57ad658?Signature=c5c3TDD0znNZ5wnr2bBIQAyRm2ap2tgNYe5N2aKOZXewG8wtMId4PjZlcdOMZkZFzs4ZT7W79kT0vHZo2Um1AA%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[14:24:24] Create tender criteria...

[14:24:24] Processing data file: criteria_create.json

[14:24:24] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/ca1d43e2e74c4f5aa9ca9848b1ec156e/criteria?acc_token=1987eadedb064acfa28510554cee7b86
[14:24:24] Response status: 201 Created

[14:24:24] Tender criteria created:
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

[14:24:24] Processing data file: tender_notice_attach.json

[14:24:24] Processing data file: tender_notice_file.p7s

[14:24:24] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:24] Response status: 200 OK

[14:24:24] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/ca1d43e2e74c4f5aa9ca9848b1ec156e/documents?acc_token=1987eadedb064acfa28510554cee7b86
[14:24:24] Response status: 201 Created

[14:24:24] Document attached:
 - data.id              112c1dbab41445198657f41c7d5c032f
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/db50128c2f9b4aa8a5c493999c625982?Signature=apxMRlYlCPbN6zV11fjwmEevCTIWzoGUqwQxFtZFW1lAq0Ew8ATM5bxiYLC4dAfk5lVPH6tangO5TqQxWScODA%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[14:24:24] Patching tender...

[14:24:24] Processing data file: tender_patch.json

[14:24:24] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/ca1d43e2e74c4f5aa9ca9848b1ec156e?acc_token=1987eadedb064acfa28510554cee7b86
[14:24:25] Response status: 200 OK

[14:24:25] Tender patched:
 - data.id              ca1d43e2e74c4f5aa9ca9848b1ec156e
 - data.status          active.tendering

[14:24:25] Skipping complaints creating: bot and reviewer tokens are required

[14:24:25] Creating bids...

[14:24:25] Processing data file: bid_create_0.json

[14:24:25] Processing data file: bid_document_file.txt

[14:24:25] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:25] Response status: 200 OK

[14:24:25] Processing data file: bid_confidential_document_file.txt

[14:24:25] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:25] Response status: 200 OK

[14:24:25] Processing data file: bid_eligibility_document_file.txt

[14:24:25] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:25] Response status: 200 OK

[14:24:25] Processing data file: bid_financial_document_file.txt

[14:24:25] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:26] Response status: 200 OK

[14:24:26] Processing data file: bid_qualification_document_file.txt

[14:24:26] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:26] Response status: 200 OK

[14:24:26] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/ca1d43e2e74c4f5aa9ca9848b1ec156e/bids
[14:24:26] Response status: 201 Created

[14:24:26] Document attached:
 - data.id              36bcac72410b4d4aba84b476291c11d3
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/b0b188fca853452c8b03d5826584343c?Signature=XQ7pztpqSL97x62lE1NsIR3yABrWIlMmRZi%2ByCavgeCjwQXKvGprA6hvfV1X3ATz62Mq1ZkXvf%2B2z6u8P9XkDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:26] Document attached:
 - data.id              9c1ffd3796944eb0bd292ee0cd750d73
 - data.confidentiality buyerOnly

[14:24:26] Document attached:
 - data.id              38bd74d0b5cb408cb7ff545d786365ef
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/e763d999792548cc948871eb23164838?Signature=TPkEGPZ63z%2BXqgp44Yz0zeAVAHyCmNrNnVk3FSl%2FQRYXNuNcdDUciMVaveKge1WHQvJbg7HpsbaiWShgjXsgBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:26] Document attached:
 - data.id              971badd14b1c42f8bb3a07f658725e93
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/a97e07af6dc844e2892dbef381c07e37?Signature=B9T8cu2QAUNpm28kXoH33g1K8SXOMh9ogCWs9ZqjszWsvjez1n7gRn0v5QecWnHJ%2Bkl1msAXdgViTMPi2Q%2F6Bg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:26] Document attached:
 - data.id              f413551441b543e28471599d18115884
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/ecca82e1c8ac46c69fdd96fa3859c627?Signature=O8YgLTRWhkr84blozl2HwyrsCN2f1%2BwKCvd91G%2BEJi4%2B7%2FFmBjvdruroOcV86sCATFP7B88MD9xJwaD61zYgAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:26] Bid created:
 - data.id              4866e95f09154ccc855d26cbfa3e89c5
 - access.token         5fe949699d474bb1aaa30745d85574dd
 - data.status          draft

[14:24:26] Processing data file: bid_create_1.json

[14:24:26] Processing data file: bid_document_file.txt

[14:24:26] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:26] Response status: 200 OK

[14:24:26] Processing data file: bid_confidential_document_file.txt

[14:24:26] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:26] Response status: 200 OK

[14:24:26] Processing data file: bid_eligibility_document_file.txt

[14:24:26] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:26] Response status: 200 OK

[14:24:26] Processing data file: bid_financial_document_file.txt

[14:24:26] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:26] Response status: 200 OK

[14:24:26] Processing data file: bid_qualification_document_file.txt

[14:24:26] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:27] Response status: 200 OK

[14:24:27] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/ca1d43e2e74c4f5aa9ca9848b1ec156e/bids
[14:24:27] Response status: 201 Created

[14:24:27] Document attached:
 - data.id              9bee78efbb264c23a7a700ee2eca7c27
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/fec836bc2c68450a8813d6ceb0060330?Signature=So58X8BW1EC9F%2BIbypeERJNit68aFeotvm3W6mSzS9aPp3QPBU61zv3LWQ4FodD3nklFJJlkVukU7x0ZUUPSDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:27] Document attached:
 - data.id              0b8468d740ff4dce8935ecdbd80e737d
 - data.confidentiality buyerOnly

[14:24:27] Document attached:
 - data.id              19e1347f2efc44789737f40689b73536
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/f4f5339620fd47339cbd3fff4c74d11d?Signature=EMz0O3xuOcUcjOuvbISTRHedRNalaPmImRaZJq11bCWmsyofPZDJYrHsgQ8BKjWzpQNzeFstpWk9dM56nfm5AQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:27] Document attached:
 - data.id              bc04e97391614d3382a519200afbdd1b
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/f68a52bd05e64b42898f0ed0535f8c0d?Signature=QEMRtxSEVUVhxLrr63HJM2v3caJrMhaDg41PvCJ2x6WvxxCyBktQS8pXQBtIZAZBPnyqDNZq4QEEIkNONEKpAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:27] Document attached:
 - data.id              5185a2cebf794362a2c3cafbbd228a7e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/06121714122949baaf87b7dce0fbaeee?Signature=q2DqQkkbVcC%2BYG9s60COpoXgCvKbsM7qwyTHb6LGaD%2BVESWVFHh1NpjH1NTHiTYmboyqdDbi%2B4s9a26R6GKkBw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:27] Bid created:
 - data.id              d23572c9d25847f0993b0571c6a30e81
 - access.token         d2ff911e97ff4bd0abb4b84b79d25dc7
 - data.status          draft

[14:24:27] Processing data file: bid_create_2.json

[14:24:27] Processing data file: bid_document_file.txt

[14:24:27] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:27] Response status: 200 OK

[14:24:27] Processing data file: bid_confidential_document_file.txt

[14:24:27] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:27] Response status: 200 OK

[14:24:27] Processing data file: bid_eligibility_document_file.txt

[14:24:27] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:27] Response status: 200 OK

[14:24:27] Processing data file: bid_financial_document_file.txt

[14:24:27] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:27] Response status: 200 OK

[14:24:27] Processing data file: bid_qualification_document_file.txt

[14:24:27] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:28] Response status: 200 OK

[14:24:28] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/ca1d43e2e74c4f5aa9ca9848b1ec156e/bids
[14:24:28] Response status: 201 Created

[14:24:28] Document attached:
 - data.id              c27a077968dc4b3ebddf82a6b2c5c908
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/753aff4635d64a6f9528200f330e6210?Signature=hEwDkejUIP%2FScrUju13biGFcSNJkXS8wMbXSrlrDjkSZ1DYuSsChCdVjA4F7d7sS11dNxYqSQpeu8bFV6i0KAA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:28] Document attached:
 - data.id              a80200da0350412fa17c780a1d6f5039
 - data.confidentiality buyerOnly

[14:24:28] Document attached:
 - data.id              860797d6c6e54f14b4c911eefb633bae
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/8920f883f0774ed4a02e915f1ed72452?Signature=HptrWPJWR%2BWR%2BYwmGCjsgVJbAhTzSVCYWOBnKGVHK%2BmiVx741m7lRzqiu1ofl3F8aDwMu4slN3kIwPyTtRRyCQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:28] Document attached:
 - data.id              db4574ab943c449aa9812012f63944af
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/3a81aa7d37c84136adc7b2be3477dac6?Signature=1AtTClVoxAnd34zWDtcIxYugWaZddlFzznJ0dnE%2BB9mDgmoVA2GCpFLM8EakMA80jxa2VO1EPIblCJQjLZcYDQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:28] Document attached:
 - data.id              0ce3beaf4e674dbc82b4f4a0f4f7e805
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/be39f0290f5d4a6eaa17ba5d5862f00d?Signature=1noiDZCjF0u1OgNF%2F9N8jdMLPJbHBlLD5OUPXSkEI6kUQSb2SJoUjGTt0wgY9rkMWLIE8ONxdT7UyD2mQYJSCA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:28] Bid created:
 - data.id              9dc1795341e2443baa0b69a0296d8428
 - access.token         e54e6b0ad22e465c96af2afcd7067363
 - data.status          draft

[14:24:28] Processing data file: bid_create_3.json

[14:24:28] Processing data file: bid_document_file.txt

[14:24:28] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:28] Response status: 200 OK

[14:24:28] Processing data file: bid_confidential_document_file.txt

[14:24:28] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:28] Response status: 200 OK

[14:24:28] Processing data file: bid_eligibility_document_file.txt

[14:24:28] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:28] Response status: 200 OK

[14:24:28] Processing data file: bid_financial_document_file.txt

[14:24:28] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:28] Response status: 200 OK

[14:24:28] Processing data file: bid_qualification_document_file.txt

[14:24:28] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[14:24:29] Response status: 200 OK

[14:24:29] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/ca1d43e2e74c4f5aa9ca9848b1ec156e/bids
[14:24:29] Response status: 201 Created

[14:24:29] Document attached:
 - data.id              a895ff8a7ebd4dafa343e5b4239abfdb
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/ebd6be6955e841d8899670503b8f3dc5?Signature=CfNiul2INP5VgyEYjWp4KdgQp15sPUCL2xxiLeX%2F53gOeU6FY1HklmKxTvpPkAPwLt160vmOB104GZgRefrUAA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:29] Document attached:
 - data.id              d9c94d0fc7a44521977b67cfd3536e12
 - data.confidentiality buyerOnly

[14:24:29] Document attached:
 - data.id              8f8d44301e754eaaa506dbbcabb7a882
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/24e772e6c26849c298585ce8e9d4eb0f?Signature=KkuJGL7owkPhnym8UPJl5G5sah0Ni7IHaDbjRoQB2XbcM6MT1c%2Ffx2OQadmDLPyl994xMofvSRTRmTDMm9%2FUDw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:29] Document attached:
 - data.id              4725d60a2a1b454b878f926b79d919ea
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/81baa3f353f1451e9b9108a9e5b712f6?Signature=ARe%2BLGvQgkC0AelOb9RDMJKE6GUN9O5IRoYkk6n4ZaVWjbBJwKUVLh3yeyrbdKUyD5sFHUMGhAiYOTVMQS6zBg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:29] Document attached:
 - data.id              d18d9594d3b5448b827a4edeead9e384
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/775942b446fd4f55bf218b3d07aef0ec?Signature=nctc5dzUlXw20iPZviC9O09A6XM2a5La5wJ6SzNmooOKIPRkQAOiM3TzyUiQCcVjw1kx1lvJmP8X%2FDN2qKC6CA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[14:24:29] Bid created:
 - data.id              2cce67a23a934a06b751c381441aff99
 - access.token         ca93bf748cdb40b186d15a8f7d70be22
 - data.status          draft

[14:24:29] Completed.

[14:24:29] Summary
 - closeFrameworkAgreementUA	success

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
