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
usage: procedure [-h] [-v] [-a 460800] [-p /api/0/] [-d aboveThresholdUA]
                 [-m quick(mode:no-auction)] [-s tender_create.json]
                 [--pause tender_create.json] [-w edr-qualification] [-e SEED]
                 [--reviewer-token REVIEWER_TOKEN] [--bot-token BOT_TOKEN]
                 [--debug] [--debug-req] [--debug-json-level DEBUG_JSON_LEVEL]
                 host token ds_host ds_username ds_password

positional arguments:

  host                  CDB API Host

  token                 CDB API Token

  ds_host               DS API Host

  ds_username           DS API Username

  ds_password           DS API Password

options:

  -h, --help            show this help message and exit

  -v, --version         show program's version number and exit

  -a 460800, --acceleration 460800
                        acceleration multiplier

  -p /api/0/, --path /api/0/
                        api path

  -d aboveThresholdUA, --data aboveThresholdUA
                        data files, custom path or one of:
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

  -m quick(mode:no-auction), --submission quick(mode:no-auction)
                        value for submissionMethodDetails, one of:
                         - quick
                         - quick(mode:no-auction)
                         - quick(mode:fast-auction)
                         - quick(mode:fast-forward)

  -s tender_create.json, --stop tender_create.json
                        data file name to stop after

  --pause tender_create.json
                        data file name(s) to pause after (comma-separated)

  -w edr-qualification, --wait edr-qualification
                        wait for event, one or many of (divided by comma):
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

## Usage example

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
procedure https://lb-api-sandbox-2.prozorro.gov.ua broker_api_token https://upload-docs-sandbox-2.prozorro.gov.ua broker_ds_username broker_ds_password --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA --stop=bid_create_4.json
```
```
[10:30:30] Using seed 801738

[10:30:30] Initializing cdb client

[10:30:30] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[10:30:30] Response status: 200 OK

[10:30:30] Client time delta with server: -574 milliseconds

[10:30:30] Initializing ds client

[10:30:30] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[10:30:30] Response status: 200 OK

[10:30:30] Creating framework...

[10:30:30] Processing data file: framework_create.json

[10:30:30] Skipping...

[10:30:30] Creating plan...

[10:30:30] Processing data file: plan_create.json

[10:30:30] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[10:30:30] Response status: 201 Created

[10:30:30] Plan created:
 - data.id              e8dbb846f1934d0cbfa2d2cf8fa7305d
 - access.token         c389d267bd3743b8a6d1e363981c9d12
 - access.transfer      bb6aff2da2bd43d4a6c51f5cb7973ebf
 - data.status          draft

[10:30:30] Patching plan...

[10:30:30] Processing data file: plan_patch.json

[10:30:30] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/e8dbb846f1934d0cbfa2d2cf8fa7305d?acc_token=c389d267bd3743b8a6d1e363981c9d12
[10:30:30] Response status: 200 OK

[10:30:30] Plan patched:
 - data.id              e8dbb846f1934d0cbfa2d2cf8fa7305d
 - data.status          scheduled

[10:30:30] Creating tender...

[10:30:30] Processing data file: tender_create.json

[10:30:30] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/e8dbb846f1934d0cbfa2d2cf8fa7305d/tenders
[10:30:30] Response status: 201 Created

[10:30:30] Tender created:
 - data.id              2e09be9f47e8426f84a0e01090d55f09
 - access.token         d35c5f6af3e8495786a186b8f07e8b9e
 - access.transfer      3c4b150e500c43f8af41529178f43c83
 - data.status          draft
 - data.tenderID        UA-2026-05-16-000001-a
 - data.procurementMethodType closeFrameworkAgreementUA

[10:30:30] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/2e09be9f47e8426f84a0e01090d55f09
[10:30:30] Response status: 200 OK

[10:30:30] Processing data file: tender_document_attach.json

[10:30:30] Processing data file: tender_document_file.txt

[10:30:30] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:31] Response status: 200 OK

[10:30:31] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/2e09be9f47e8426f84a0e01090d55f09/documents?acc_token=d35c5f6af3e8495786a186b8f07e8b9e
[10:30:31] Response status: 201 Created

[10:30:31] Document attached:
 - data.id              72f2937f3b9449368d928dc18b692453
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/693b89d694fb4ec3a4603da194089a7a?Signature=HmNTyfCQJ75uWUrzsyJjWB5zWr5wBiqoZfRwwlqM5B1lENK%2BaFzA6ZqhxDQX%2BVpMPmALxu2INPBqNYEcPXppBw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:31] Processing data file: contract_proforma_attach.json

[10:30:31] Processing data file: contract_proforma.txt

[10:30:31] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:31] Response status: 200 OK

[10:30:31] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/2e09be9f47e8426f84a0e01090d55f09/documents?acc_token=d35c5f6af3e8495786a186b8f07e8b9e
[10:30:31] Response status: 201 Created

[10:30:31] Document attached:
 - data.id              9bd72e1f4a7d4c72807af7ac48ca4eec
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/2fadc77c51da4e0cb699e6599e990496?Signature=0ce30ZzuZOtax7l69u8OrVHvhcKOSJwfJtBcTFscU8bT5FMca8TNyHqOHXTjM9Nnr9TL7r%2FUCaBVmi5TjIUyBw%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[10:30:31] Create tender criteria...

[10:30:31] Processing data file: criteria_create.json

[10:30:31] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/2e09be9f47e8426f84a0e01090d55f09/criteria?acc_token=d35c5f6af3e8495786a186b8f07e8b9e
[10:30:31] Response status: 201 Created

[10:30:31] Tender criteria created:
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

[10:30:31] Processing data file: tender_notice_attach.json

[10:30:31] Processing data file: tender_notice_file.p7s

[10:30:31] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:32] Response status: 200 OK

[10:30:32] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/2e09be9f47e8426f84a0e01090d55f09/documents?acc_token=d35c5f6af3e8495786a186b8f07e8b9e
[10:30:32] Response status: 201 Created

[10:30:32] Document attached:
 - data.id              44969c9aa5e247d3bbb7b07102faff69
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/64d12055b9d94622ae5cb3d515716a4f?Signature=wLZCV1RH5id%2BWel59DXcl48lPW0Ymwc9ej3pjZHDlFRyfbfrDA5L0BxVJVNlowcGAtajYFmXSuo93t8oNvotBw%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[10:30:32] Patching tender...

[10:30:32] Processing data file: tender_patch.json

[10:30:32] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/2e09be9f47e8426f84a0e01090d55f09?acc_token=d35c5f6af3e8495786a186b8f07e8b9e
[10:30:32] Response status: 200 OK

[10:30:32] Tender patched:
 - data.id              2e09be9f47e8426f84a0e01090d55f09
 - data.status          active.tendering

[10:30:32] Skipping complaints creating: bot and reviewer tokens are required

[10:30:32] Creating bids...

[10:30:32] Processing data file: bid_create_0.json

[10:30:32] Processing data file: bid_document_file.txt

[10:30:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:32] Response status: 200 OK

[10:30:32] Processing data file: bid_confidential_document_file.txt

[10:30:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:32] Response status: 200 OK

[10:30:32] Processing data file: bid_eligibility_document_file.txt

[10:30:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:32] Response status: 200 OK

[10:30:32] Processing data file: bid_financial_document_file.txt

[10:30:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:32] Response status: 200 OK

[10:30:32] Processing data file: bid_qualification_document_file.txt

[10:30:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:33] Response status: 200 OK

[10:30:33] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/2e09be9f47e8426f84a0e01090d55f09/bids
[10:30:33] Response status: 201 Created

[10:30:33] Document attached:
 - data.id              3ab39e18bec7452fb4803b2dca8b1d9f
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/668a589718664e36840177ed7df912bb?Signature=W4xGhrINtwuCw4Q%2Fe2xh420FMFeBzelSv%2Bqd7aGvZydFa4pO2nmimU3O7QN%2BKIORq1Vwk5OAdT8%2FaP6WV9I2Aw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:33] Document attached:
 - data.id              b2b31f24a3854f1baf69d1f43c56cae0
 - data.confidentiality buyerOnly

[10:30:33] Document attached:
 - data.id              7dcbb09df52a4bc1b92d8e520e8faa13
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/dc39aaba574f4fb48c32300da031df43?Signature=022Flj9vN14uxwT4zehA7aHuvC7DbkTcvvUSQQszorXPVTS9hFP1yRqE1dBct5Kxt9rAM6RLPA7E87VkK0FuBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:33] Document attached:
 - data.id              811dfb81b3ed44b2b026b87b389eef4e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/6b103d07dbea4c0d9a34fb4f9af2c22d?Signature=PKw0%2BRT6djH%2BHn0c87RFu3qnn61gwLPZOhpBErU%2B0ttyA6DFgX59gu85r%2BzJm89jIlVaErww%2BJW04oeeidIACA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:33] Document attached:
 - data.id              195a7c5b72224512be9f83c5062565b7
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/fc67d66330ef4a19862784ac147f857e?Signature=imrQP4xMhCxTyVQqff4T%2Fk02yZUYTg7kFaYW4x7G7HRxAC%2FBSDPLr2pezQF10yNmFDXZQ5SGDgKa%2FI2etVZXAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:33] Bid created:
 - data.id              eb2188697a394c46aa5658f698a57b48
 - access.token         602d318d4f2e4175888040a5f57e51d9
 - data.status          draft

[10:30:33] Processing data file: bid_create_1.json

[10:30:33] Processing data file: bid_document_file.txt

[10:30:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:33] Response status: 200 OK

[10:30:33] Processing data file: bid_confidential_document_file.txt

[10:30:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:33] Response status: 200 OK

[10:30:33] Processing data file: bid_eligibility_document_file.txt

[10:30:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:33] Response status: 200 OK

[10:30:33] Processing data file: bid_financial_document_file.txt

[10:30:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:33] Response status: 200 OK

[10:30:33] Processing data file: bid_qualification_document_file.txt

[10:30:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:33] Response status: 200 OK

[10:30:33] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/2e09be9f47e8426f84a0e01090d55f09/bids
[10:30:33] Response status: 201 Created

[10:30:33] Document attached:
 - data.id              6aee5d5d054745c4828eb4b148b54e01
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/6003c8f210bb4c748810dd0da2df96ba?Signature=NBkNm6Cq1A1SR7l6zEJ45P6EGUqjSef69gl%2FmHY1S8y61j6KHEYqxSFRPZOEw5Zlb0CCeKmHLyOrtC2Kz3cQBw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:33] Document attached:
 - data.id              e8181ee37ea248848f69bbfa1aacb3ca
 - data.confidentiality buyerOnly

[10:30:33] Document attached:
 - data.id              c5cd211a07f94c158c9b86055c53565f
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/ca26cec1a3824ae58ed67b3a05e21be2?Signature=GG9H%2FQ0S2Wt2YWN2fOnACeS7BgV5NSETCdvDZLLKZ38JoOo9Qr4XI6r4kTQ6Sfx3D0OmUADOTp4nEFxxGwDjCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:33] Document attached:
 - data.id              71ec3b626bc64448a3c9431afa671e9e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/f6589302ea024db88e006e0c793a84d1?Signature=zO2uwosVqsLado3YRmxMIt7oJZf9NFQiXbAfBNU6nNhaDD00fRshaHAM4%2BYwFqd%2BTE8uj%2BqoikUv0usnc%2BGFDw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:33] Document attached:
 - data.id              9f28c27ab79647a1ae215b7f2f482f68
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/97a0062500484c84a6c968e9c4aa5936?Signature=dPJaZNrsJcMEIfnzR8GnmTlfzoc1O21beOqTuMR%2BUQrNwx7hcrBUAdMxxPXQEb3JTJkXYnBrxYVwnlZ8ruBqAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:33] Bid created:
 - data.id              3e69a169b48d4aecb3e45d077acfd8be
 - access.token         49f49d7d0db34c7881b607a8e1659de4
 - data.status          draft

[10:30:33] Processing data file: bid_create_2.json

[10:30:33] Processing data file: bid_document_file.txt

[10:30:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:33] Response status: 200 OK

[10:30:33] Processing data file: bid_confidential_document_file.txt

[10:30:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:33] Response status: 200 OK

[10:30:33] Processing data file: bid_eligibility_document_file.txt

[10:30:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:34] Response status: 200 OK

[10:30:34] Processing data file: bid_financial_document_file.txt

[10:30:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:34] Response status: 200 OK

[10:30:34] Processing data file: bid_qualification_document_file.txt

[10:30:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:34] Response status: 200 OK

[10:30:34] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/2e09be9f47e8426f84a0e01090d55f09/bids
[10:30:34] Response status: 201 Created

[10:30:34] Document attached:
 - data.id              205c9ee3049f4006b75a7d040cc56e8a
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/bcb44a81ef75402f84eafdfb6d8bae7d?Signature=Ls3T%2FtcBsmuiXLEMUsFvRD390f1aBO1BmeyPz4EsB%2Bf06PDJdfvsxbtJJvW6Yxp69cufCRcwK%2Fkqg6EvNA8JBA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:34] Document attached:
 - data.id              bae4b4990d7e427eaabe1552083bbc4b
 - data.confidentiality buyerOnly

[10:30:34] Document attached:
 - data.id              2043daa9ac3742408e733b5443a774df
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/34ce4e80ab8e4888abd85cf58ae9f403?Signature=RqbL%2BzRWW8fOly6BF0NRC7tJNJ7IPJXAvc0q1INfFyE%2BUxjHvbqGqTQKhz%2FMRDk2DwPJ4wteVtiVLS1e%2BK0wAA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:34] Document attached:
 - data.id              a592c193d1cc470eaf7452466620c80e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/223bdd86ad6d4274a66e0acf31447b08?Signature=%2FgPuT5%2FUJNwPBMdwmpS7aD9q8fHwwGslflxxDqUuYFzU27fV07OR%2B8uGmmB1%2BF%2FJogJyd7SVzFaPvs%2B%2BcIzzDw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:34] Document attached:
 - data.id              b4787d19689f47a4883a5b47de4d83c3
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/7635960dd2294fb0afa907f3d26aa3b1?Signature=JWRK9xdw9%2BOLMJfS%2FfsuOEGfJkIsMAtdpRw09Weam%2FqP%2Bcs6HMDrmsmx4mJ8oJvI6ApNi22cr1alDLH4JZtWCg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:34] Bid created:
 - data.id              516f74e1a39d4a5eaaab24f70d8ebd35
 - access.token         c460ac7c00424b3b96d7f840b0c87125
 - data.status          draft

[10:30:34] Processing data file: bid_create_3.json

[10:30:34] Processing data file: bid_document_file.txt

[10:30:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:34] Response status: 200 OK

[10:30:34] Processing data file: bid_confidential_document_file.txt

[10:30:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:34] Response status: 200 OK

[10:30:34] Processing data file: bid_eligibility_document_file.txt

[10:30:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:34] Response status: 200 OK

[10:30:34] Processing data file: bid_financial_document_file.txt

[10:30:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:34] Response status: 200 OK

[10:30:34] Processing data file: bid_qualification_document_file.txt

[10:30:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[10:30:34] Response status: 200 OK

[10:30:34] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/2e09be9f47e8426f84a0e01090d55f09/bids
[10:30:35] Response status: 201 Created

[10:30:35] Document attached:
 - data.id              7843e91987684bec934febbb444ca94a
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/203ffc1b7a8d4fadbaadeeea3dc26e7d?Signature=Qrm0OZNm3Ram7obBHt7oNg8Vf5D4LP0mslFYhCm0qCroJkNKZZp3YgfPQSkXTOf1FVKromjjHvbXtlX70a%2FXAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:35] Document attached:
 - data.id              83f44692c5974ee38a78329d1a6553e9
 - data.confidentiality buyerOnly

[10:30:35] Document attached:
 - data.id              ce50ef3335204415af49a9ad9b13402f
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/d8cc831c86e54b96a5fd1c55dc33002e?Signature=gI7kA66gnud3pxJuRN8bhKqYIlr%2Blj1NjsAXLgj3YpDrd8WSdFn4BUlRdxmg83NLZnXPy3e3vckuNTeWC3j%2FBg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:35] Document attached:
 - data.id              66f243c9a8a34aeab308f5010fedc61c
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/03292ecf7fe2490d898c77b147881239?Signature=FMGtDzKdwrpBgkxp5kEJIHMrRuvB1bkemP%2BIwXOWhOQl4f%2FVU2TFJmCpZMwozGnm7VOzJo0IgHgK0ZZLhjXZAw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:35] Document attached:
 - data.id              bc0996012dda4a309b21beaa3ea7aab3
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/693e30a9c4614a4693157d1cb5d59385?Signature=pUWvQdTfJATCQxB6U7M1hkqxuQgwulYoMhAgHJ80kYgYNXkh7Hz%2F92JfBFAFlbxy%2FC2sRx8bMUkM%2FjCjImqwBg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[10:30:35] Bid created:
 - data.id              6fcfb1927da04bad8874804dd709b7d6
 - access.token         c8852d143fce4b2c977f67c395a1d22d
 - data.status          draft

```

## Update readme

```
export API_HOST=https://lb-api-sandbox-2.prozorro.gov.ua
export API_TOKEN=broker_api_token
export DS_HOST=https://upload-docs-sandbox-2.prozorro.gov.ua
export DS_USERNAME=broker_ds_username
export DS_PASSWORD=broker_ds_password

./README.sh
```
or
```
API_HOST=https://lb-api-sandbox-2.prozorro.gov.ua API_TOKEN=broker_api_token DS_HOST=https://upload-docs-sandbox-2.prozorro.gov.ua DS_USERNAME=broker_ds_username DS_PASSWORD=broker_ds_password ./README.sh
```

## Run tests

```
export API_HOST=https://lb-api-sandbox-2.prozorro.gov.ua
export API_TOKEN=broker_api_token
export DS_HOST=https://upload-docs-sandbox-2.prozorro.gov.ua
export DS_USERNAME=broker_ds_username
export DS_PASSWORD=broker_ds_password

pytest
```
or
```
API_HOST=https://lb-api-sandbox-2.prozorro.gov.ua API_TOKEN=broker_api_token DS_HOST=https://upload-docs-sandbox-2.prozorro.gov.ua DS_USERNAME=broker_ds_username DS_PASSWORD=broker_ds_password pytest
```
