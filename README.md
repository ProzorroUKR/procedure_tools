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
[15:45:38] Using env file /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/.env.readme

[15:45:38] Press P to pause and show summary, S to show summary

[15:45:38] Using seed 479326

[15:45:38] Initializing cdb client

[15:45:38] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[15:45:39] Response status: 200 OK

[15:45:39] Client time delta with server: -647 milliseconds

[15:45:39] Initializing ds client

[15:45:39] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[15:45:39] Response status: 200 OK

[15:45:39] Creating framework...

[15:45:39] Processing data file: framework_create.json

[15:45:39] Skipping...

[15:45:39] Creating plan...

[15:45:39] Processing data file: plan_create.json

[15:45:39] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[15:45:39] Response status: 201 Created

[15:45:39] Plan created:
 - data.id              06f7c47c82aa43488c48924c6ebeb203
 - access.token         517d67f7095c46b589a46ecd077811c5
 - access.transfer      96cc085afe0546f7a188b74bfa5c20bb
 - data.status          draft

[15:45:39] Patching plan...

[15:45:39] Processing data file: plan_patch.json

[15:45:39] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/06f7c47c82aa43488c48924c6ebeb203?acc_token=517d67f7095c46b589a46ecd077811c5
[15:45:39] Response status: 200 OK

[15:45:39] Plan patched:
 - data.id              06f7c47c82aa43488c48924c6ebeb203
 - data.status          scheduled

[15:45:39] Creating tender...

[15:45:39] Processing data file: tender_create.json

[15:45:39] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/06f7c47c82aa43488c48924c6ebeb203/tenders
[15:45:40] Response status: 201 Created

[15:45:40] Tender created:
 - data.id              0d749558f25943dca80c29d2cf6bcba2
 - access.token         5683bc11cb2d4d008e2cef033a4bd9a3
 - access.transfer      7953c86990364d08870aeaaaea02ca6e
 - data.status          draft
 - data.tenderID        UA-2026-09-15-000310-a
 - data.procurementMethodType closeFrameworkAgreementUA

[15:45:40] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/0d749558f25943dca80c29d2cf6bcba2
[15:45:40] Response status: 200 OK

[15:45:40] Processing data file: tender_document_attach.json

[15:45:40] Processing data file: tender_document_file.txt

[15:45:40] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:41] Response status: 200 OK

[15:45:41] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/0d749558f25943dca80c29d2cf6bcba2/documents?acc_token=5683bc11cb2d4d008e2cef033a4bd9a3
[15:45:41] Response status: 201 Created

[15:45:41] Document attached:
 - data.id              3128846ab7f74971852d99ea7fd762db
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/25bd92a3f39f4ae38f6964bf57028fdb?Signature=oPR9t6N6C0Aqd1JrJ1fNehaKTZrysishOz2Go%2FTL4sPa3qcm%2BC296pmTOqWPZVO%2Fretdp1wNHJuQQAw%2FBAFmDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:41] Processing data file: contract_proforma_attach.json

[15:45:41] Processing data file: contract_proforma.txt

[15:45:41] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:43] Response status: 200 OK

[15:45:43] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/0d749558f25943dca80c29d2cf6bcba2/documents?acc_token=5683bc11cb2d4d008e2cef033a4bd9a3
[15:45:43] Response status: 201 Created

[15:45:43] Document attached:
 - data.id              5b045382c9784202a29c03b6038f2960
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/f99df6f1f343487283704fff4b4b87e8?Signature=ROuIKAlA%2FQqSVljKi%2Bl98S8%2FRVXT%2B7N6T1o1fWp1XglIHe%2FPerLr6CupoyCBXNywnGwVgNtFeT3jv7uKKI%2BJDg%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[15:45:43] Create tender criteria...

[15:45:43] Processing data file: criteria_create.json

[15:45:43] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/0d749558f25943dca80c29d2cf6bcba2/criteria?acc_token=5683bc11cb2d4d008e2cef033a4bd9a3
[15:45:43] Response status: 201 Created

[15:45:43] Tender criteria created:
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

[15:45:43] Processing data file: tender_notice_attach.json

[15:45:43] Processing data file: tender_notice_file.p7s

[15:45:43] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:44] Response status: 200 OK

[15:45:44] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/0d749558f25943dca80c29d2cf6bcba2/documents?acc_token=5683bc11cb2d4d008e2cef033a4bd9a3
[15:45:44] Response status: 201 Created

[15:45:44] Document attached:
 - data.id              76ad7236e9614f218acf3fa2d21e2ba0
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/e1c10fd075764b6f877d6bd652ae6f25?Signature=yltYr63hJ2Ru27ZZnoF249VWBhHl5nsAEJlO%2BSfCAh7Nb1ZCwlelVG%2FkLcM8%2B1lxHQQ5pX1IoqGQ3Gyz7V3RCQ%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[15:45:44] Patching tender...

[15:45:44] Processing data file: tender_patch.json

[15:45:44] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/0d749558f25943dca80c29d2cf6bcba2?acc_token=5683bc11cb2d4d008e2cef033a4bd9a3
[15:45:44] Response status: 200 OK

[15:45:44] Tender patched:
 - data.id              0d749558f25943dca80c29d2cf6bcba2
 - data.status          active.tendering

[15:45:44] Skipping complaints creating: bot and reviewer tokens are required

[15:45:44] Creating bids...

[15:45:44] Processing data file: bid_create_0.json

[15:45:44] Processing data file: bid_document_file.txt

[15:45:44] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:45] Response status: 200 OK

[15:45:45] Processing data file: bid_confidential_document_file.txt

[15:45:45] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:46] Response status: 200 OK

[15:45:46] Processing data file: bid_eligibility_document_file.txt

[15:45:46] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:46] Response status: 200 OK

[15:45:46] Processing data file: bid_financial_document_file.txt

[15:45:46] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:47] Response status: 200 OK

[15:45:47] Processing data file: bid_qualification_document_file.txt

[15:45:47] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:47] Response status: 200 OK

[15:45:47] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/0d749558f25943dca80c29d2cf6bcba2/bids
[15:45:48] Response status: 201 Created

[15:45:48] Document attached:
 - data.id              ec8adc3e46644ae3815202cc886a773e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/0dedb37cb8ab47c4b48c4a451de69835?Signature=NHgPa6g1nxZmCVJmgzKiqdu8gpYQ5SlviKZqPYtcl7hV3aw%2F4zq50N5IVxL8WA9DFEowIHWAroXY7ffdr%2B1oAA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:48] Document attached:
 - data.id              a313fa1ecea242bb8e4c8caa1249f007
 - data.confidentiality buyerOnly

[15:45:48] Document attached:
 - data.id              c87db011437047acb637fb42c9881554
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/bd3cb71c1fa94cb29cfcbbe850b08aae?Signature=PvE0vejrQSFGIWenORdiRRW%2BylQGU%2BUnGNHXQ5eZ1w7wpPVHDgI3quyPiGAI7XgbpG4KJ7AOs8gbYZudzX0qBg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:48] Document attached:
 - data.id              fc8af218f6ea4d548ad1c4b14f76760a
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/55acf883a69e4373a82eaaa4c1ba9f67?Signature=qfbc2OtzKDJ7oeg5FR8hW4AaLl3yOptoPoEXXTf5ewDVmuce%2BOePOq6lTiQR0S2SDOs0NtVfKqdqP9sYj0H3BA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:48] Document attached:
 - data.id              402f5b8fc4094f82b95fb7928a8d0a10
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/b1f711ee4d2f4dd38f870f678a535ff8?Signature=mIl2bMooVRjVAmptZHV0IoigYdnfod5TwZ5d72yLD9AeuAjHQan1ok01bObDjk55FJV5sRxEjke%2B6FfxzBe%2BDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:48] Bid created:
 - data.id              e20f3c4f28ca435cbaaba8b84d255645
 - access.token         c268d894197e49468e63a331d88bb0a5
 - data.status          draft

[15:45:48] Processing data file: bid_create_1.json

[15:45:48] Processing data file: bid_document_file.txt

[15:45:48] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:48] Response status: 200 OK

[15:45:48] Processing data file: bid_confidential_document_file.txt

[15:45:48] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:48] Response status: 200 OK

[15:45:48] Processing data file: bid_eligibility_document_file.txt

[15:45:48] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:48] Response status: 200 OK

[15:45:48] Processing data file: bid_financial_document_file.txt

[15:45:48] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:48] Response status: 200 OK

[15:45:48] Processing data file: bid_qualification_document_file.txt

[15:45:48] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:48] Response status: 200 OK

[15:45:48] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/0d749558f25943dca80c29d2cf6bcba2/bids
[15:45:48] Response status: 201 Created

[15:45:48] Document attached:
 - data.id              acf734e953d94b3c92440cfa8db0fae0
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/863295dd22cb4499848b2997ae426eff?Signature=TqFEpdlKhcF0NZ8RpvFVPQi0XUz3qhvIAT6Dqa0YtUpqMUFBzVUObqcUaUZCuxISHNpjpn2iD7zo9%2FIpVLF%2BCA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:48] Document attached:
 - data.id              5f1d87b78481400bb5b1f3c1e2d7a448
 - data.confidentiality buyerOnly

[15:45:48] Document attached:
 - data.id              7ef73df3cba14cc1be42fd528d0c612f
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/6563195802e94611827c94f84e26386f?Signature=ddXhFJDP4FRax%2FzvfBkHjPs5w%2FS2aMbR4pqqAKcXBX3R1fR0m5t%2BbvaVc5GSGqdx0%2BwbI8u6r7ToDx%2FNSniPBw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:48] Document attached:
 - data.id              36f20c40ab5549ee9832bce6ebe07ab6
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/99f2aa6cb46d4c2181fef45311c2e6d1?Signature=QOMB7kDM6DtzpIfDNU6Vo%2Fpu%2FMdGEGBuVN9Wte7L3UINOITs%2BlO4xNt0ZHvOIQcvUi8UKdRICCs5S3yJ4Q%2BxCA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:48] Document attached:
 - data.id              f6b69af7ab1043128285031c5c50191e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/c52dba592bfb4f8e9350d7b324939ea8?Signature=83pAR9oYAjxNEBeNLgWjOviGhz9ERW7A6mNZYk8ESB99KcEUtFNTs9uxOZQ8MYAo%2FAcXgZUDkNXzeNDdsk5XBw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:48] Bid created:
 - data.id              f97b0d05ceb94bd2ac4df60884c3454a
 - access.token         f1b24e84fdeb42c694017c4513156b25
 - data.status          draft

[15:45:48] Processing data file: bid_create_2.json

[15:45:48] Processing data file: bid_document_file.txt

[15:45:48] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:49] Response status: 200 OK

[15:45:49] Processing data file: bid_confidential_document_file.txt

[15:45:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:49] Response status: 200 OK

[15:45:49] Processing data file: bid_eligibility_document_file.txt

[15:45:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:49] Response status: 200 OK

[15:45:49] Processing data file: bid_financial_document_file.txt

[15:45:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:49] Response status: 200 OK

[15:45:49] Processing data file: bid_qualification_document_file.txt

[15:45:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:49] Response status: 200 OK

[15:45:49] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/0d749558f25943dca80c29d2cf6bcba2/bids
[15:45:49] Response status: 201 Created

[15:45:49] Document attached:
 - data.id              5afb9eb254e94f71bffdca92ad8ea88b
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/44f2b54e2a5042ab84c1830fd40064d8?Signature=MQ%2Bd3co9%2BfiypMwLXS4bLSi%2BhyWBe897w3jjjWXtL%2BpgGm44LZtdpkEZ3XUUt8jYhLRnTRogj6nVXZkjAz7IBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:49] Document attached:
 - data.id              9998a7c05f734ea5bb8e2d76322cf129
 - data.confidentiality buyerOnly

[15:45:49] Document attached:
 - data.id              7885884ed9bc4025a0ad9ced8db0c8b8
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/374c0455c9684f149f74b78777d57a97?Signature=PS0ZtgFosjAYNpBMW3JqIGundtWhzNuNlspSPXlQ3JRp1lnMEih8H5x60q0d3Zk0UGJkfW7spSxWkGzr1TdNAA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:49] Document attached:
 - data.id              701b25d4b91049d9bbe65122ce99e66e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/eb5da7b6945d4abaa27a90a8de6ed2d5?Signature=FV2VQaU7%2FXgBGZoFTytS9dKDIWfATDgkmKm6K5OCsU7%2Fjizmgcr%2BtfaiORjpN4aRhz6s3OYJ9DyRqMKnn824AQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:49] Document attached:
 - data.id              4fe5527fb2854ead8d5932b2c4c5d6e6
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/b749cb978eda4157926fbc6d8c81fe5c?Signature=pomPBJ4%2FTb67gG%2FL7FDRRR2KNnMBvydVbtvuRQtsJf0l4Xy3VMSzVhD2zkZf1X%2BbvWr6gk1Jckm3V5uoOTJOCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:49] Bid created:
 - data.id              a5f23368547e4c7d875d4c0db58ffd0b
 - access.token         baa85c01856d4836b636d7b8ae2bd578
 - data.status          draft

[15:45:49] Processing data file: bid_create_3.json

[15:45:49] Processing data file: bid_document_file.txt

[15:45:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:49] Response status: 200 OK

[15:45:49] Processing data file: bid_confidential_document_file.txt

[15:45:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:50] Response status: 200 OK

[15:45:50] Processing data file: bid_eligibility_document_file.txt

[15:45:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:50] Response status: 200 OK

[15:45:50] Processing data file: bid_financial_document_file.txt

[15:45:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:50] Response status: 200 OK

[15:45:50] Processing data file: bid_qualification_document_file.txt

[15:45:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:45:50] Response status: 200 OK

[15:45:50] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/0d749558f25943dca80c29d2cf6bcba2/bids
[15:45:50] Response status: 201 Created

[15:45:50] Document attached:
 - data.id              076e95f35a494dd696a99cb7b6105488
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/00fd0f4f05194c3abdb2df82cd76e509?Signature=oy0tNpKgMKDx74VNhcer8sZS06JsacMSJVtK2axnTilp69SAADmmhzmiPR%2FYJv0kljHQaj1ZEuxlJ97CidPZBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:50] Document attached:
 - data.id              7dd660566c19492c9f549bc0cd891505
 - data.confidentiality buyerOnly

[15:45:50] Document attached:
 - data.id              13b3b7a6082944c3a54557faf3882bde
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/166bd6b8ae7c4b7ab0a8dbb2ca71ae1c?Signature=PBrlQsHZ0JF1aFh%2FDiwu3v3M1wS1Hoyk2d7mrGXW%2FF7B4v4AKToeeBJrrjpOJWyhJBFufdjzvRwOXWwVWsFYCg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:50] Document attached:
 - data.id              fe005ff8f005407ab5275dcd854cbec5
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/a7da8e62a8144c368d0a077cbefcb564?Signature=%2FCGCd6gU8o%2BCLtqOpUirr7YAMMKIHzfzZ3pUlTgHVWE1QZ8srKnBdCbOzYvISprzbTWWTQva0%2F3v0wBR8AcTCQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:50] Document attached:
 - data.id              a22814d901784ad4b62c0632cc8aaad8
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/2e6fcaf7d1104c94854e1a901f776b29?Signature=PBtPbpmWwRjBldvqWVc8PV59scrynVnBdvWCdV9UYFqYTw71M4EQis7NSq0mkhP6YeFHYdIhSulDKFddasdbBQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[15:45:50] Bid created:
 - data.id              34142f3ff41741828a610d81646f8456
 - access.token         9fe22c700bc440ae839848931b073282
 - data.status          draft

[15:45:50] Completed.

[15:45:50] Summary
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
