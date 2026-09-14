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

3. Install with pip:

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
[12:58:27] Using env file /Users/smithumble/Dev/prozorro/dev-other/procedure_tools/.env.readme

[12:58:27] Press P to pause and show summary, S to show summary

[12:58:27] Using seed 674762

[12:58:27] Initializing cdb client

[12:58:27] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[12:58:27] Response status: 200 OK

[12:58:27] Client time delta with server: -957 milliseconds

[12:58:27] Initializing ds client

[12:58:27] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[12:58:28] Response status: 200 OK

[12:58:28] Creating framework...

[12:58:28] Processing data file: framework_create.json

[12:58:28] Skipping...

[12:58:28] Creating plan...

[12:58:28] Processing data file: plan_create.json

[12:58:28] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[12:58:28] Response status: 201 Created

[12:58:28] Plan created:
 - data.id              66ce000e2c4d4828b22bdcfd25eb2cd4
 - access.token         4c5d04649ef1443e8edce073cf1e3a69
 - access.transfer      038964bcff27492bb5ba55c1d52225af
 - data.status          draft

[12:58:28] Patching plan...

[12:58:28] Processing data file: plan_patch.json

[12:58:28] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/66ce000e2c4d4828b22bdcfd25eb2cd4?acc_token=4c5d04649ef1443e8edce073cf1e3a69
[12:58:28] Response status: 200 OK

[12:58:28] Plan patched:
 - data.id              66ce000e2c4d4828b22bdcfd25eb2cd4
 - data.status          scheduled

[12:58:28] Creating tender...

[12:58:28] Processing data file: tender_create.json

[12:58:28] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/66ce000e2c4d4828b22bdcfd25eb2cd4/tenders
[12:58:28] Response status: 201 Created

[12:58:28] Tender created:
 - data.id              b18356f3bb114e11ae11881eeb2b7544
 - access.token         da23a1f83ee6459a85ff9796b9a327fd
 - access.transfer      836bf6ffd5af44bb8c15b0f3b9a8cf8c
 - data.status          draft
 - data.tenderID        UA-2026-09-14-000004-a
 - data.procurementMethodType closeFrameworkAgreementUA

[12:58:28] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b18356f3bb114e11ae11881eeb2b7544
[12:58:28] Response status: 200 OK

[12:58:28] Processing data file: tender_document_attach.json

[12:58:28] Processing data file: tender_document_file.txt

[12:58:28] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:28] Response status: 200 OK

[12:58:28] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b18356f3bb114e11ae11881eeb2b7544/documents?acc_token=da23a1f83ee6459a85ff9796b9a327fd
[12:58:29] Response status: 201 Created

[12:58:29] Document attached:
 - data.id              d8ef2233625148a486bee7a4701e2772
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/2131d7e9ed744837803f7815cd59b520?Signature=A9wlrWSo3Sj%2BbZOhWG%2Ft%2BO3ZibrNSLjimwmnUZTFRM%2B3lvvrzimAoRkAtVI7sWNNys%2Bx5E1a0t9Tnj2noa1NCg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:29] Processing data file: contract_proforma_attach.json

[12:58:29] Processing data file: contract_proforma.txt

[12:58:29] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:29] Response status: 200 OK

[12:58:29] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b18356f3bb114e11ae11881eeb2b7544/documents?acc_token=da23a1f83ee6459a85ff9796b9a327fd
[12:58:29] Response status: 201 Created

[12:58:29] Document attached:
 - data.id              120a027049264fff980b2cacfd786f9c
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/d952db7d90374931ac458ef0a7520eec?Signature=zqIZNIM49RLd5PG8B9rqttfcXsrcXX4npjfFOoMvVh5lycehcaI8rkAk8%2F%2F%2BerDH2yAscgrkWNCmwbkUwb7bCw%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[12:58:29] Create tender criteria...

[12:58:29] Processing data file: criteria_create.json

[12:58:29] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b18356f3bb114e11ae11881eeb2b7544/criteria?acc_token=da23a1f83ee6459a85ff9796b9a327fd
[12:58:29] Response status: 201 Created

[12:58:29] Tender criteria created:
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

[12:58:29] Processing data file: tender_notice_attach.json

[12:58:29] Processing data file: tender_notice_file.p7s

[12:58:29] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:29] Response status: 200 OK

[12:58:29] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b18356f3bb114e11ae11881eeb2b7544/documents?acc_token=da23a1f83ee6459a85ff9796b9a327fd
[12:58:30] Response status: 201 Created

[12:58:30] Document attached:
 - data.id              30dd654b72bc4c6bb79d85866022031d
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/5dd1a4c0111a4f3bb8198d2cd0d31485?Signature=Yr8F5KBo%2FHp8yklWr1%2Bw7QIY21QCt8KSfvycdyBcsxG72GXIiuuAJkHfWs5Q%2F2i70MCWQRpx1TzX6XCMyl4WAg%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[12:58:30] Patching tender...

[12:58:30] Processing data file: tender_patch.json

[12:58:30] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b18356f3bb114e11ae11881eeb2b7544?acc_token=da23a1f83ee6459a85ff9796b9a327fd
[12:58:30] Response status: 200 OK

[12:58:30] Tender patched:
 - data.id              b18356f3bb114e11ae11881eeb2b7544
 - data.status          active.tendering

[12:58:30] Skipping complaints creating: bot and reviewer tokens are required

[12:58:30] Creating bids...

[12:58:30] Processing data file: bid_create_0.json

[12:58:30] Processing data file: bid_document_file.txt

[12:58:30] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:30] Response status: 200 OK

[12:58:30] Processing data file: bid_confidential_document_file.txt

[12:58:30] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:30] Response status: 200 OK

[12:58:30] Processing data file: bid_eligibility_document_file.txt

[12:58:30] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:30] Response status: 200 OK

[12:58:30] Processing data file: bid_financial_document_file.txt

[12:58:30] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:30] Response status: 200 OK

[12:58:30] Processing data file: bid_qualification_document_file.txt

[12:58:30] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:31] Response status: 200 OK

[12:58:31] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b18356f3bb114e11ae11881eeb2b7544/bids
[12:58:31] Response status: 201 Created

[12:58:31] Document attached:
 - data.id              2da45315d5e940fd9ee0a8123e96328b
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/9b229b524c844e52a58f5ed9e0f4299d?Signature=2yjFT2EVEDTFubX6drsPO2BNAI0%2FfBvCl4kcx51rPHx6vhYJ6rWAzlcnyBkLKJNcBwKJvus%2Bgi91aQelE8qkAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:31] Document attached:
 - data.id              3212cb66857a45c480ee92f39ebcc3e0
 - data.confidentiality buyerOnly

[12:58:31] Document attached:
 - data.id              7a9c09f943ad4428afa22db1b6ea543f
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/6686d746cb204ff99fa87809c22a45c9?Signature=mB6%2B1775ThzaGDuGG9H7WFlkZYx4695bzJZZ0oe0esvtSapTSWPhHzBucqNwWtWgqyR06z%2FEOHg0wHjdrnVxDw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:31] Document attached:
 - data.id              3ba35649280d41258e2a6faaa2f9b58e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/004cfb950caa484b8b766239fed86a4e?Signature=KWhhD2AjtAaNjUWF03%2BQlsfLWDvz5pSaIUQb6FRu8RBdgFXY7wLjYQ0raZ7E9B3DZ%2FmF27EiopmYMDUmIUY%2BDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:31] Document attached:
 - data.id              fae354582c284230aff7017e6e665e64
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/b0b9961c051748c989f3503a9c71faaf?Signature=XHu6Gk0J9Ds8Ni5wCt93hRojmm9x75zDhhQtgA7xa%2BJBxRqLbJZA7Vk003pI%2FCqZ011y6IcP7Tf5mZ1zveZsBw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:31] Bid created:
 - data.id              a07387ec83de48da95935188fbd15d33
 - access.token         0c78049c354a42959a09cbca50b85999
 - data.status          draft

[12:58:31] Processing data file: bid_create_1.json

[12:58:31] Processing data file: bid_document_file.txt

[12:58:31] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:31] Response status: 200 OK

[12:58:31] Processing data file: bid_confidential_document_file.txt

[12:58:31] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:31] Response status: 200 OK

[12:58:31] Processing data file: bid_eligibility_document_file.txt

[12:58:31] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:31] Response status: 200 OK

[12:58:31] Processing data file: bid_financial_document_file.txt

[12:58:31] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:31] Response status: 200 OK

[12:58:31] Processing data file: bid_qualification_document_file.txt

[12:58:31] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:31] Response status: 200 OK

[12:58:31] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b18356f3bb114e11ae11881eeb2b7544/bids
[12:58:32] Response status: 201 Created

[12:58:32] Document attached:
 - data.id              b73f181a066f40f3bfc6a9457800c766
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/882b8181e26a4499b3dc39dc14f3936d?Signature=bYqy%2B379gZ%2B%2Bul8Xi6UxnfM9cJMGYoCRWxwJTF88BP10HM%2BtYQflpDVu%2FX4e41du9xbyU%2FVdNVteR7Ntj1xfDw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:32] Document attached:
 - data.id              e9cb52f054254ef6ba383f1e996ad734
 - data.confidentiality buyerOnly

[12:58:32] Document attached:
 - data.id              eef1708792074baa81fdd90220961549
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/64ed3ed506964545a1691c267e3cc3ae?Signature=mS5v9lkk4QnBLnZ92NGWk1CyqL4HUs2qMOtINmZjFE22AgEu8MVDUXEZ2ABjp5K2qSwHjlkB15fJM6qKG7DjCQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:32] Document attached:
 - data.id              9de4484422374470b2f4c2faadba66f8
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/9a21d1cadc034e3384b396efcfb1cd2c?Signature=r6hC9P2bxny%2B%2FWMx2GnD7ZggcbxnlWtfN1z0nxuR%2Bsh%2F7h85Iy4k3PLyNNOva4VK3uY6qpjB42s2N4W1V25VDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:32] Document attached:
 - data.id              ec7f4b8008424c8ca94e482983a4ccca
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/9851372bc4e94e2f8a4fa5c096391238?Signature=oCundUm3Me4uf26ogoCz2Ztrgp%2FGkjaBE2CRK7mK2mp2ymf%2FkJRa%2FthQNULz%2Fl%2FRARHJikumXQ0ittFI0BQ6AQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:32] Bid created:
 - data.id              eaa8c49e868c44eba216945745a2d406
 - access.token         99e5300a91df489eb2f1526e67ca2b96
 - data.status          draft

[12:58:32] Processing data file: bid_create_2.json

[12:58:32] Processing data file: bid_document_file.txt

[12:58:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:32] Response status: 200 OK

[12:58:32] Processing data file: bid_confidential_document_file.txt

[12:58:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:32] Response status: 200 OK

[12:58:32] Processing data file: bid_eligibility_document_file.txt

[12:58:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:32] Response status: 200 OK

[12:58:32] Processing data file: bid_financial_document_file.txt

[12:58:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:32] Response status: 200 OK

[12:58:32] Processing data file: bid_qualification_document_file.txt

[12:58:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:32] Response status: 200 OK

[12:58:32] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b18356f3bb114e11ae11881eeb2b7544/bids
[12:58:33] Response status: 201 Created

[12:58:33] Document attached:
 - data.id              c7060963864a44ed82f36fb5f0e44941
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/ecf13c30687f49d78350cce1d93c8888?Signature=gz9Q5srwBMtGKHPxjYZ%2BJNWwMuO5nkK5v6QbQQ2PfFJxamniYmzdw6qYjTr1tBMXy1G3%2BSJaVj9WxbBYLaIODA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:33] Document attached:
 - data.id              df81aef86e204e88963c4b068fcd342b
 - data.confidentiality buyerOnly

[12:58:33] Document attached:
 - data.id              6af44e8db1a2429dbad391ed1a13a543
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/457ddabfc53041639ff6afa5640ee6ba?Signature=G5fxA9OOMFvG0m37AJ2vUqOkKmeWBKykUoTNYWBZORuabS36TK0lGZfbs%2FLlmz5lKUHrdxic6ZiTA3d7gyT6Bw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:33] Document attached:
 - data.id              5de45f6453d74114afe9523e364a0456
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/aa710f7b76aa47a1bdfc75f1ce888257?Signature=g4KLXpBo8A3dZCpWls4X6F5FlW1AWvPcYDo%2Fgw%2FCeWK%2FXOKun6BWyf0nKDNqvyBQTcScdHEjOWLR6S49IZWUDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:33] Document attached:
 - data.id              7722d3329f7440c685b7d003748de1d9
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/690350622a714134b142a03b72d2e037?Signature=%2BHdcqodeL7X7yDaTEXzbqj3XxyVjqfarAdfUMPvkN%2BgsIjVW85wbnor9JFAl1EzEic%2FxiEbTCZ8nkgYzyLt3BA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:33] Bid created:
 - data.id              691b5394b00643868f9b74e4c63455b4
 - access.token         8b8c7f2947564e42aefc7137ea8689ad
 - data.status          draft

[12:58:33] Processing data file: bid_create_3.json

[12:58:33] Processing data file: bid_document_file.txt

[12:58:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:33] Response status: 200 OK

[12:58:33] Processing data file: bid_confidential_document_file.txt

[12:58:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:33] Response status: 200 OK

[12:58:33] Processing data file: bid_eligibility_document_file.txt

[12:58:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:33] Response status: 200 OK

[12:58:33] Processing data file: bid_financial_document_file.txt

[12:58:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:33] Response status: 200 OK

[12:58:33] Processing data file: bid_qualification_document_file.txt

[12:58:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[12:58:33] Response status: 200 OK

[12:58:33] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/b18356f3bb114e11ae11881eeb2b7544/bids
[12:58:33] Response status: 201 Created

[12:58:33] Document attached:
 - data.id              13a3a39e5a5c44d9b07d85b6a8761eca
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/16a6d2450fc04c07a665f2fb277fb803?Signature=2Rs50Q%2BVqdI7tNXY9bc7KgKuYO9S%2BdHd3U9lGkskJyZ62DMGdU9LPpFWD138EXPs0TrIIEj4koBTDre4zCnXBw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:33] Document attached:
 - data.id              d42e0a0707b74cbf8889c4435c223bab
 - data.confidentiality buyerOnly

[12:58:33] Document attached:
 - data.id              0e1ac519f39c46bc99f06ba323fd0d8f
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/1aa5c57a64cb4237adf8c31d8a2eea80?Signature=KxIsbpAE8CTEVPp6R1QZbrgW6AbcqGHTcep6RNzRTx5J%2Bb9DBFOkvY8854JYLmWdx0CfyXr%2FDCFcvMZ4dUEjAA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:33] Document attached:
 - data.id              ed7ba28d1ef6460181b09757cf222a3f
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/35764c2a3c33445b9c97e3dc7194427c?Signature=8oDt0qavEMHQ%2FdODpXl7XVCTz3pBaRvFlwrXDUcLCAyd9pqUYcscXkSynGdDVT7GK00fsZSkLA3j9lU7R%2BF0Ag%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:33] Document attached:
 - data.id              9bd0ad7c79e24f959ab82cb4c5d6113e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/1711cf2840f249e1a1c5661bdaa62804?Signature=Oyxja%2F1oWhuwzqpOfVi5UCO5mw4U8kGKMRdFln2LqSIvUri6UvUR0DQcpJlpXSd7ugDByky40EDM%2FFVjGgs0Ag%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[12:58:33] Bid created:
 - data.id              09af80f6b4454a0ba6a1164442f2de21
 - access.token         6acc5795c4a14d6ebaa2fbdb604394ac
 - data.status          draft

[12:58:33] Completed.

[12:58:33] Summary
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
