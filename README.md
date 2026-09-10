# procedure_tools

## Install

1. Clone

    ```
    git clone https://github.com/ProzorroUKR/procedure_tools.git
    ```

2. Navigate to cloned folder:

    ```
    cd procedure_tools
    ```

3. Install with pip

    * vanilla:

        ```
        pip install -e .
        ```

    * colorized output:

        ```
        pip install -e .[color]
        ```

    * with tests requirements:

        ```
        pip install -e .[test]
        ```

## Update

1. Pull

    ```
    git pull
    ```

    In case of conflicts:

    * Undo changes in project folder or reset with command

        ```
        git reset --hard
        ```

    * Pull again

        ```
        git pull
        ```

    * If this did not help, clean project folder

        ```
        git clean -fd
        ```

    * Pull again

        ```
        git pull
        ```

2. Install

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
                         - negotiation.quick
                         - priceQuotation
                         - reporting
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

All CLI parameters can be set in an env file. Command-line arguments override the file.

Copy an example file for the environment you need:

```
cp .env.sandbox.example .env.sandbox
cp .env.staging.example .env.staging
cp .env.dev.example .env.dev
```

Use `--env` (or `-E`) to select the file for the current run. It accepts a path or an environment name and looks up `.env.<name>`, `<name>.env`, or `envs/<name>`. If omitted, `PROCEDURE_ENV` is used, otherwise `.env` when that file exists.

```
procedure --env sandbox --data closeFrameworkAgreementUA
procedure --env .env.dev --data closeFrameworkAgreementUA
PROCEDURE_ENV=sandbox procedure --data closeFrameworkAgreementUA
```

Override selected values from the command line:

```
procedure --env sandbox --token other_token --data closeFrameworkAgreementUA
```

## Usage example

### With env file

Create with default data
```
procedure --env sandbox --data=closeFrameworkAgreementUA
```

Create with default data and stop after specific data file
```
procedure --env sandbox --data=closeFrameworkAgreementUA --stop=bid_create_3.json
```

Create with custom data files (relative path)
```
procedure --env sandbox --data=customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path)
```
procedure --env sandbox --data=/Users/JonhDoe/customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path, Windows)
```
procedure --env sandbox --data=C:\Users\JonhDoe\customdata\closeFrameworkAgreementUA
```

### Without env file

Create with default data
```
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA
```

Create with default data and stop after specific data file
```
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA --stop=bid_create_3.json
```

Create with custom data files (relative path)
```
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path)
```
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=/Users/JonhDoe/customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path, Windows)
```
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=C:\Users\JonhDoe\customdata\closeFrameworkAgreementUA
```

## Output example
```
procedure --env sandbox --data=closeFrameworkAgreementUA --stop=bid_create_4.json
```
```
[00:42:49] Using env file /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/.env.readme

[00:42:49] Using seed 290636

[00:42:49] Initializing cdb client

[00:42:49] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[00:42:49] Response status: 200 OK

[00:42:49] Client time delta with server: -662 milliseconds

[00:42:49] Initializing ds client

[00:42:49] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[00:42:49] Response status: 200 OK

[00:42:49] Creating framework...

[00:42:49] Processing data file: framework_create.json

[00:42:49] Skipping...

[00:42:49] Creating plan...

[00:42:49] Processing data file: plan_create.json

[00:42:49] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[00:42:49] Response status: 201 Created

[00:42:49] Plan created:
 - data.id              97910858824c42c5890964634fdbe32e
 - access.token         c9a5473eeccf4c6b97d6887da2289b4e
 - access.transfer      3475dddc87fd48168160ff06f7b4f0e5
 - data.status          draft

[00:42:49] Patching plan...

[00:42:49] Processing data file: plan_patch.json

[00:42:49] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/97910858824c42c5890964634fdbe32e?acc_token=c9a5473eeccf4c6b97d6887da2289b4e
[00:42:49] Response status: 200 OK

[00:42:49] Plan patched:
 - data.id              97910858824c42c5890964634fdbe32e
 - data.status          scheduled

[00:42:49] Creating tender...

[00:42:49] Processing data file: tender_create.json

[00:42:50] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/97910858824c42c5890964634fdbe32e/tenders
[00:42:50] Response status: 201 Created

[00:42:50] Tender created:
 - data.id              710372582cfd4ac99f8de4fb27767914
 - access.token         65e4ab639b134ab6823713de78dd8d82
 - access.transfer      aca0190266324ae89f47198113a15c79
 - data.status          draft
 - data.tenderID        UA-2026-09-11-000069-a
 - data.procurementMethodType closeFrameworkAgreementUA

[00:42:50] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/710372582cfd4ac99f8de4fb27767914
[00:42:50] Response status: 200 OK

[00:42:50] Processing data file: tender_document_attach.json

[00:42:50] Processing data file: tender_document_file.txt

[00:42:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:50] Response status: 200 OK

[00:42:50] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/710372582cfd4ac99f8de4fb27767914/documents?acc_token=65e4ab639b134ab6823713de78dd8d82
[00:42:50] Response status: 201 Created

[00:42:50] Document attached:
 - data.id              d47614a7bfa74990a3b5c6fd041efd1f
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/0af9c263de5e429a812a9f029c449987?Signature=H%2B9ezXrCBkMcR%2B00f8pO8MHLGaM4rYPBdlFFLuYAcTKC50ZNVOasUn0%2B4VIKFjtsW3GwhCf0%2FZUPHGaBRYKBAg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:50] Processing data file: contract_proforma_attach.json

[00:42:50] Processing data file: contract_proforma.txt

[00:42:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:51] Response status: 200 OK

[00:42:51] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/710372582cfd4ac99f8de4fb27767914/documents?acc_token=65e4ab639b134ab6823713de78dd8d82
[00:42:51] Response status: 201 Created

[00:42:51] Document attached:
 - data.id              7214d9b83bb943ab80006b9bf16e6543
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/5519ab2387e64443a9c189db6db2ec45?Signature=10zhO%2FqVIBVBWDFVQT8qzcL4RaIGIAU6nF%2BnNS4qrkQsWm5EKbqtgZphTH8ir5AEZZz52nN39f%2BEL0WoU8QfCA%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[00:42:51] Create tender criteria...

[00:42:51] Processing data file: criteria_create.json

[00:42:51] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/710372582cfd4ac99f8de4fb27767914/criteria?acc_token=65e4ab639b134ab6823713de78dd8d82
[00:42:51] Response status: 201 Created

[00:42:51] Tender criteria created:
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

[00:42:51] Processing data file: tender_notice_attach.json

[00:42:51] Processing data file: tender_notice_file.p7s

[00:42:51] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:51] Response status: 200 OK

[00:42:51] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/710372582cfd4ac99f8de4fb27767914/documents?acc_token=65e4ab639b134ab6823713de78dd8d82
[00:42:51] Response status: 201 Created

[00:42:51] Document attached:
 - data.id              9871207da8b346a7a2d50f4bfb027d75
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/5415f25a0303447f8af19c0e77400ad2?Signature=3AESnbZRsjVVHaeUTEL2ziwBMeZL4zOr01VrWW%2F6tOvy1FCVqZbGzIl%2FU%2BiPls868mMtjS0SVtg6F%2BLJGd0ICw%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[00:42:51] Patching tender...

[00:42:51] Processing data file: tender_patch.json

[00:42:51] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/710372582cfd4ac99f8de4fb27767914?acc_token=65e4ab639b134ab6823713de78dd8d82
[00:42:52] Response status: 200 OK

[00:42:52] Tender patched:
 - data.id              710372582cfd4ac99f8de4fb27767914
 - data.status          active.tendering

[00:42:52] Skipping complaints creating: bot and reviewer tokens are required

[00:42:52] Creating bids...

[00:42:52] Processing data file: bid_create_0.json

[00:42:52] Processing data file: bid_document_file.txt

[00:42:52] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:52] Response status: 200 OK

[00:42:52] Processing data file: bid_confidential_document_file.txt

[00:42:52] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:52] Response status: 200 OK

[00:42:52] Processing data file: bid_eligibility_document_file.txt

[00:42:52] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:52] Response status: 200 OK

[00:42:52] Processing data file: bid_financial_document_file.txt

[00:42:52] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:52] Response status: 200 OK

[00:42:52] Processing data file: bid_qualification_document_file.txt

[00:42:52] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:52] Response status: 200 OK

[00:42:52] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/710372582cfd4ac99f8de4fb27767914/bids
[00:42:52] Response status: 201 Created

[00:42:52] Document attached:
 - data.id              5621128b03694fbeb0ab58e501b9528d
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/2f0f7b544752436baf7fa309805991d0?Signature=aFyVvcgErRe2%2FLzsIuiceWxFaYdX%2FKXogtuiZjM6XoRxvz%2BCVfGSNGyvMz5sHkuDupYLiSt6DVX%2BYUA2cyDFDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:52] Document attached:
 - data.id              694e08181a664960a2953a39c3d47dcb
 - data.confidentiality buyerOnly

[00:42:52] Document attached:
 - data.id              3389dc34c29c418186fb4d6d071fc1c2
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/6b00d007595e4e58b797b16911737628?Signature=SHqBnQi1vAGmMiX8FtG4xl%2B33tBGzyHGiw%2FDa4T%2BIyfcErRAC3Tf%2F71DB9veXtMeMW7sRGUYKooQYPSRtekGCA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:52] Document attached:
 - data.id              0d6a97e27b3e4087878dba36c5ae0a43
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/c7fcd427c98c4615ab62e0a679612c19?Signature=WaKs4iWnGIf0K9xplcBMr%2FCOWIVutg0PXuCgYlMjX%2FPO%2B2%2BKzmm0L7T%2BXTgFUQNUrMb2AgC16hpUbFQ4abCKCg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:52] Document attached:
 - data.id              44aa04d38dba4822a26ff1d8fabbe749
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/39a75be68d1248cd8643dec63cd43033?Signature=8CFyKzcpfImX4RThowl4rNtcS2ujtqVLDRBLeN04%2BHd%2Fassx60BZVJl78g2MEQX9b0qcCE5IDLd6VJpTlfWvDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:52] Bid created:
 - data.id              f29e4c8d97614ada9eb825b5bab670f9
 - access.token         c9be67e0a09f47f38809d177dad27e29
 - data.status          draft

[00:42:52] Processing data file: bid_create_1.json

[00:42:53] Processing data file: bid_document_file.txt

[00:42:53] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:53] Response status: 200 OK

[00:42:53] Processing data file: bid_confidential_document_file.txt

[00:42:53] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:53] Response status: 200 OK

[00:42:53] Processing data file: bid_eligibility_document_file.txt

[00:42:53] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:53] Response status: 200 OK

[00:42:53] Processing data file: bid_financial_document_file.txt

[00:42:53] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:53] Response status: 200 OK

[00:42:53] Processing data file: bid_qualification_document_file.txt

[00:42:53] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:53] Response status: 200 OK

[00:42:53] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/710372582cfd4ac99f8de4fb27767914/bids
[00:42:53] Response status: 201 Created

[00:42:53] Document attached:
 - data.id              2e1e9a991938482da07980d58129ca22
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/1fb0afddd0fc41fbb2a9933979ed3c51?Signature=uVJZm3J3sDOUhMISgc1WtNMXIw6zpC%2FI82rSNLGHr6Pd2wPNfZub7N8TGe%2Fl7ZDBJGXKLArXiBG1vh5BqyWYAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:53] Document attached:
 - data.id              29f2c0b0b82a4c6b8c21db28014f07a2
 - data.confidentiality buyerOnly

[00:42:53] Document attached:
 - data.id              7b05e15853b144ceaa5566e8f33ecadb
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/aa33278899de4f2593047eb8aa649fe8?Signature=N9YUufQXgSBaSQyQ6tzuK%2BxgKgRxqcFQrz3sYrqUgMIJGt2wvHhA0%2BzUVqUPHjQBdUI48JIWxkdVygdCy4bdAA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:53] Document attached:
 - data.id              e69ffbea2a9341b789b8ee433e55b359
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/08ed6c38d5af4e8da95d77af4e68e765?Signature=eCXjP7GwJwZPfTmR5oNVwgB85P45zSvyRx%2FM1rTUL44itDgc0%2FVDHZIENnQDehmHwOe4oRpfIh3Dd8JNFY%2BsDw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:53] Document attached:
 - data.id              aabc6c726a1a465d9157c9a422f29bf4
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/d924a3f116f14842a3b9a2d2e19bc8b8?Signature=JpKuhqaVSn35sYPfneRz%2BhupgRh1sF7sQ%2BTdcQ09Bv1Zl19pzegdjN5MQr8QknH1jnpYM94SttJtFmkgxOwtDQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:53] Bid created:
 - data.id              701e57c5c12348bb89c3a56aad0510a4
 - access.token         6f730161c5a44e3f902382e99b49a858
 - data.status          draft

[00:42:53] Processing data file: bid_create_2.json

[00:42:53] Processing data file: bid_document_file.txt

[00:42:53] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:53] Response status: 200 OK

[00:42:53] Processing data file: bid_confidential_document_file.txt

[00:42:53] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:54] Response status: 200 OK

[00:42:54] Processing data file: bid_eligibility_document_file.txt

[00:42:54] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:54] Response status: 200 OK

[00:42:54] Processing data file: bid_financial_document_file.txt

[00:42:54] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:54] Response status: 200 OK

[00:42:54] Processing data file: bid_qualification_document_file.txt

[00:42:54] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:54] Response status: 200 OK

[00:42:54] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/710372582cfd4ac99f8de4fb27767914/bids
[00:42:54] Response status: 201 Created

[00:42:54] Document attached:
 - data.id              6abf2278fa9f462497dc649ddf353af3
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/1b3af0b1aa844c9893f4fdb3bca43a89?Signature=lulrCGIc%2FFZCudUzrsboBmf0rw%2B0Dr6GVhEqLnJC5zIqsXNv%2FaC8yoLB7onzZ5MXICxwFhqapfKFvWHCmhuABg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:54] Document attached:
 - data.id              d341478af82747aebb9d3c5a4ac90d2f
 - data.confidentiality buyerOnly

[00:42:54] Document attached:
 - data.id              3a0c22c654164b88bff957a28f1d9dd4
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/51fec7ee7cd94d83b277bb4d2906367d?Signature=3yx9J4CoT8Qz1xlQOWXSqihkEtxA8ryTdgFKqPXKoSiLx8wNmPaIojf0v%2FPNVfEnqs4CD25nXiMivoj0L7iiCQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:54] Document attached:
 - data.id              e468a2397e1e423f8fe74def2145fb66
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/9a5f1c515b7c46f2ab209e9d21de68fb?Signature=3g5leroKJp3obt%2F0JEyxpv5lwiYroeADJPAltJx4l3RA1Ln9n44IUl0hnFG6yfOkdDek0pLZGABDjMyetpssAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:54] Document attached:
 - data.id              0d6b83ad349d4499a2e934e6e4a16062
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/cea591eb2a604461bf0679fa7d09f91d?Signature=jDSlywYl7Qht63J7zvVmE4IErgohekmMC7jNI63QaqnTEHNZgkjh4mN6H5v7zfJ%2FR8tegtUbUz%2FhuIiyqFNeDQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:54] Bid created:
 - data.id              a8a6d494331a4e15b87f582512ccfa39
 - access.token         7aaf227230364c7d9799594bd5798e27
 - data.status          draft

[00:42:54] Processing data file: bid_create_3.json

[00:42:54] Processing data file: bid_document_file.txt

[00:42:54] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:54] Response status: 200 OK

[00:42:54] Processing data file: bid_confidential_document_file.txt

[00:42:54] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:54] Response status: 200 OK

[00:42:54] Processing data file: bid_eligibility_document_file.txt

[00:42:54] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:55] Response status: 200 OK

[00:42:55] Processing data file: bid_financial_document_file.txt

[00:42:55] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:55] Response status: 200 OK

[00:42:55] Processing data file: bid_qualification_document_file.txt

[00:42:55] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:42:55] Response status: 200 OK

[00:42:55] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/710372582cfd4ac99f8de4fb27767914/bids
[00:42:55] Response status: 201 Created

[00:42:55] Document attached:
 - data.id              07f47c5323404fd68d31653d6f864efc
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/d6deb1417f7f4e8db6b003b21a539fc2?Signature=OZzgUX1eALpL9N%2FQiJ494QHsGolmGiKY%2BwS%2F9Ka7OpMLdg0OKI3fxoFMBHsLZfABZBac8MO858lnPiJsbWujDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:55] Document attached:
 - data.id              0f0f818744684582baabe71351acd27d
 - data.confidentiality buyerOnly

[00:42:55] Document attached:
 - data.id              4545a2fe66a9469087438b601dc91044
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/7a226d0361f246a1ab96d6e359ede4f0?Signature=g7dtqR%2FNj0xZRAbWwKnFm9oeXU0b0Gi3zMu8hPM6oBSk8JoX1D50DXvTqB8FnhbRFnnojuAj3%2B1ardnQP3zaCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:55] Document attached:
 - data.id              01a63b416b374e588446451411ed0886
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/e7164fad6aaf440490e85a770f7207ae?Signature=LmNQi8F6ooi11zfCNFXTa5NuoCWrUs%2FDcg%2BdkHcZRWxzN5CyJD9r7ogjz80TTi6v2U%2FzclqYVuuJKbtIN3MXAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:55] Document attached:
 - data.id              86b3eb043d6e47b39eff14ab1e9c98a9
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/025a85ebc05d4223afd2f88b1c55b44a?Signature=b%2BucKQzcOkLfeQHdLwI3RQw8uZ7QFeQYCq92MnkJSOXu4iMkeuVf%2Fi3v2p8%2FgCsoNFtyGyed%2F3eYZFPYfjO7DA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[00:42:55] Bid created:
 - data.id              2d95bbd8167a4705977136958a307407
 - access.token         6964e92a9be645dfa2b155e40907a3ec
 - data.status          draft

[00:42:55] Completed.

```

## Update readme

Copy and fill `.env.readme`:

```
cp .env.readme.example .env.readme
```

then run:

```
./README.sh
```

## Run tests

Copy and fill `.env.test`, then run:

```
cp .env.test.example .env.test
pytest
```
