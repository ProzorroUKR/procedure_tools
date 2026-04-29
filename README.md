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
                 [--debug]
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

  --debug               Show requests and responses
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
[17:43:39] Using seed 59072

[17:43:39] Initializing cdb client

[17:43:39] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[17:43:39] Starting new HTTPS connection (1): lb-api-sandbox-2.prozorro.gov.ua:443
[17:43:39] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/spore HTTP/11" 200 1207397
[17:43:40] Response status code: 200

[17:43:40] Client time delta with server: -1194 milliseconds

[17:43:40] Initializing ds client

[17:43:40] Creating framework...

[17:43:40] Processing data file: framework_create.json

[17:43:40] Skipping...

[17:43:40] Creating plan...

[17:43:40] Processing data file: plan_create.json

[17:43:40] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[17:43:40] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans HTTP/11" 201 4202
[17:43:40] Response status code: 201

[17:43:40] Plan created:
 - id                   6a46967be5c247ee88afbab977fef0d9
 - token                1e7617378cfa46678babcf3d8bfbbd9a
 - transfer             5535e76389ff4d3d892aa0ed6b80346f
 - status               draft

[17:43:40] Patching plan...

[17:43:40] Processing data file: plan_patch.json

[17:43:40] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/6a46967be5c247ee88afbab977fef0d9?acc_token=1e7617378cfa46678babcf3d8bfbbd9a
[17:43:40] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/plans/6a46967be5c247ee88afbab977fef0d9?acc_token=1e7617378cfa46678babcf3d8bfbbd9a HTTP/11" 200 4101
[17:43:40] Response status code: 200

[17:43:40] Plan patched:
 - id                   6a46967be5c247ee88afbab977fef0d9
 - status               scheduled

[17:43:40] Creating tender...

[17:43:40] Processing data file: tender_create.json

[17:43:40] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/6a46967be5c247ee88afbab977fef0d9/tenders
[17:43:40] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans/6a46967be5c247ee88afbab977fef0d9/tenders HTTP/11" 201 28628
[17:43:40] Response status code: 201

[17:43:40] Tender created:
 - id                   73eba4b60119438e822e81f2c7ff9b61
 - token                db02047f0840496a871cb0dcb9967992
 - transfer             4854e1ab8054406a9a117accd81570e9
 - status               draft
 - tenderID             UA-2026-04-29-000084-a
 - procurementMethodType closeFrameworkAgreementUA

[17:43:40] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/73eba4b60119438e822e81f2c7ff9b61
[17:43:40] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/tenders/73eba4b60119438e822e81f2c7ff9b61 HTTP/11" 200 28523
[17:43:40] Response status code: 200

[17:43:40] Processing data file: tender_document_attach.json

[17:43:40] Processing data file: tender_document_file.txt

[17:43:40] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:40] Starting new HTTPS connection (1): upload-docs-sandbox-2.prozorro.gov.ua:443
[17:43:41] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 576
[17:43:41] Response status code: 200

[17:43:41] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/documents?acc_token=db02047f0840496a871cb0dcb9967992
[17:43:41] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/documents?acc_token=db02047f0840496a871cb0dcb9967992 HTTP/11" 201 580
[17:43:41] Response status code: 201

[17:43:41] Document attached:
 - id                   db42340a91f148eeb8071c98581762d9
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/ce469f67dc0b4f48bed48a607b2f0e03?Signature=cDF0E7wA18J8Qr49OzSzQs%2FuZp7rc8zSCSxndNAf1qp6WvxWp600mvYM8hqBtyFTk6VMmfyqBhyPx09%2BvOc%2BBA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:41] Processing data file: contract_proforma_attach.json

[17:43:41] Processing data file: contract_proforma.txt

[17:43:41] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:41] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 573
[17:43:41] Response status code: 200

[17:43:41] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/documents?acc_token=db02047f0840496a871cb0dcb9967992
[17:43:41] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/documents?acc_token=db02047f0840496a871cb0dcb9967992 HTTP/11" 201 613
[17:43:41] Response status code: 201

[17:43:41] Document attached:
 - id                   9b28b4ff3351458fac7c19bf88c3e2f4
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/a667fc0e0f1e450d95e48fa05d2caa9f?Signature=wwMPxZH%2BcrHpm4kaVpDwCYBm2YXzPD1g97hrrIUJ8jM40sxbLgtDHaMevKy92XVt2%2FahSAmnQLhQND%2FyoCjQBQ%3D%3D&KeyID=1331dc52
 - documentType         contractProforma
 - confidentiality      public

[17:43:41] Create tender criteria...

[17:43:41] Processing data file: criteria_create.json

[17:43:41] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/criteria?acc_token=db02047f0840496a871cb0dcb9967992
[17:43:41] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/criteria?acc_token=db02047f0840496a871cb0dcb9967992 HTTP/11" 201 93928
[17:43:41] Response status code: 201

[17:43:41] Tender criteria created:
 - classification.id    CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION
 - classification.id    CRITERION.EXCLUSION.CONVICTIONS.FRAUD
 - classification.id    CRITERION.EXCLUSION.CONVICTIONS.CORRUPTION
 - classification.id    CRITERION.EXCLUSION.CONVICTIONS.CHILD_LABOUR-HUMAN_TRAFFICKING
 - classification.id    CRITERION.EXCLUSION.CONTRIBUTIONS.PAYMENT_OF_TAXES
 - classification.id    CRITERION.EXCLUSION.BUSINESS.BANKRUPTCY
 - classification.id    CRITERION.EXCLUSION.MISCONDUCT.MARKET_DISTORTION
 - classification.id    CRITERION.EXCLUSION.CONFLICT_OF_INTEREST.MISINTERPRETATION
 - classification.id    CRITERION.EXCLUSION.NATIONAL.OTHER
 - classification.id    CRITERION.OTHER.BID.LANGUAGE
 - classification.id    CRITERION.SELECTION.TECHNICAL_PROFESSIONAL_ABILITY.TECHNICAL.EQUIPMENT
 - classification.id    CRITERION.SELECTION.TECHNICAL_PROFESSIONAL_ABILITY.TECHNICAL.STAFF_FOR_CARRYING_SCOPE
 - classification.id    CRITERION.SELECTION.TECHNICAL_PROFESSIONAL_ABILITY.REFERENCES.WORKS_PERFORMANCE
 - classification.id    CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING
 - classification.id    CRITERION.EXCLUSION.CONVICTIONS.TERRORIST_OFFENCES
 - classification.id    CRITERION.EXCLUSION.CONFLICT_OF_INTEREST.EARLY_TERMINATION
 - classification.id    CRITERION.OTHER.BID.VALIDITY_PERIOD
 - classification.id    CRITERION.SELECTION.TECHNICAL_PROFESSIONAL_ABILITY.MANAGEMENT.SUBCONTRACTING_PROPORTION

[17:43:41] Processing data file: tender_notice_attach.json

[17:43:41] Processing data file: tender_notice_file.p7s

[17:43:41] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:41] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 590
[17:43:41] Response status code: 200

[17:43:41] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/documents?acc_token=db02047f0840496a871cb0dcb9967992
[17:43:41] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/documents?acc_token=db02047f0840496a871cb0dcb9967992 HTTP/11" 201 606
[17:43:41] Response status code: 201

[17:43:41] Document attached:
 - id                   e5ebf5efc8294ca8b0516f302c471b31
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/bb97993d288b489481512853c27833d0?Signature=Mc9b3002hD%2BPoeZ%2BNvdCpPxAglyTSc%2BBYKfa%2BgTHl7Wh0Gz5gAYt9WZw7e8kMnLAGs0BOkrSuhRxF3Hm3O4gCA%3D%3D&KeyID=1331dc52
 - documentType         notice
 - confidentiality      public

[17:43:41] Patching tender...

[17:43:41] Processing data file: tender_patch.json

[17:43:41] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/73eba4b60119438e822e81f2c7ff9b61?acc_token=db02047f0840496a871cb0dcb9967992
[17:43:42] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/tenders/73eba4b60119438e822e81f2c7ff9b61?acc_token=db02047f0840496a871cb0dcb9967992 HTTP/11" 200 124362
[17:43:42] Response status code: 200

[17:43:42] Tender patched:
 - id                   73eba4b60119438e822e81f2c7ff9b61
 - status               active.tendering

[17:43:42] Skipping complaints creating: bot and reviewer tokens are required

[17:43:42] Creating bids...

[17:43:42] Processing data file: bid_create_0.json

[17:43:42] Processing data file: bid_document_file.txt

[17:43:42] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:42] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 581
[17:43:42] Response status code: 200

[17:43:42] Processing data file: bid_confidential_document_file.txt

[17:43:42] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:42] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 590
[17:43:42] Response status code: 200

[17:43:42] Processing data file: bid_eligibility_document_file.txt

[17:43:42] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:42] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 607
[17:43:42] Response status code: 200

[17:43:42] Processing data file: bid_financial_document_file.txt

[17:43:42] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:42] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 605
[17:43:42] Response status code: 200

[17:43:42] Processing data file: bid_qualification_document_file.txt

[17:43:42] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:42] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 611
[17:43:42] Response status code: 200

[17:43:42] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/bids
[17:43:42] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/bids HTTP/11" 201 5129
[17:43:42] Response status code: 201

[17:43:42] Document attached:
 - id                   a0d6bb36e4254bdcac5f79446f0e4bf1
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/9f7bf80ec97b4f9fa5023895a9b72570?Signature=roaR%2BfVdwuvAvjOcuOeVmx6dBP9Ft208UCC8ulVtKBc1DchiUkuhFnFqUmCY31QPddDJ86%2Fus0z4Je3%2F%2BHCwAg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:42] Document attached:
 - id                   293e7400f50a429fb0ace9447f8a5e81
 - confidentiality      buyerOnly

[17:43:42] Document attached:
 - id                   010d993be1e646f392c73016cfbbdd3f
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/0599c694f444487f8cffbf7097e035eb?Signature=i%2BBTZtxoKwTCd36wOQPllk908mZC8LMkVVDn%2F2i6ZN5OMUt%2Bd7tlIaQVhENqfltDtXSR%2BGqEuFSd2Ib%2Fp6B8BA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:42] Document attached:
 - id                   fa7bf4847b434bd3832cf5ce5f59bd44
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/b98e99aadd0541eba5bee330098283e6?Signature=Nz99yvP8GY5X3gBiEIwGtFbTVtbkhcTqFIZncRFDmbsXzlg8Lvh8OeWNLHX8wS5bArMLVlrM31b%2BmH4KhqXaBA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:42] Document attached:
 - id                   ceb1196d3d9149948d2001703abb6dbb
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/00353f33b90144ed869540ae294a1a02?Signature=6%2ByH2EmD7z6aH2lNs%2FqY0ZyI9RyxmMxltQreVKz%2BzGXlpoWo0z0DRbHD8Rg%2F4iitiPJ4kRPTWtC4a5Gj5EJVDQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:42] Bid created:
 - id                   40817126127f48b69edc91d3014bb387
 - token                32e858e2a005405dbdf5954c908038ef
 - status               draft

[17:43:42] Processing data file: bid_create_1.json

[17:43:42] Processing data file: bid_document_file.txt

[17:43:42] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:43] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 575
[17:43:43] Response status code: 200

[17:43:43] Processing data file: bid_confidential_document_file.txt

[17:43:43] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:43] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 588
[17:43:43] Response status code: 200

[17:43:43] Processing data file: bid_eligibility_document_file.txt

[17:43:43] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:43] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 593
[17:43:43] Response status code: 200

[17:43:43] Processing data file: bid_financial_document_file.txt

[17:43:43] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:43] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 599
[17:43:43] Response status code: 200

[17:43:43] Processing data file: bid_qualification_document_file.txt

[17:43:43] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:43] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 591
[17:43:43] Response status code: 200

[17:43:43] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/bids
[17:43:43] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/bids HTTP/11" 201 5220
[17:43:43] Response status code: 201

[17:43:43] Document attached:
 - id                   c42a694cdcdd4631bbbaccfb2c2b6c62
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/94302772a4764ee79ad11e3ad4c169e3?Signature=J0dWJ1zZ3Ev%2F98mUK2pyIJ3NI2XsrwbhDpbOZAZ2tbJF85lfs9FfSThmc0XIVwE9%2B1cK6Kq7EuhchP16b8NbDQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:43] Document attached:
 - id                   95a45b8bc922442080aea1d5569776ee
 - confidentiality      buyerOnly

[17:43:43] Document attached:
 - id                   12a798e3915b4af18ce2fab5c093e835
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/822cd647ec5744eaba72c5cb7f778b3e?Signature=ILn118wwZeOpxAje8spwFoMSGktT3Bt24S%2F4BSc21X5EV5VDhpuKLA2xOlIzvmdrR7yShqgYhi%2FaNzQpfLLsDQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:43] Document attached:
 - id                   6b4178631f984013a6dbde7ceac1880c
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/d71835f9753a414896bf1d0e3b21d0d7?Signature=IWIQHPrYdiunFvPtFMjoc6OGY3jWeFcHdYA1wuHMOUqgbE6dHq0XZxRQ5DMgFZIWm5mQF9g4BeHu8%2FcQyfGpDA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:43] Document attached:
 - id                   591fc4fa0139494f9d98c234b1bb806a
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/13e96c55a62e4767975a2d997b17cd49?Signature=rftvX9SffgGBogedYnLMNSJXIRhav%2BcI1NlEoact%2FBCeRFvzKTdRis%2BMJKvOJFyVGGWoaUGs%2B1MGPksQ727ZDA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:43] Bid created:
 - id                   db9ff5a52de34458a030ae13b9971503
 - token                bf64a5bed9c04f40b86883e870e22566
 - status               draft

[17:43:43] Processing data file: bid_create_2.json

[17:43:43] Processing data file: bid_document_file.txt

[17:43:43] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:43] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 589
[17:43:43] Response status code: 200

[17:43:43] Processing data file: bid_confidential_document_file.txt

[17:43:43] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:43] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 596
[17:43:43] Response status code: 200

[17:43:43] Processing data file: bid_eligibility_document_file.txt

[17:43:43] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:44] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 599
[17:43:44] Response status code: 200

[17:43:44] Processing data file: bid_financial_document_file.txt

[17:43:44] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:44] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 597
[17:43:44] Response status code: 200

[17:43:44] Processing data file: bid_qualification_document_file.txt

[17:43:44] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:44] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 599
[17:43:44] Response status code: 200

[17:43:44] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/bids
[17:43:44] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/bids HTTP/11" 201 5228
[17:43:44] Response status code: 201

[17:43:44] Document attached:
 - id                   ee47f44941874f749a0629c1de3b0f8d
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/6627840d84ae4753afa1a35e3a5415ed?Signature=Sxw%2B1DG50tes%2BvsvxrIt%2BXTxBVIkR2YKW1ujWjXiW9V8%2FsOsdt2amNXMAwIdlrkoLjdXfH8HAI99PSs4UJeFCw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:44] Document attached:
 - id                   a0d2e2863b144d1a8ecb4c195389cbb9
 - confidentiality      buyerOnly

[17:43:44] Document attached:
 - id                   6858a699946d408bb564f31160d95237
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/be691c1def0c4964b7a738799fd5475e?Signature=BhBDLQkiaZSVhkyZKOgre%2FZUlvaoNVjcGzZoZ3tKgpKNNdf%2BfIUfnpdX5A9D0ShgOwkxaawt9w88HFxplO2uDg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:44] Document attached:
 - id                   6d6f83693fe244c394a68f72d724f5a3
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/7fc511b9277b4c14af0639ac42aae381?Signature=cfTmhw5AdDXmVlhV5mxgmJugUMOzCejvQMOhKjGl%2FF1c3GL6unKYi2zZegekMvZ3NMzp%2B%2FMOP6vGCuousn%2BMCg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:44] Document attached:
 - id                   cce24ef61d564158b2d767a552c1614d
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/34b090bb1f064396b413a64074f7d25d?Signature=ux3V8RqRCDiQfAHZCyt7shkBxrS40T4Mbuq%2ByaHBXxrtdy4QZ6v48del%2Btz3nA6JJGBP43OISm%2FOzGiNocBKAg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:44] Bid created:
 - id                   6ed028f01c8e42d4ab227bb434edce5f
 - token                0cd74c884b4446edb6e9d8d57340bd80
 - status               draft

[17:43:44] Processing data file: bid_create_3.json

[17:43:44] Processing data file: bid_document_file.txt

[17:43:44] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:44] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 589
[17:43:44] Response status code: 200

[17:43:44] Processing data file: bid_confidential_document_file.txt

[17:43:44] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:44] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 612
[17:43:44] Response status code: 200

[17:43:44] Processing data file: bid_eligibility_document_file.txt

[17:43:44] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:44] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 597
[17:43:44] Response status code: 200

[17:43:44] Processing data file: bid_financial_document_file.txt

[17:43:44] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:45] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 601
[17:43:45] Response status code: 200

[17:43:45] Processing data file: bid_qualification_document_file.txt

[17:43:45] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[17:43:45] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 601
[17:43:45] Response status code: 200

[17:43:45] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/bids
[17:43:45] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/73eba4b60119438e822e81f2c7ff9b61/bids HTTP/11" 201 5218
[17:43:45] Response status code: 201

[17:43:45] Document attached:
 - id                   83ed8e24528b4428b30edf2021d96d6a
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/b1397d3bf212489885e9f0775b5f1fb3?Signature=NI87db0pdY3eSx%2BMWf1z33fmQNm1pTLxBG8ZfI44SSUeEbpqaIKIC5DsluUNADk4R7wQ7cbawMkWJt8B1NhpAg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:45] Document attached:
 - id                   ea70c6f9eb8f407682be3a187a3c3a5d
 - confidentiality      buyerOnly

[17:43:45] Document attached:
 - id                   8d6a578b8f4744cf8d50a26bd7c8b31a
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/9511f2a834d24e75bdf4727700138246?Signature=VashF2HGzWTYGLxyID7pi3R8jOlU7aTBLxTDjHKmLA0ur4aFRp9rmoGezZPPglAxNK5J95A1mqceN5UmtEEOBw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:45] Document attached:
 - id                   18a508a235414c76b7e51d1cded25dc7
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/984bd23d8d264755835ca410de1a130c?Signature=ghwXsfMUDsj1b%2FbYZrqk1KVL2QcMY2ATeyogJSsSd50GEarsaMcUSiDn%2F8gxo0%2BkBmeLAPZd1%2BCO%2Fk2diiDfDA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:45] Document attached:
 - id                   17780116e03b47a3bf08f693a33dfb70
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/a7d3529b0392494b98195956c377d367?Signature=rAk4huvVW2MB4%2FdidoMxXXK7BLpbm8rbPxrZ5PZB9rP9MHUlcQtPfgOBWDmhA6LFPjGAWx4eOpDhUcXT%2Bf3vDA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[17:43:45] Bid created:
 - id                   a9853c62e6524b6590162717f7caef7c
 - token                2571c41ef9194607885235d0f0bdd51c
 - status               draft

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
