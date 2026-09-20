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
procedure --env sandbox --data=closeFrameworkAgreementUA --stop=tender_bid_create_3.json
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
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA --stop=tender_bid_create_3.json
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
procedure --env sandbox --data=closeFrameworkAgreementUA --stop=tender_bid_create_4.json
```
```
[13:04:34] Using env file /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/.env.readme

[13:04:34] Press P to pause and show summary, S to show summary

[13:04:34] Using seed 638824

[13:04:34] Initializing cdb client

[13:04:34] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[13:04:34] Response status: 200 OK

[13:04:34] Client time delta with server: -958 milliseconds

[13:04:34] Initializing ds client

[13:04:34] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[13:04:34] Response status: 200 OK

[13:04:34] Creating framework...

[13:04:34] Processing data file: framework_create.json

[13:04:34] Skipping...

[13:04:34] Creating plan...

[13:04:34] Processing data file: plan_create.json

[13:04:35] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[13:04:35] Response status: 201 Created

[13:04:35] Plan created:
 - data.id              37dfc73946824aabac891822c2268244
 - access.token         bbeeb684e9bb4bbb8f804affa70fdbb2
 - access.transfer      011c7d69838d489c8b205c7bf9f241ca
 - data.status          draft

[13:04:35] Patching plan...

[13:04:35] Processing data file: plan_patch.json

[13:04:35] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/37dfc73946824aabac891822c2268244?acc_token=bbeeb684e9bb4bbb8f804affa70fdbb2
[13:04:35] Response status: 200 OK

[13:04:35] Plan patched:
 - data.id              37dfc73946824aabac891822c2268244
 - data.status          scheduled

[13:04:35] Creating tender...

[13:04:35] Processing data file: tender_create.json

[13:04:35] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/37dfc73946824aabac891822c2268244/tenders
[13:04:35] Response status: 201 Created

[13:04:35] Tender created:
 - data.id              f8d37a0baa8541d8a80afd59be5de9e7
 - access.token         e280adccd88a4f2a9bbda31a52f94997
 - access.transfer      5cd3920fd3f040c18667adb30f36f89b
 - data.status          draft
 - data.tenderID        UA-2026-09-20-000115-a
 - data.procurementMethodType closeFrameworkAgreementUA

[13:04:35] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f8d37a0baa8541d8a80afd59be5de9e7
[13:04:35] Response status: 200 OK

[13:04:35] Processing data file: tender_document_attach.json

[13:04:35] Processing data file: tender_document_file.txt

[13:04:35] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:35] Response status: 200 OK

[13:04:35] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f8d37a0baa8541d8a80afd59be5de9e7/documents?acc_token=e280adccd88a4f2a9bbda31a52f94997
[13:04:36] Response status: 201 Created

[13:04:36] Document attached:
 - data.id              76f492e192354735a3898d3e251a16ca
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/cc7ef8226b854999b4fce7bb4ea50e92?Signature=XDV0cq7q%2Frvv2C8I%2F9PH%2FrVbj3QuXkqSDAsj%2F2kPBUzZyLedLf4xpaoCj%2F8G%2F844j3S%2FAQdkUMTCXMmPBnC5Ag%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:36] Processing data file: contract_proforma_attach.json

[13:04:36] Processing data file: contract_proforma.txt

[13:04:36] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:36] Response status: 200 OK

[13:04:36] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f8d37a0baa8541d8a80afd59be5de9e7/documents?acc_token=e280adccd88a4f2a9bbda31a52f94997
[13:04:36] Response status: 201 Created

[13:04:36] Document attached:
 - data.id              e2d9aa745515425f8694ecf0f54233b8
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/b8e48c5d455c424b8692ae4f44e9a170?Signature=PCX1BcPgZToPLXn3T7ZraPQ88fhAIAl%2BQI7wit1EbBgVJcHEy%2FTnw8f%2Fm9DJSKsu1E3e95dQlO9BoVAl8qE1Bw%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[13:04:36] Create tender criteria...

[13:04:36] Processing data file: criteria_create.json

[13:04:36] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f8d37a0baa8541d8a80afd59be5de9e7/criteria?acc_token=e280adccd88a4f2a9bbda31a52f94997
[13:04:36] Response status: 201 Created

[13:04:36] Tender criteria created:
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

[13:04:36] Processing data file: tender_notice_attach.json

[13:04:36] Processing data file: tender_notice_file.p7s

[13:04:36] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:36] Response status: 200 OK

[13:04:36] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f8d37a0baa8541d8a80afd59be5de9e7/documents?acc_token=e280adccd88a4f2a9bbda31a52f94997
[13:04:36] Response status: 201 Created

[13:04:36] Document attached:
 - data.id              e2891837563849a887639ddaa1cfbd43
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/40c9e3a5e6ce439b96161ddae42b8f7f?Signature=A6qCvUnlXCLc1S%2B8HmjXdWsq2VAeM7LFkcs3TSGa1O3xsH6ZKc6ihC%2BIkc30ViA05EyS2tVlY%2FqTu0F96nEtAA%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[13:04:36] Patching tender...

[13:04:36] Processing data file: tender_patch.json

[13:04:36] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f8d37a0baa8541d8a80afd59be5de9e7?acc_token=e280adccd88a4f2a9bbda31a52f94997
[13:04:37] Response status: 200 OK

[13:04:37] Tender patched:
 - data.id              f8d37a0baa8541d8a80afd59be5de9e7
 - data.status          active.tendering

[13:04:37] Creating complaints...

[13:04:37] Skipping complaints creating: bot and reviewer tokens are required

[13:04:37] Creating bids...

[13:04:37] Processing data file: tender_bid_create_0.json

[13:04:37] Processing data file: bid_document_file.txt

[13:04:37] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:37] Response status: 200 OK

[13:04:37] Processing data file: bid_confidential_document_file.txt

[13:04:37] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:37] Response status: 200 OK

[13:04:37] Processing data file: bid_eligibility_document_file.txt

[13:04:37] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:37] Response status: 200 OK

[13:04:37] Processing data file: bid_financial_document_file.txt

[13:04:37] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:37] Response status: 200 OK

[13:04:37] Processing data file: bid_qualification_document_file.txt

[13:04:37] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:38] Response status: 200 OK

[13:04:38] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f8d37a0baa8541d8a80afd59be5de9e7/bids
[13:04:38] Response status: 201 Created

[13:04:38] Document attached:
 - data.id              f9bd557b4c1d4385b030cb9a08bfc1b3
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/b46908bbc896483aa01a29e3d864d4be?Signature=%2Bk9JcZT2jftlRpDXBO2ftfe7ZDdLIVP9EKtgwqu9NnXxZFoIxqnzZN5G1O2oxqFGNJQX4UJkL%2FgXyyEhL9WACA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:38] Document attached:
 - data.id              5eec174cd4b848a0b2dfe28dd2544fba
 - data.confidentiality buyerOnly

[13:04:38] Document attached:
 - data.id              6426d390cf1c4e7c865f6b691e0025fa
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/2696574cf11e498bb6f8bc1cff2d6abf?Signature=r%2Bvrt%2BJp2zVx%2BhEz6Zfug7dZ6y55gkAsk74h4RMpUqEbojadEJmQ2Sh9FSeV%2FldTjIALqMkQkO4srazaZsgmDQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:38] Document attached:
 - data.id              4e2df22ccadc4614ba8387858552f289
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/7ec2c4bb9f4d4aceba5a9f78652dca94?Signature=PskrUjJS%2FGMOcRYdSHkWIjlCxWWzt5T50qnn0ngfJ4CgeU9olvgOz3rEBYmpIKLASlEWgpRWeL98%2FRk6Zdd%2FAg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:38] Document attached:
 - data.id              8d17c1f22a304c0f94dc89230e490521
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/e6f15bdbbbf8477eb5f3b8187679b214?Signature=lEQpjOgc9jDppO7TGZI5%2Bv%2F6xTLGrFChuQ%2FXGCgvz0wgC%2BSOSZXkQ%2FD0bxd7NyJ2359L5qaLkqB9kIk5eRGhAg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:38] Bid created:
 - data.id              b6a8733bd48a4b7d9f4d311a3116d27e
 - access.token         bcb7109877534d45b44a371fca8a32b8
 - data.status          draft

[13:04:38] Processing data file: tender_bid_create_1.json

[13:04:38] Processing data file: bid_document_file.txt

[13:04:38] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:38] Response status: 200 OK

[13:04:38] Processing data file: bid_confidential_document_file.txt

[13:04:38] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:38] Response status: 200 OK

[13:04:38] Processing data file: bid_eligibility_document_file.txt

[13:04:38] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:38] Response status: 200 OK

[13:04:38] Processing data file: bid_financial_document_file.txt

[13:04:38] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:38] Response status: 200 OK

[13:04:38] Processing data file: bid_qualification_document_file.txt

[13:04:38] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:38] Response status: 200 OK

[13:04:38] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f8d37a0baa8541d8a80afd59be5de9e7/bids
[13:04:38] Response status: 201 Created

[13:04:38] Document attached:
 - data.id              bb8abb017c654c5fa9df0cc057a0c242
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/7503e415ac4247d78f9a3b6486d54db2?Signature=YqtFRSsRpQmO7%2Bvq8XaXZAh%2BTIDV2RaAoN8ZZOMmXUm3IUlHU3Ba%2BPcEv46I%2FwihddjnLNd5luGzGiJpIvRKDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:38] Document attached:
 - data.id              7ba813a1f01d42deb642a8e38d77a208
 - data.confidentiality buyerOnly

[13:04:38] Document attached:
 - data.id              d9fc0a44623246d98511ee745151d389
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/3662c25dbba348b9b8fa90abafb5cd7e?Signature=qIGZP4vUXl1RJ9pgAAdotGkBJGITC5KViLASi%2B3YXW0c0mJL69eCoi9VyTSKpWf2gdEm5FtU3jzlImTgMIvDBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:38] Document attached:
 - data.id              04ab27c3c2b04eae9243587a447ecc3c
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/881f0918aadd4105bf9f7f2ffd904e4c?Signature=UBk2t%2B8YGTY9Ez3cWupPvH08y4Rc15zUPf1nkDXRL7usXzFLqExUl143DHYvI3Jn5%2BcV%2FJdTA4J%2FYQOeaUlrBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:38] Document attached:
 - data.id              eddba9cfd99f426ca6ca2733a44c9226
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/1468eccf39c74398878a74bdc7ac4410?Signature=%2B1maANdP9CB01A6rOnCb9e1Uj9FimsLLlQ3SXdXrMK80ZhFwIkmhS%2BDFF3SkSoJ6dVzv5ZE1Z4%2BhIrT8JRKZDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:38] Bid created:
 - data.id              967ccc6cc764480babb2be486889c56b
 - access.token         9d5800685acd422a9a3359ac887df00d
 - data.status          draft

[13:04:38] Processing data file: tender_bid_create_2.json

[13:04:38] Processing data file: bid_document_file.txt

[13:04:38] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:39] Response status: 200 OK

[13:04:39] Processing data file: bid_confidential_document_file.txt

[13:04:39] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:39] Response status: 200 OK

[13:04:39] Processing data file: bid_eligibility_document_file.txt

[13:04:39] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:39] Response status: 200 OK

[13:04:39] Processing data file: bid_financial_document_file.txt

[13:04:39] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:39] Response status: 200 OK

[13:04:39] Processing data file: bid_qualification_document_file.txt

[13:04:39] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:39] Response status: 200 OK

[13:04:39] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f8d37a0baa8541d8a80afd59be5de9e7/bids
[13:04:39] Response status: 201 Created

[13:04:39] Document attached:
 - data.id              8aef3f789dc44dcfad2abc6102bec5cb
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/4501ba14a1fe47c3bc68c4c4dc78be31?Signature=vLGkCVKUEo83Kwpjc54XrqaVpuWyZji%2BA1CQMi1rVq8RS47QkG7OO5Qdyl2Yqoz0lrO3p6%2BJsJKM86LXIKQGCg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:39] Document attached:
 - data.id              0d8718701c4b4f9c9b827ed672f70498
 - data.confidentiality buyerOnly

[13:04:39] Document attached:
 - data.id              9abebf9627e044d1ae643afe29f18ebc
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/c65a0c740152445ab95b27afe954dc7c?Signature=h4%2FXHhj0I5jwJ6SI4KoHQXh5Pn4oLhzH6PelNKzNpG04awbi%2FT8Vk6kWutZbfSGQFPaN992hpVaat4fLyXRgDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:39] Document attached:
 - data.id              2527885ee391453f93b83a98661c8566
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/29385d026a27420d8ce156c8e26e3973?Signature=7pVk%2F3aMQUdcY%2FhXo0BTAi0JBl%2BQ12s32cmhReu3ARg6a%2FxDWDU34qgo7eAGXSzFNYIP694hmB9WHPfXnda6Dg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:39] Document attached:
 - data.id              8d6585d77e1f43a2a67bec49f6d475a1
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/03164bda509e4a11906e34afaa6caa79?Signature=1KToQVyrNFq%2B7NV3xxT806EZh9EneI94T4xwKdQt7rHBrEWu9NG8Y%2Ffmf0vIvywOIF3OxNfihZCJsfEOSKQKDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:39] Bid created:
 - data.id              84140ed8e6ad4115bb4a69f2082669d1
 - access.token         9ea2987086d24813b713e85ed80d059e
 - data.status          draft

[13:04:39] Processing data file: tender_bid_create_3.json

[13:04:39] Processing data file: bid_document_file.txt

[13:04:39] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:39] Response status: 200 OK

[13:04:39] Processing data file: bid_confidential_document_file.txt

[13:04:39] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:40] Response status: 200 OK

[13:04:40] Processing data file: bid_eligibility_document_file.txt

[13:04:40] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:40] Response status: 200 OK

[13:04:40] Processing data file: bid_financial_document_file.txt

[13:04:40] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:40] Response status: 200 OK

[13:04:40] Processing data file: bid_qualification_document_file.txt

[13:04:40] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:04:40] Response status: 200 OK

[13:04:40] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f8d37a0baa8541d8a80afd59be5de9e7/bids
[13:04:40] Response status: 201 Created

[13:04:40] Document attached:
 - data.id              718b463d17444e2dbe5c89eb445a4384
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/ba9152d4567143b68b13aca3a52b4dde?Signature=3xFrQ9CSqZ83qZpTCiB4%2BYeBY842d0F3QafxmUyn%2FtxlVprbhwsLsOtuMXn5%2B1U8kF6bFjfjEsLj3Uk1tNspCQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:40] Document attached:
 - data.id              dbdaa109b6464565bf5f4a623806d8d6
 - data.confidentiality buyerOnly

[13:04:40] Document attached:
 - data.id              6353397635814f90b7a92b9f4c220f6e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/aa67658c0dc54781948ff9d4aee310cf?Signature=EEidFsimssGaxHE8QFZy4SLQveo5BguyXrwDezbJRk770c4WMmk0o5j5WG5JrrK1FpiLUwhDPZxXf3ZAF6ZvAg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:40] Document attached:
 - data.id              9433de6fc7144a78a2fb81336c637068
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/f0aabd050c0b4e618dbc55df16669689?Signature=LM%2FrJQJLxnKP4SI3N%2BEcN7o6MviKu7DKZGCzycw5vCz8hdksCZ4PlrBLx2B7z8sSIwf9TUr2VCcV6%2Br2kCdvBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:40] Document attached:
 - data.id              93189957c34d4093802410a8d387ebb0
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/89325a0830b64b129796ae443f3bd4c0?Signature=B399Ke3DksGm5YXe0O0Cb1TfKqaHG00cPYVeZnWdRTZdxS%2BA%2FCbo0DqLkm3Wtv6G7siDILQn29GapzZFKiyFDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[13:04:40] Bid created:
 - data.id              b2bab45699ce47f0b8721173830746a1
 - access.token         9da88643b9914a89942f29bd2941d8d9
 - data.status          draft

[13:04:40] Completed.

[13:04:40] Summary
 - closeFrameworkAgreementUA	success

```

## procedure-tools

`procedure-tools` creates the same procedures with the same options (see `procedure-tools -h`), but there is no procedure specific code path: the data files define the flow. Every `.json` file in a data folder (`tools/data/<name>`) is one action:

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

Every action updates the shared context: created objects (`plan`, `tender`, `bids`, `awards`, `contracts`, `framework`, `agreement`, ...) and their tokens (`tender_token`, `bids_tokens`, `contracts_tokens`, ...). The context is also the template context of the data files, so `{{ tender.id }}`, `{{ contracts[0].dateModified }}` or `{{ plans[1].id }}` resolve to what earlier actions stored. `fake`, `fake_en`, `from_now_iso()` and the other helpers work as in `procedure`.

Technical actions (`tender_wait_status`, `tender_wait_next_check`, `wait_date`, `stop_if`, `context_rename`, ...) replace the waits and branches that `procedure` hard-codes. Their parameters live in the data file, for example:

```
2160_tender_wait_status.json    {"status": ["active.qualification", "active.awarded"], "fail_status": "unsuccessful"}
2500_tender_wait_status.json    {"status": "complete"}
2150_tender_wait_next_check.json  {}
```

An unknown action name fails before anything is sent to the API and prints the available actions. `--stop`, `--pause`, `--wait`, `--parallel` and env files work as for `procedure`.

Run:

```
procedure-tools --env sandbox --data reporting
procedure-tools --env sandbox --data aboveThreshold --stop tender_bid_patch_1.json
procedure-tools --env sandbox --data customdata/myFlow
```

Example flow (`tools/data/reporting`):

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
 - agreement_get                            Load the agreement (GET agreements/{id}) of the framework, or the last agreement of the tender, into agreement.
 - context_delete                           Delete context keys: {"keys": ["awards", "contracts"]}.
 - context_rename                           Rename context keys, e.g. before a new stage: {"tender": "stage1_tender", "tender_token": "stage1_tender_token"}.
 - context_set                              Merge the data file into the context: {"my_value": "{{ tender.id }}"}.
 - contract_access_post                     Get an econtract token for a role (POST contracts/{id}/access); parts: [contract index, buyer|supplier]; sets contracts_<role>_tokens[i].
 - contract_buyer_signer_info_put           Set the buyer signer info (PUT contracts/{id}/buyer/signer_info); parts: [contract index, (role)].
 - contract_cancellation_post               Cancel a contract (POST contracts/{id}/cancellations); parts: [contract index, (role)].
 - contract_change_cancellation_post        Cancel a contract change (POST contracts/{id}/changes/{id}/cancellations); parts: [contract index, change index, (role)].
 - contract_change_document_attach          Attach a document to a contract change (POST contracts/{id}/changes/{id}/documents); parts: [contract index, change index, (role)].
 - contract_change_patch                    Patch a contract change (PATCH contracts/{id}/changes/{id}); parts: [contract index, change index, (role)].
 - contract_change_post                     Create a contract change (POST contracts/{id}/changes); parts: [contract index, (role)].
 - contract_change_signatories_post         Sign a contract change (POST contracts/{id}/changes/{id}/signatories); parts: [contract index, change index, (role)].
 - contract_credentials_patch               Get the legacy contract token (PATCH contracts/{id}/credentials); parts: [contract index]; sets contracts_tokens[i].
 - contract_document_attach                 Attach a document to a contract (POST contracts/{id}/documents); parts: [contract index, (role)].
 - contract_patch                           Patch a contract (PATCH contracts/{id}); parts: [contract index, (role)].
 - contract_post                            Create a contract (POST contracts) with the token of contract [index]; parts: [contract index, (role)].
 - contract_signatories_post                Sign a contract (POST contracts/{id}/signatories); parts: [contract index, (role)].
 - contract_suppliers_signer_info_put       Set the suppliers signer info (PUT contracts/{id}/suppliers/signer_info) with the winning bid token; parts: [contract index, (role)].
 - framework_create                         Create a framework (POST frameworks); sets framework, framework_token.
 - framework_get                            Refresh the framework in context (GET frameworks/{id}).
 - framework_patch                          Patch the framework (PATCH frameworks/{id}), for example to activate it.
 - framework_qualification_document_attach  Attach a document to a framework qualification (POST qualifications/{id}/documents); parts: [submission index].
 - framework_qualification_patch            Patch a framework qualification (PATCH qualifications/{id}); parts: [submission index].
 - framework_submission_create              Create a submission (POST submissions); parts: [submission index]; sets submissions[i], submissions_tokens[i].
 - framework_submission_patch               Patch a submission (PATCH submissions/{id}); parts: [submission index].
 - pause                                    Pause until Enter is pressed: {"message": "<optional prompt>"}.
 - plan_create                              Create a plan (POST plans); sets plan, plan_token and appends to plans, plans_tokens.
 - plan_patch                               Patch a plan (PATCH plans/{id}); parts: [plan index] (default: the last created plan).
 - skip_if                                  Skip the next steps when a condition holds: {"condition": "{{ tender.status != 'active.pre-qualification' }}", "steps": 2}.
 - stop_if                                  Stop the run successfully when a condition holds: {"condition": "{{ constants.SIGNATURE_VERIFICATION_ENABLED }}", "message": "..."}.
 - tender_agreement_contract_patch          Patch the agreement contract of a bid (PATCH tenders/{id}/agreements/{id}/contracts/{id}); parts: [agreement index, bid index].
 - tender_agreement_document_attach         Attach a document to a tender agreement (POST tenders/{id}/agreements/{id}/documents); parts: [agreement index].
 - tender_agreement_patch                   Patch a tender agreement (PATCH tenders/{id}/agreements/{id}); parts: [agreement index].
 - tender_agreements_get                    Refresh the tender agreements in context (GET tenders/{id}/agreements).
 - tender_award_complaint_create            Create an award complaint (POST tenders/{id}/awards/{id}/complaints); parts: [award index, complaint index].
 - tender_award_complaint_patch             Patch an award complaint as a role; parts: [award index, complaint index, bot|reviewer|tenderer|complainer].
 - tender_award_create                      Create an award (POST tenders/{id}/awards) in limited procedures; parts are a free label.
 - tender_award_document_attach             Attach a document to an award (POST tenders/{id}/awards/{id}/documents); parts: [award index, free label].
 - tender_award_patch                       Patch an award (PATCH tenders/{id}/awards/{id}); parts: [award index]; refreshes awards.
 - tender_awards_get                        Refresh the tender awards in context (GET tenders/{id}/awards).
 - tender_awards_wait_complaint_period      Wait for the end of the complaint period of all awards.
 - tender_awards_wait_edr                   Wait for the EDR identification documents of the awards; runs only with --wait edr-qualification.
 - tender_bid_create                        Create a bid (POST tenders/{id}/bids), uploading the documents listed in it; parts: [bid index]; sets bids[i], bids_tokens[i].
 - tender_bid_document_attach               Attach a document to a bid (POST tenders/{id}/bids/{id}/documents); parts: [bid index, free label].
 - tender_bid_patch                         Patch a bid (PATCH tenders/{id}/bids/{id}); parts: [bid index].
 - tender_bid_res_post                      Post bid requirement responses (POST tenders/{id}/bids/{id}/requirement_responses); parts: [bid index].
 - tender_bids_get                          Load the tender bids into context (GET tenders/{id}/bids) when they were not created in this run.
 - tender_complaint_create                  Create a tender complaint (POST tenders/{id}/complaints); parts: [complaint index].
 - tender_complaint_patch                   Patch a tender complaint as a role; parts: [complaint index, bot|reviewer|tenderer|complainer].
 - tender_contracts_get                     Load the tender contracts into contracts (GET tenders/{id}/contracts, then GET contracts/{id} for each).
 - tender_create                            Create a tender (POST tenders, or POST plans/{id}/tenders when a plan is in context); sets tender, tender_token, tender_config.
 - tender_credentials_patch                 Take over the second stage tender (PATCH tenders/{stage2TenderID}/credentials); the previous tender moves to stage1_tender.
 - tender_criteria_post                     Create tender criteria (POST tenders/{id}/criteria); sets criteria.
 - tender_document_attach                   Attach a document to the tender (POST tenders/{id}/documents); parts are a free label; appends to tender_documents.
 - tender_document_put                      Replace a tender document with a new version (PUT tenders/{id}/documents/{id}); parts: [tender_documents index] or a label, then the last attached document with the same title is replaced.
 - tender_get                               Refresh the tender in context (GET tenders/{id}).
 - tender_patch                             Patch the tender (PATCH tenders/{id}), for example to switch its status.
 - tender_plan_post                         Connect a plan to the tender (POST tenders/{id}/plans); the data file holds the plan id, e.g. {{ plans[1].id }}.
 - tender_qualification_complaint_create    Create a qualification complaint (POST tenders/{id}/qualifications/{id}/complaints); parts: [qualification index, complaint index].
 - tender_qualification_complaint_patch     Patch a qualification complaint as a role; parts: [qualification index, complaint index, bot|reviewer|tenderer|complainer].
 - tender_qualification_document_attach     Attach a document to a tender qualification (POST tenders/{id}/qualifications/{id}/documents); parts: [qualification index].
 - tender_qualification_patch               Patch a tender qualification (PATCH tenders/{id}/qualifications/{id}); parts: [qualification index].
 - tender_qualifications_get                Refresh the tender qualifications in context (GET tenders/{id}/qualifications).
 - tender_qualifications_wait_edr           Wait for the EDR identification documents of the qualifications; runs only with --wait edr-pre-qualification.
 - tender_wait_auction                      Wait for the auction participation urls of the active bids; skipped for mode:no-auction submissions.
 - tender_wait_next_check                   Wait for the next chronograph check of the tender (its next_check date), if any.
 - tender_wait_status                       Wait for a tender status: {"status": "x" or [...], "fail_status": "y" (optional), "delay": seconds (default 1)}.
 - wait_date                                Wait until a date: {"date": "<iso date, templates allowed>", "description": "<optional log text>"}.
 - wait_seconds                             Sleep for a number of seconds: {"seconds": 5}.
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
