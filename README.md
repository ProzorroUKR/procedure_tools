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
[15:48:57] Using env file /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/.env.readme

[15:48:57] Press P to pause and show summary, S to show summary

[15:48:57] Using seed 589122

[15:48:57] Initializing cdb client

[15:48:57] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[15:48:57] Response status: 200 OK

[15:48:57] Client time delta with server: -807 milliseconds

[15:48:57] Initializing ds client

[15:48:57] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[15:48:57] Response status: 200 OK

[15:48:57] Creating framework...

[15:48:57] Processing data file: framework_create.json

[15:48:57] Skipping...

[15:48:57] Creating plan...

[15:48:57] Processing data file: plan_create.json

[15:48:57] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[15:48:57] Response status: 201 Created

[15:48:57] Plan created:
 - data.id              7cb5db6e275145ab9f23960a6abac441
 - access.token         6d62d7d0144c45d08eb725a1502dcc37
 - access.transfer      f5c94eeb8ccc47c19e7850255f25365e
 - data.status          draft

[15:48:57] Patching plan...

[15:48:57] Processing data file: plan_patch.json

[15:48:57] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/7cb5db6e275145ab9f23960a6abac441?acc_token=6d62d7d0144c45d08eb725a1502dcc37
[15:48:58] Response status: 200 OK

[15:48:58] Plan patched:
 - data.id              7cb5db6e275145ab9f23960a6abac441
 - data.status          scheduled

[15:48:58] Creating tender...

[15:48:58] Processing data file: tender_create.json

[15:48:58] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/7cb5db6e275145ab9f23960a6abac441/tenders
[15:48:58] Response status: 201 Created

[15:48:58] Tender created:
 - data.id              b32c1d39d4374fa7b2843e48b26c7a5c
 - access.token         8f86e3d3100e4121952c894020f76508
 - access.transfer      203ff24cd12a4ee99f5a0aa40c2ca601
 - data.status          draft
 - data.tenderID        UA-2026-09-15-000334-a
 - data.procurementMethodType closeFrameworkAgreementUA

[15:48:58] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b32c1d39d4374fa7b2843e48b26c7a5c
[15:48:58] Response status: 200 OK

[15:48:58] Processing data file: tender_document_attach.json

[15:48:58] Processing data file: tender_document_file.txt

[15:48:58] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:48:58] Response status: 200 OK

[15:48:58] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b32c1d39d4374fa7b2843e48b26c7a5c/documents?acc_token=8f86e3d3100e4121952c894020f76508
[15:48:58] Response status: 201 Created

[15:48:58] Document attached:
 - data.id              a546151caaf740b09907339f5668424c
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/41ca733e96be49b9b6261ca886fff480?Signature=tacQik73m9hL5tX1%2BKi493buCGQ61v0qCAftlT1U8zDTTU5e3XnhvnRxSbfx2hs8vXonbdhnN4PIdYUHMDEBCQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:48:58] Processing data file: contract_proforma_attach.json

[15:48:58] Processing data file: contract_proforma.txt

[15:48:58] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:48:58] Response status: 200 OK

[15:48:58] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b32c1d39d4374fa7b2843e48b26c7a5c/documents?acc_token=8f86e3d3100e4121952c894020f76508
[15:48:58] Response status: 201 Created

[15:48:58] Document attached:
 - data.id              b3a2c1ec086c4d55b6704eaa3ef87f90
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/93a86701d951466ab82c30a1c1fd4290?Signature=zkrUSbna8i33okYjlETeuMfDnGDppeKNWSfc6Jrg%2B7lGsoKmtmdRlUflcFFxz1jxVHYn%2FV4iKtMTQur%2BZRIgDg%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[15:48:58] Create tender criteria...

[15:48:58] Processing data file: criteria_create.json

[15:48:58] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b32c1d39d4374fa7b2843e48b26c7a5c/criteria?acc_token=8f86e3d3100e4121952c894020f76508
[15:48:59] Response status: 201 Created

[15:48:59] Tender criteria created:
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

[15:48:59] Processing data file: tender_notice_attach.json

[15:48:59] Processing data file: tender_notice_file.p7s

[15:48:59] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:48:59] Response status: 200 OK

[15:48:59] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b32c1d39d4374fa7b2843e48b26c7a5c/documents?acc_token=8f86e3d3100e4121952c894020f76508
[15:48:59] Response status: 201 Created

[15:48:59] Document attached:
 - data.id              08ceb62eb83749949e2906ad0a5a11a2
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/00dde1ccbb614c5697b7c935f3767b54?Signature=yu2b1JplMFtcxilFIM1B1BoVNk3pwW9fRv5YpkEkNUJq6pETYDV87pE6dgXTQO86dC4%2FGl%2FqSSrmnglDpmWrCw%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[15:48:59] Patching tender...

[15:48:59] Processing data file: tender_patch.json

[15:48:59] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b32c1d39d4374fa7b2843e48b26c7a5c?acc_token=8f86e3d3100e4121952c894020f76508
[15:48:59] Response status: 200 OK

[15:48:59] Tender patched:
 - data.id              b32c1d39d4374fa7b2843e48b26c7a5c
 - data.status          active.tendering

[15:48:59] Skipping complaints creating: bot and reviewer tokens are required

[15:48:59] Creating bids...

[15:48:59] Processing data file: bid_create_0.json

[15:48:59] Processing data file: bid_document_file.txt

[15:48:59] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:48:59] Response status: 200 OK

[15:48:59] Processing data file: bid_confidential_document_file.txt

[15:48:59] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:00] Response status: 200 OK

[15:49:00] Processing data file: bid_eligibility_document_file.txt

[15:49:00] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:00] Response status: 200 OK

[15:49:00] Processing data file: bid_financial_document_file.txt

[15:49:00] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:00] Response status: 200 OK

[15:49:00] Processing data file: bid_qualification_document_file.txt

[15:49:00] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:00] Response status: 200 OK

[15:49:00] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b32c1d39d4374fa7b2843e48b26c7a5c/bids
[15:49:00] Response status: 201 Created

[15:49:00] Document attached:
 - data.id              f261c5d96b3844c6ae3744309c959ca3
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/823679d0b391405480b7bf5d8ddec905?Signature=q0Kw2wp890Mxa5hzXu9oIAojEBxGkigvWpZRHq02rAu2f8u%2FAeuIYmXcwEe%2FSABJwKhssoYLyiBDFwqp5t6XDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:00] Document attached:
 - data.id              e98a7e06d1a74cd79792a5a27407fd34
 - data.confidentiality buyerOnly

[15:49:00] Document attached:
 - data.id              d869e677bc3149ecab8bef7582f7b032
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/56112932f16b49ea8e79aa13a77fbccc?Signature=XJjF%2Fb2a5aUXFGConL%2FppZ1O7P3mk9pqy6dn8kzNR4z8JGXsL0UZVGr%2F3qKMGIXPHN%2BvGtmBdj%2FHBPz9anIlCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:00] Document attached:
 - data.id              e3762a76397b4cf1ab143faafa277986
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/9393fe9e09f34e48815ee52a7ded0805?Signature=EqGzRaqyXw9yCNRzy2u5M1s9nAuiM0lNxutRzaBNpPxNK6XKqoQnjnjfTyGjoLdamSNAQAogKAFESjIqY5%2BiDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:00] Document attached:
 - data.id              51f489140de640c18dfe5d01c6283919
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/c04ebcfbc76c4883b5cd08bc4fa1acec?Signature=ArLeiTPvEYjrQrswR4IUcG5YjgrKk003NTzFcpfsY5HvPW7fwJwQZjiyz5wIdKdPT6D0npXqw%2BsCBeTNEcsuBg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:00] Bid created:
 - data.id              0ca80291479a4c15a3c546bd2cd477cb
 - access.token         f772a132533e462baa96be9295997c22
 - data.status          draft

[15:49:00] Processing data file: bid_create_1.json

[15:49:00] Processing data file: bid_document_file.txt

[15:49:00] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:01] Response status: 200 OK

[15:49:01] Processing data file: bid_confidential_document_file.txt

[15:49:01] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:01] Response status: 200 OK

[15:49:01] Processing data file: bid_eligibility_document_file.txt

[15:49:01] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:01] Response status: 200 OK

[15:49:01] Processing data file: bid_financial_document_file.txt

[15:49:01] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:01] Response status: 200 OK

[15:49:01] Processing data file: bid_qualification_document_file.txt

[15:49:01] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:02] Response status: 200 OK

[15:49:02] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b32c1d39d4374fa7b2843e48b26c7a5c/bids
[15:49:02] Response status: 201 Created

[15:49:02] Document attached:
 - data.id              067b3485c2d24971a7b286459f214d8a
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/82d8ad7e9d3c498ebdd62d0747c4095b?Signature=i9TnnkyZbdHvpP9c%2BHUR%2FgdEfPwP2P0j7NTMaCZHk6aU2vnS%2FI5W3BEoqvJiLU3OBs%2FNQ5LBQ8qM5uWBNtvbAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:02] Document attached:
 - data.id              85897ab8a3984c1f997a08b1fa4c8491
 - data.confidentiality buyerOnly

[15:49:02] Document attached:
 - data.id              5feaa99223814c3698bdfcf2322371c3
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/82b7bf1d778a43e6bd100a07da54ae2f?Signature=6Ng%2B0OJlotVTjT7rEq2z0JnfNOsvGCxi56vWbfx7IJi0u%2BAECxDLIBA7Bb%2BzGNFLZFwOT%2BUPhsY3jaKeiFZbAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:02] Document attached:
 - data.id              4204182b157b4074bd829b2aa9245056
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/c32092b7cd544088b1b54a9c308bfb89?Signature=tFHMxKdtyQRublSuQwBa7oHNYx%2B5dCeD5V3ykW9ph6v9GRJL%2BuHVwpknNcZRc6cxckEzQpT4ofS21jhPiomEDw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:02] Document attached:
 - data.id              023a09f55c584494b80ac43b291e996c
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/283a1fce3e4844d686c8f4ddab9e09d3?Signature=X5ZQcTpEvwzOl7L0yGZUcqgBH45YVqpu2m46R%2Fc5zEfen7cPhqFE%2Fn5YFWcVZ6VtK%2BF62ViaBKlpfM0dECjsDw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:02] Bid created:
 - data.id              ca8818e5a1164b3f804e32914145bc53
 - access.token         7d218a1fa0c5473fa678a8e58f11d7cf
 - data.status          draft

[15:49:02] Processing data file: bid_create_2.json

[15:49:02] Processing data file: bid_document_file.txt

[15:49:02] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:02] Response status: 200 OK

[15:49:02] Processing data file: bid_confidential_document_file.txt

[15:49:02] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:02] Response status: 200 OK

[15:49:02] Processing data file: bid_eligibility_document_file.txt

[15:49:02] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:02] Response status: 200 OK

[15:49:02] Processing data file: bid_financial_document_file.txt

[15:49:02] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:02] Response status: 200 OK

[15:49:02] Processing data file: bid_qualification_document_file.txt

[15:49:02] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:02] Response status: 200 OK

[15:49:02] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b32c1d39d4374fa7b2843e48b26c7a5c/bids
[15:49:03] Response status: 201 Created

[15:49:03] Document attached:
 - data.id              451115b2a7714d2e8c6fe34809ad0b3c
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/c5b94b2b638349c1ab0afe25b9a8708b?Signature=%2FcpBvmo9Kgi6Qn8e2Kg7O0TdcDi0dwfsLHr7%2BuYFvigvmN5vZHIG5KeNsPR%2FYWNeg9NhpXN0%2FWFX%2BLMp1XI%2FCQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:03] Document attached:
 - data.id              fbf338e1d8d641a4af5655acd0677c08
 - data.confidentiality buyerOnly

[15:49:03] Document attached:
 - data.id              ee5f26e948ac40eaa9468b1a5def217c
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/2c129391b48b4fb7b7573796c57329f4?Signature=JVAT1duZZXD9qx80UYFgQLejXgjO1LiFVOBA6eiqVGd7ehA%2BKq2Zv4C6OHrlPFKAU0U7gQ1SRrnPO5GGcP8QAg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:03] Document attached:
 - data.id              f4d4347698b4443d97bfa9dea35e6d83
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/a8afeb8864454ebe9863d7394a4728c4?Signature=s%2Bz9SsQgvPH%2FlqFEJTrIFGwlwb18m792uAMn4eJv9IMmBITG5E8WlNrBtfSyZX8wS9bBc1BQiHd5WC63lre%2BAg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:03] Document attached:
 - data.id              e4a1867c291547029e435f2cf2423f01
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/7777b2138b434a9ca796017195f6f5b2?Signature=6qV%2B4O%2BZr0jnHOK%2FeEjkFrDf%2FGQMFWpAw%2BzPXGrx98%2BVHNB0WXCm0gLAU4TEPh%2F7srmF63Y2HcNTjGxRaPtLAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:03] Bid created:
 - data.id              226f3238133a4c4fbc67ec853ab90ee7
 - access.token         e5e6cd4c6c5c4934b164d1f94db42fca
 - data.status          draft

[15:49:03] Processing data file: bid_create_3.json

[15:49:03] Processing data file: bid_document_file.txt

[15:49:03] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:03] Response status: 200 OK

[15:49:03] Processing data file: bid_confidential_document_file.txt

[15:49:03] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:03] Response status: 200 OK

[15:49:03] Processing data file: bid_eligibility_document_file.txt

[15:49:03] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:03] Response status: 200 OK

[15:49:03] Processing data file: bid_financial_document_file.txt

[15:49:03] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:03] Response status: 200 OK

[15:49:03] Processing data file: bid_qualification_document_file.txt

[15:49:03] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:49:03] Response status: 200 OK

[15:49:03] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b32c1d39d4374fa7b2843e48b26c7a5c/bids
[15:49:04] Response status: 201 Created

[15:49:04] Document attached:
 - data.id              9deadb0852504eeabc52902db001d997
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/39ac7a7defb6468bb9af2ba7320bb725?Signature=J8uqZB8zTcAXZfCJ5upDQgAHztASObfPdzyKXBsinsXvPRI%2Fg064apfJ%2F5q9ihovGYftyAgbEkbDGF%2Bjabq0Cw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:04] Document attached:
 - data.id              edc5bf9364e746fc92ecb8d52743b9d2
 - data.confidentiality buyerOnly

[15:49:04] Document attached:
 - data.id              d5c9a60ca2694680be278401233eba4d
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/5af287eccc8042b4aeaefabaf1a9384f?Signature=UjIDGr9CL5rjVEolPfasa4zBHYjXyvS4Upr7YHumxxTL%2Bu9sLAqZke9wT4jM4t8iwawpqlhEmQ5oXkx7ULYsCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:04] Document attached:
 - data.id              65b091568f9c49b0b76a1ab17f444cd2
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/7005d3624f9043639a6fd6072b12b88f?Signature=Tw8wDdEYIWQBafo7iCS7Khdn%2B0eMrvdETfRrw3Lu9RoXqgh2%2FJKkY9oKUSZb7dA58%2BFOkXgjNtX%2BKK%2Bs9wBWCg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:04] Document attached:
 - data.id              5217642084bd49e98c217d57e87dbcdb
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/b7d428208f5b4de59d44aa2fff141938?Signature=Zv%2FDRnC7LVxOKxFWr8KrYePJpwh%2FkWsFEvuOu6N%2BLPYTU5SKu8vmY%2BVKaPQiyCdzQWgMjjrlfYTCtCiEgJbkCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:49:04] Bid created:
 - data.id              874b2e5ec0d24972bf79d0bd32b922ef
 - access.token         2fe43bd88ac34401a0909f17d838bab5
 - data.status          draft

[15:49:04] Completed.

[15:49:04] Summary
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
