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
[01:21:39] Using env file /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/.env.readme

[01:21:39] Press P to pause and show summary, S to show summary

[01:21:39] Using seed 285283

[01:21:39] Initializing cdb client

[01:21:39] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[01:21:39] Response status: 200 OK

[01:21:40] Client time delta with server: -1580 milliseconds

[01:21:40] Initializing ds client

[01:21:40] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[01:21:40] Response status: 200 OK

[01:21:40] Creating framework...

[01:21:40] Processing data file: framework_create.json

[01:21:40] Skipping...

[01:21:40] Creating plan...

[01:21:40] Processing data file: plan_create.json

[01:21:40] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[01:21:40] Response status: 201 Created

[01:21:40] Plan created:
 - data.id              1fcdd326976d4e09a8d26037ee878443
 - access.token         c7743a7200d5468e960fc505340c1242
 - access.transfer      6122d2276aa24720b30bd3de0bcfeded
 - data.status          draft

[01:21:40] Patching plan...

[01:21:40] Processing data file: plan_patch.json

[01:21:40] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/1fcdd326976d4e09a8d26037ee878443?acc_token=c7743a7200d5468e960fc505340c1242
[01:21:40] Response status: 200 OK

[01:21:40] Plan patched:
 - data.id              1fcdd326976d4e09a8d26037ee878443
 - data.status          scheduled

[01:21:40] Creating tender...

[01:21:40] Processing data file: tender_create.json

[01:21:41] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/1fcdd326976d4e09a8d26037ee878443/tenders
[01:21:41] Response status: 201 Created

[01:21:41] Tender created:
 - data.id              1cd58d2be8714dc3a4c9cdd8304a889a
 - access.token         622bd54a11b14b53bcfab95e825aeeba
 - access.transfer      26521ad050b74d5a94b2f8e830478680
 - data.status          draft
 - data.tenderID        UA-2026-09-11-000212-a
 - data.procurementMethodType closeFrameworkAgreementUA

[01:21:41] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cd58d2be8714dc3a4c9cdd8304a889a
[01:21:41] Response status: 200 OK

[01:21:41] Processing data file: tender_document_attach.json

[01:21:41] Processing data file: tender_document_file.txt

[01:21:41] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:41] Response status: 200 OK

[01:21:41] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cd58d2be8714dc3a4c9cdd8304a889a/documents?acc_token=622bd54a11b14b53bcfab95e825aeeba
[01:21:41] Response status: 201 Created

[01:21:41] Document attached:
 - data.id              e7f71f8760fc49149bc0cce525967e0d
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/9aa72c254bc543a2b35379b311f48084?Signature=tlNAM7ZOFU4snljVrEOfZcaQj5S%2F%2BbxZK3It2O1K6tB45IXIQl8DUAczcaOumSYftQc7N8Bp%2BvqTH3deU69ADg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:41] Processing data file: contract_proforma_attach.json

[01:21:41] Processing data file: contract_proforma.txt

[01:21:41] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:41] Response status: 200 OK

[01:21:41] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cd58d2be8714dc3a4c9cdd8304a889a/documents?acc_token=622bd54a11b14b53bcfab95e825aeeba
[01:21:41] Response status: 201 Created

[01:21:41] Document attached:
 - data.id              0ebb8b301bbc46f7a6597749de0f110f
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/a081211f72f24562afa8c8db55935465?Signature=4PkALGcX03lDd%2BDIVPEtSOEA0zcXxEgpMaIyZ35ZuAIW7IamwwryjkM1OQ4Q8VJD71gywUotgsSarxLRhHajBA%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[01:21:41] Create tender criteria...

[01:21:41] Processing data file: criteria_create.json

[01:21:41] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cd58d2be8714dc3a4c9cdd8304a889a/criteria?acc_token=622bd54a11b14b53bcfab95e825aeeba
[01:21:42] Response status: 201 Created

[01:21:42] Tender criteria created:
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

[01:21:42] Processing data file: tender_notice_attach.json

[01:21:42] Processing data file: tender_notice_file.p7s

[01:21:42] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:42] Response status: 200 OK

[01:21:42] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cd58d2be8714dc3a4c9cdd8304a889a/documents?acc_token=622bd54a11b14b53bcfab95e825aeeba
[01:21:42] Response status: 201 Created

[01:21:42] Document attached:
 - data.id              0c00b10c8bc04aa6865ed55f3cb936cc
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/badaf3f6b89b40ffb7bec48e9ae35ad0?Signature=H0kb2tpwPRuY%2FjXH%2FmCD2lajiQPEYAWCIayjRWutLVIa1GnBFUZe2ezAQhgnN5WlPJ%2FsC1tVWL84bAiljF6PBw%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[01:21:42] Patching tender...

[01:21:42] Processing data file: tender_patch.json

[01:21:42] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cd58d2be8714dc3a4c9cdd8304a889a?acc_token=622bd54a11b14b53bcfab95e825aeeba
[01:21:43] Response status: 200 OK

[01:21:43] Tender patched:
 - data.id              1cd58d2be8714dc3a4c9cdd8304a889a
 - data.status          active.tendering

[01:21:43] Skipping complaints creating: bot and reviewer tokens are required

[01:21:43] Creating bids...

[01:21:43] Processing data file: bid_create_0.json

[01:21:43] Processing data file: bid_document_file.txt

[01:21:43] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:43] Response status: 200 OK

[01:21:43] Processing data file: bid_confidential_document_file.txt

[01:21:43] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:44] Response status: 200 OK

[01:21:44] Processing data file: bid_eligibility_document_file.txt

[01:21:44] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:45] Response status: 200 OK

[01:21:45] Processing data file: bid_financial_document_file.txt

[01:21:45] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:45] Response status: 200 OK

[01:21:45] Processing data file: bid_qualification_document_file.txt

[01:21:45] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:45] Response status: 200 OK

[01:21:45] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cd58d2be8714dc3a4c9cdd8304a889a/bids
[01:21:45] Response status: 201 Created

[01:21:45] Document attached:
 - data.id              3f5913b89d7f49faa9602aa876b75de4
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/2a78282f37d04c70967eff2f38229035?Signature=YjPu74ZL%2F2GdzeIaVCfxBazwv4LgvGHO42mbdfeXT6C6%2BRHlGFYAr9xgN5XVLxrVp5OQ3kO8nkCOxF%2BoJhs4Bw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:45] Document attached:
 - data.id              1896c4acf77740f582a3b8024e9d99ea
 - data.confidentiality buyerOnly

[01:21:45] Document attached:
 - data.id              12a609332c2f47ec8f6cd3e1def0b069
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/afe78c4bd3814ec59aa6fcf62e385919?Signature=lTiBrsabo0zEhn0CqQ%2BS%2FSqJXasoVjBuYcVHZFUpkEcdqRc8YEo6F8wJ%2FmCwJpsn7wpyGqaZioptsDp5HFGxAg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:45] Document attached:
 - data.id              3f905c89c3654be092eb4bde93139ac6
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/ad9768e977c04bee87862d64e5023e99?Signature=oloEHG1yeHWxTGjufBFdaD9vJvtHXIATTewnPlySNa89knvu4TvtkR56leZGHu%2BhEgObK%2BP4suD3ay7PFhyHAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:45] Document attached:
 - data.id              d8a67d1657cb455bbdc7da05fb9a10a7
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/b245f36a376f41a4a81c92cc3eeb4e59?Signature=DNkwiyN4mLzzJiYowBtjgqsZ1cyYQHS9X7QLxWxpfQ0LNC1MxxGyepMISwA4cVSHBI2irX7XyN%2Ff%2BLXsOV8YBg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:45] Bid created:
 - data.id              ed3588a6e761468d87bc26a92dbc2f57
 - access.token         382a0fa0fe314533921e245ca8df931a
 - data.status          draft

[01:21:45] Processing data file: bid_create_1.json

[01:21:45] Processing data file: bid_document_file.txt

[01:21:45] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:46] Response status: 200 OK

[01:21:46] Processing data file: bid_confidential_document_file.txt

[01:21:46] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:47] Response status: 200 OK

[01:21:47] Processing data file: bid_eligibility_document_file.txt

[01:21:47] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:47] Response status: 200 OK

[01:21:47] Processing data file: bid_financial_document_file.txt

[01:21:47] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:47] Response status: 200 OK

[01:21:47] Processing data file: bid_qualification_document_file.txt

[01:21:47] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:47] Response status: 200 OK

[01:21:47] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cd58d2be8714dc3a4c9cdd8304a889a/bids
[01:21:49] Response status: 201 Created

[01:21:49] Document attached:
 - data.id              5f433f899f114abcbdba46654836426b
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/9cd565ded67149b8b997f6d77502dd1e?Signature=9OTkJYsN0246xvXXhe2oeXx8NDZfB4sIgpS3jKZ0pvgEEI1SzcWTnUL56rQ64dmeRbwHHc%2FJyAouZgXzgnl2Dg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:49] Document attached:
 - data.id              2b9fea2a461c45ec904c0fc84d91b660
 - data.confidentiality buyerOnly

[01:21:49] Document attached:
 - data.id              7cf58e80bb77400ab8f659eb4b8a1d68
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/9a450fbcb7b842e2a214c6024e405d1b?Signature=Fp%2BfsWeL%2BlbdWpwR5ev5g0xNvRvdETwR8tScehlbsYZT4kPuhVd1yzU3UuLhId28tbRDQ5qver%2FUFK%2FmEj0VBQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:49] Document attached:
 - data.id              4d42f0727d3e4d4ca33e6a7d280af79e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/97736ca6ccc641e2aa83f671405b043f?Signature=C5lokeOYLKp2sWQot4CEd6mGn2LFQTfPZ32t8ghWR%2FpysW%2FORXD3ktDt%2Fcjp6TES7TXOvmouC9z7f5%2ByJIllDw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:49] Document attached:
 - data.id              a4e1bfd6354744f896f543172f8a0b00
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/95996b8c3c5346288c7d912e2dd9be4a?Signature=3FCo%2Fw7cfTZ9HdgTYPHhqXVkyyzgry9zlMov3q8V6d47fFt3SKWViRbVvgRvffxgTw0AozV9E4vMBe%2B5P3aWCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:49] Bid created:
 - data.id              459116cbec0b47839f22d3edb8cbfab1
 - access.token         24583b4c81374e74960eb3cd6c482c86
 - data.status          draft

[01:21:49] Processing data file: bid_create_2.json

[01:21:49] Processing data file: bid_document_file.txt

[01:21:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:49] Response status: 200 OK

[01:21:49] Processing data file: bid_confidential_document_file.txt

[01:21:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:49] Response status: 200 OK

[01:21:49] Processing data file: bid_eligibility_document_file.txt

[01:21:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:49] Response status: 200 OK

[01:21:49] Processing data file: bid_financial_document_file.txt

[01:21:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:49] Response status: 200 OK

[01:21:49] Processing data file: bid_qualification_document_file.txt

[01:21:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:49] Response status: 200 OK

[01:21:49] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cd58d2be8714dc3a4c9cdd8304a889a/bids
[01:21:49] Response status: 201 Created

[01:21:49] Document attached:
 - data.id              03ebe71d29b24ef097864cfff9a3bf6b
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/7782519ac55e403f9f2ea4848011068b?Signature=3EOSMUiKAZd%2F1p5XYtfcfUPGz9KfrCE%2BvACa3N5YyYpXVDjO33bFsz7itTkEFCzUp5JiHo7VR7AgHVTkU0t8Dw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:49] Document attached:
 - data.id              16b30c56b5ae4888a52cf391fc13486d
 - data.confidentiality buyerOnly

[01:21:49] Document attached:
 - data.id              0e38987ff52f40eab705e67bbae35dfa
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/16d974de57d744f2951c90477c4c6cb2?Signature=TuXUHFZ9ZbekkH%2FefjXltxpTbMd51zQazx%2B5t9RkY9Erh1SbVwVT3ukGIWguurU%2BIhEa7aTtiXGcWc9nEU9cBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:49] Document attached:
 - data.id              146b53478ca64537bf8de3e11915b68b
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/fa8440f1074f45dab446709958af1f3a?Signature=b%2BbDyoUfTQKD4MOq6WV4URIyDC3Dl7VEbS4v0UxKEnoarIMuIVm7gFNTaC1r5Bdn%2F0y5BhgiUQdcY669XcMbBg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:49] Document attached:
 - data.id              602dd97600984ffcae8d8c036de6b5d9
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/5d261d94b64a4a08b263c2e128347469?Signature=UaRXFB%2BsseNuq89xV0YyKOgAv11XKRJLO7RMplZwb%2Bb96igRASrgqgeZ%2Fy8bbcA07nOLuxXWkTerRcmZ%2BHv2DA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:49] Bid created:
 - data.id              b4273547d87546d7a802e1b519b01985
 - access.token         33f98b33f9014a90aadfad4628bcffde
 - data.status          draft

[01:21:49] Processing data file: bid_create_3.json

[01:21:49] Processing data file: bid_document_file.txt

[01:21:49] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:50] Response status: 200 OK

[01:21:50] Processing data file: bid_confidential_document_file.txt

[01:21:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:50] Response status: 200 OK

[01:21:50] Processing data file: bid_eligibility_document_file.txt

[01:21:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:50] Response status: 200 OK

[01:21:50] Processing data file: bid_financial_document_file.txt

[01:21:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:50] Response status: 200 OK

[01:21:50] Processing data file: bid_qualification_document_file.txt

[01:21:50] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[01:21:50] Response status: 200 OK

[01:21:50] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/1cd58d2be8714dc3a4c9cdd8304a889a/bids
[01:21:50] Response status: 201 Created

[01:21:50] Document attached:
 - data.id              9125f4c8588a4bbd81d1d63f170b75a1
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/9d775425ea72402e9af50b4e715466a6?Signature=I8D3v4FGQsqONDY6yht1JkrF%2BU2xn7lgbvFmAjk%2FjWhU%2FWQIOwAz81L4imHgMdB28%2BAq1%2BXTxOdLktAZxHu9Dw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:50] Document attached:
 - data.id              4a0823c507a344ca8f1ec584d726b28b
 - data.confidentiality buyerOnly

[01:21:50] Document attached:
 - data.id              aa048074fa7b49ce8726149d2e901e57
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/6714022b927643949e0e2b41045b23ed?Signature=%2FBrg104%2BRLIpZmKFJ3RDUMaTfTSh4LFRCy1HM%2FUYFyulJqm1DVJSjPX2oDMoU9hGGn6QhxY3NeOjyUMppqoWCg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:50] Document attached:
 - data.id              e0e7f14caba9445daa48c7b7c12dc0f9
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/f3397f2ef4a1479a8984237ab5b5a7f4?Signature=JghA5K2I6%2FyYSUv0EstFcwh1Jbf%2Bzw5tTejXOjhNTJ4XOvYYqHfw8XbLNZ372OvzmC7koUy%2FAGBfF4o0TQr4Bg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:50] Document attached:
 - data.id              b02f4189095c46fd963ce42f2c80f73e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/39c0c38316324a6aa5cd277eb814e95c?Signature=WmiER2YS3bhyVz6MUBTg8FAXcDiFHr7Ou%2BMAdgIi1dKunCr8tPo%2BHNggLE2gmHoq2b%2BslRZb2192FSAr%2BjcAAA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[01:21:50] Bid created:
 - data.id              2083ca9a1ae64c4e946be9800886dbf2
 - access.token         726750261d93488ca622e2f784733b4d
 - data.status          draft

[01:21:50] Completed.

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
