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
                 [-w edr-qualification] [-e SEED]
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
                         - aboveThreshold.features
                         - aboveThreshold.lcc
                         - aboveThresholdEU
                         - aboveThresholdEU.features
                         - aboveThresholdEU.lcc
                         - aboveThresholdUA
                         - aboveThresholdUA.features
                         - aboveThresholdUA.lcc
                         - belowThreshold
                         - belowThreshold.central
                         - belowThreshold.features
                         - closeFrameworkAgreementUA
                         - closeFrameworkAgreementUA.central
                         - competitiveDialogueEU
                         - competitiveDialogueUA
                         - competitiveDialogueUA.features
                         - dynamicPurchasingSystem.competitiveOrdering
                         - dynamicPurchasingSystem.priceQuotation
                         - dynamicPurchasingSystem.priceQuotation.nolot
                         - esco
                         - esco.features
                         - internationalFinancialInstitutions.requestForProposal
                         - negotiation
                         - negotiation.quick
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
[11:56:28] Using seed 694234

[11:56:28] Initializing cdb client

[11:56:28] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[11:56:28] Starting new HTTPS connection (1): lb-api-sandbox-2.prozorro.gov.ua:443
[11:56:28] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/spore HTTP/11" 200 1086991
[11:56:28] Response status code: 200

[11:56:28] Client time delta with server: -505 milliseconds

[11:56:28] Initializing ds client

[11:56:28] Creating framework...

[11:56:28] Processing data file: framework_create.json

[11:56:28] Skipping...

[11:56:28] Creating plan...

[11:56:28] Processing data file: plan_create.json

[11:56:28] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[11:56:28] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans HTTP/11" 201 4202
[11:56:28] Response status code: 201

[11:56:28] Plan created:
 - id                   73a0d8132bff4cd0aa072a20ebb06fd5
 - token                d21e62f325f043d7bfd4a0b6193b416f
 - transfer             e0baa5b1440349e79658637be0170f3e
 - status               draft

[11:56:28] Patching plan...

[11:56:28] Processing data file: plan_patch.json

[11:56:28] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/73a0d8132bff4cd0aa072a20ebb06fd5?acc_token=d21e62f325f043d7bfd4a0b6193b416f
[11:56:28] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/plans/73a0d8132bff4cd0aa072a20ebb06fd5?acc_token=d21e62f325f043d7bfd4a0b6193b416f HTTP/11" 200 4101
[11:56:28] Response status code: 200

[11:56:28] Plan patched:
 - id                   73a0d8132bff4cd0aa072a20ebb06fd5
 - status               scheduled

[11:56:28] Creating tender...

[11:56:28] Processing data file: tender_create.json

[11:56:28] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/73a0d8132bff4cd0aa072a20ebb06fd5/tenders
[11:56:28] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans/73a0d8132bff4cd0aa072a20ebb06fd5/tenders HTTP/11" 201 7426
[11:56:28] Response status code: 201

[11:56:28] Tender created:
 - id                   6d481da08ad14baf857d9f57653b368b
 - token                ae4dc3c605c947ac82e5aea3e35628aa
 - transfer             ed7ccf0901ac4fefae3df872ddeec5c6
 - status               draft
 - tenderID             UA-2025-03-26-000004-a
 - procurementMethodType closeFrameworkAgreementUA

[11:56:28] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/6d481da08ad14baf857d9f57653b368b
[11:56:28] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/tenders/6d481da08ad14baf857d9f57653b368b HTTP/11" 200 7321
[11:56:28] Response status code: 200

[11:56:28] Processing data file: tender_document_attach.json

[11:56:28] Processing data file: tender_document_file.txt

[11:56:28] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:28] Starting new HTTPS connection (1): upload-docs-sandbox-2.prozorro.gov.ua:443
[11:56:29] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 576
[11:56:29] Response status code: 200

[11:56:29] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/6d481da08ad14baf857d9f57653b368b/documents?acc_token=ae4dc3c605c947ac82e5aea3e35628aa
[11:56:29] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/6d481da08ad14baf857d9f57653b368b/documents?acc_token=ae4dc3c605c947ac82e5aea3e35628aa HTTP/11" 201 580
[11:56:29] Response status code: 201

[11:56:29] Document attached:
 - id                   513b792a730944aca671cd7f864d0947
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/982c481aa49a4fc29a01095f2dc46581?Signature=t8gW3%2BB7x1bVsDrJavxgk4OLz%2ByTmbTQ5YBwitcA7A8ZcCicbtkeiHXyboIj%2BkmTHdhK7dRlLIZeNmxS1FicCQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:29] Create tender criteria...

[11:56:29] Processing data file: criteria_create.json

[11:56:29] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/6d481da08ad14baf857d9f57653b368b/criteria?acc_token=ae4dc3c605c947ac82e5aea3e35628aa
[11:56:29] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/6d481da08ad14baf857d9f57653b368b/criteria?acc_token=ae4dc3c605c947ac82e5aea3e35628aa HTTP/11" 201 86348
[11:56:29] Response status code: 201

[11:56:29] Tender criteria created:
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

[11:56:29] Processing data file: tender_notice_attach.json

[11:56:29] Processing data file: tender_notice_file.p7s

[11:56:29] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:29] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 592
[11:56:29] Response status code: 200

[11:56:29] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/6d481da08ad14baf857d9f57653b368b/documents?acc_token=ae4dc3c605c947ac82e5aea3e35628aa
[11:56:29] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/6d481da08ad14baf857d9f57653b368b/documents?acc_token=ae4dc3c605c947ac82e5aea3e35628aa HTTP/11" 201 610
[11:56:29] Response status code: 201

[11:56:29] Document attached:
 - id                   ee98ddfb2d054a48837ab79ee74df631
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/044bed06dcf94297a77d822af4ce7ff3?Signature=OPmyPhtOIT7T6I%2FZUoPl338oODAkHgURF8rA%2BA54YESrTP%2Fhh80kV4ERJ8mRJ5KW%2F%2Ff9%2BchzWfvazU8UOHuYAg%3D%3D&KeyID=1331dc52
 - documentType         notice
 - confidentiality      public

[11:56:29] Patching tender...

[11:56:29] Processing data file: tender_patch.json

[11:56:29] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/6d481da08ad14baf857d9f57653b368b?acc_token=ae4dc3c605c947ac82e5aea3e35628aa
[11:56:29] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/tenders/6d481da08ad14baf857d9f57653b368b?acc_token=ae4dc3c605c947ac82e5aea3e35628aa HTTP/11" 200 94979
[11:56:29] Response status code: 200

[11:56:29] Tender patched:
 - id                   6d481da08ad14baf857d9f57653b368b
 - status               active.tendering

[11:56:29] Skipping complaints creating: bot and reviewer tokens are required

[11:56:29] Creating bids...

[11:56:29] Processing data file: bid_create_0.json

[11:56:29] Processing data file: bid_document_file.txt

[11:56:29] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:30] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 589
[11:56:30] Response status code: 200

[11:56:30] Processing data file: bid_confidential_document_file.txt

[11:56:30] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:30] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 608
[11:56:30] Response status code: 200

[11:56:30] Processing data file: bid_eligibility_document_file.txt

[11:56:30] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:30] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 593
[11:56:30] Response status code: 200

[11:56:30] Processing data file: bid_financial_document_file.txt

[11:56:30] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:30] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 587
[11:56:30] Response status code: 200

[11:56:30] Processing data file: bid_qualification_document_file.txt

[11:56:30] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:30] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 597
[11:56:30] Response status code: 200

[11:56:30] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/6d481da08ad14baf857d9f57653b368b/bids
[11:56:30] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/6d481da08ad14baf857d9f57653b368b/bids HTTP/11" 201 5119
[11:56:30] Response status code: 201

[11:56:30] Document attached:
 - id                   2c327f50f1cc4efba13d16de84cbe407
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/c74a853b8d3b4a1b80f2b074175fb8b6?Signature=VbPKpogX%2FEanPKk0V0ieL4FkeZKHgvdGr5317lX765Iw0uuGPNtOjip6SWROvoX5YMSHaI1nnDCabWbA4MyNAA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:30] Document attached:
 - id                   8b1d06e65c4a4511bd41aa33161e212e
 - confidentiality      buyerOnly

[11:56:30] Document attached:
 - id                   dfaeaa9341ab492da8e14f9ca9a12970
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/d15d7a4972474e0e94a6eb6ba4746c43?Signature=8L8Zo1JxmPMGgj9nN303nYIJVs2lroetmLFz80aMj%2BjIusqrEO6NGww9Uyj1m%2BsK%2BOcBmLxwXarJBX81Jsl0Bw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:30] Document attached:
 - id                   bdd305f247b242adb7f8ec78c8c31d86
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/05468b252d184073aea3644157e82dba?Signature=v1PA3%2FrWkzTaXIZbH82%2BjLC%2F4gJZvbZPggj%2FnqSuxHxAywZch16dpoY9xqj2ZswLm4fAjxlLdKNNmlpp7ybDBQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:30] Document attached:
 - id                   e395638196364b4388f8144717687190
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/b7556be960454e48bf062a3f34719ea9?Signature=oIjHD1HCiaP2Or8HBlKOTtO7BKXzWWcQa0bECNBT9OJYnvEBcJp0RCEX2gVI2pptX4br1plxaUCGhgK%2FDMn3Bg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:30] Bid created:
 - id                   8e49f560544040bbb5f41fc5b10b79e7
 - token                8c0d0e57b4a04eb5b9a03224b8695b2b
 - status               draft

[11:56:30] Processing data file: bid_create_1.json

[11:56:30] Processing data file: bid_document_file.txt

[11:56:30] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:30] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 599
[11:56:30] Response status code: 200

[11:56:30] Processing data file: bid_confidential_document_file.txt

[11:56:30] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:31] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 594
[11:56:31] Response status code: 200

[11:56:31] Processing data file: bid_eligibility_document_file.txt

[11:56:31] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:31] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 595
[11:56:31] Response status code: 200

[11:56:31] Processing data file: bid_financial_document_file.txt

[11:56:31] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:31] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 601
[11:56:31] Response status code: 200

[11:56:31] Processing data file: bid_qualification_document_file.txt

[11:56:31] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:31] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 611
[11:56:31] Response status code: 200

[11:56:31] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/6d481da08ad14baf857d9f57653b368b/bids
[11:56:31] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/6d481da08ad14baf857d9f57653b368b/bids HTTP/11" 201 5228
[11:56:31] Response status code: 201

[11:56:31] Document attached:
 - id                   9acf4849d9804a8fb70045f976025155
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/1bcabbacd62a498789d978f627b0d1b5?Signature=NjhuprWQUGRAGAyyAMQKUDi4eTCeUxz%2Fj7GIBk6%2B3egtaaKmCbjZt0mScH94O5QCH6C3cswjkrwVlcx%2BDIFJBg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:31] Document attached:
 - id                   580256bc5ad4471e9d120d79e9518fb5
 - confidentiality      buyerOnly

[11:56:31] Document attached:
 - id                   43a40076ef804536a0071aa9d57b440e
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/df0f9283ca844e509667bc6dd612a99f?Signature=upETrF5AZQGkyQi8vQGu%2FqFv8UIyOimzYBtr3dK9UR6%2FH4nL329N6X6Swn8kAaHKkc24WV7T%2BD%2BvjNvKZb%2BKAA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:31] Document attached:
 - id                   45c76fec610e402ab349bd34f89682ee
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/8964a641d6584eb99cbcaca94cf8fcae?Signature=HEQPIvQ25HMP0oCjPIhcSQ20EvK7ulPVXMkks3J2XuU%2BMVpsZqe0SVMTrrlftdBbYusMn%2FNANNjgIb6NZ2nSCg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:31] Document attached:
 - id                   e78687990d6c4b8b987184ced990aec3
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/9eed7e4e6a8d46b3b545b5cca9b4d5c3?Signature=LdtZc%2FIfSfS7Os9q2SZEogWcW8jm1Rz9RLOgqSqpUkyjdqSEcEnhvIx6%2Ff%2FvaI7b3DkbX5Jst7Ecc4RIBfZzAw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:31] Bid created:
 - id                   de9a9a9dd77c421da7bcc48f74729274
 - token                59377e75ec80452a9c8657c3f08abe86
 - status               draft

[11:56:31] Processing data file: bid_create_2.json

[11:56:31] Processing data file: bid_document_file.txt

[11:56:31] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:31] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 577
[11:56:31] Response status code: 200

[11:56:31] Processing data file: bid_confidential_document_file.txt

[11:56:31] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:31] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 600
[11:56:31] Response status code: 200

[11:56:31] Processing data file: bid_eligibility_document_file.txt

[11:56:31] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:31] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 595
[11:56:31] Response status code: 200

[11:56:31] Processing data file: bid_financial_document_file.txt

[11:56:31] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:32] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 587
[11:56:32] Response status code: 200

[11:56:32] Processing data file: bid_qualification_document_file.txt

[11:56:32] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:32] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 599
[11:56:32] Response status code: 200

[11:56:32] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/6d481da08ad14baf857d9f57653b368b/bids
[11:56:32] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/6d481da08ad14baf857d9f57653b368b/bids HTTP/11" 201 5224
[11:56:32] Response status code: 201

[11:56:32] Document attached:
 - id                   cfb09f152dd0472db4695016e36525cc
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/e81c36f4914845879fa6615ff70ea059?Signature=RoqEdsOwyignpN8eY%2FzFaNSKHwfWwk0zTa0zjh%2FiVCpvcL%2BuKnN%2FWpbbEY27L0gPH5BVngIiYENwBtCgUdhLAQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:32] Document attached:
 - id                   b7da9adff6674d85be62f97c944cde6b
 - confidentiality      buyerOnly

[11:56:32] Document attached:
 - id                   adbea4cc95644db991f8232c03f3c2fd
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/d4850871d4884a088d95fafb141ed492?Signature=dMWm2sHZdV4hUwwpfStnW2VwrWpRn9teowFUgTRCZiyezoz2nNipXzR9RuBfGhHKvYJYl2pSeFitpfSR2tXaBw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:32] Document attached:
 - id                   5313a6edc8f446acbbac278dd44268ba
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/b9d4d20985a245ca8a3213514520aa2f?Signature=wUvfNSbaA1svfRnUtj%2B8nr6re3%2BTpTmx99hCTDnRmgIvmFjSUF7x0J1cjY0xBOnSWU7QsLI%2F8YmD2xgvzJuHDg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:32] Document attached:
 - id                   15adb71d40804e698ca032e2b48aca1f
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/169cabc2bd4948229651caafc0c4ba81?Signature=%2BPIm%2FvubEiF0VmjwayQR5ATTSEusjFxHsWr2y8qzpnGXenJ6%2Bl4JUCzUjE4KPn4X0NTpjoCdRB6XY70ZHdf%2FBg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:32] Bid created:
 - id                   fb1a27311c084c2cb953fc34d39f49ca
 - token                af13f080b3a34b56b036fb889337aa52
 - status               draft

[11:56:32] Processing data file: bid_create_3.json

[11:56:32] Processing data file: bid_document_file.txt

[11:56:32] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:32] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 577
[11:56:32] Response status code: 200

[11:56:32] Processing data file: bid_confidential_document_file.txt

[11:56:32] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:32] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 588
[11:56:32] Response status code: 200

[11:56:32] Processing data file: bid_eligibility_document_file.txt

[11:56:32] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:32] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 589
[11:56:32] Response status code: 200

[11:56:32] Processing data file: bid_financial_document_file.txt

[11:56:32] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:32] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 613
[11:56:32] Response status code: 200

[11:56:32] Processing data file: bid_qualification_document_file.txt

[11:56:32] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[11:56:33] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 607
[11:56:33] Response status code: 200

[11:56:33] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/6d481da08ad14baf857d9f57653b368b/bids
[11:56:33] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/6d481da08ad14baf857d9f57653b368b/bids HTTP/11" 201 5216
[11:56:33] Response status code: 201

[11:56:33] Document attached:
 - id                   3552f0c0a7804601962c27a97d7377e2
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/21e497f1680e41f7ae40e824db1ff68d?Signature=zgq8RlV%2FBwPeIptNPSX6hhAUV3CHDnhlsAgddXt0gtgCj1KJqCtNmWbS0LtNIrOkdx%2FmLteGYKxO2Vnl11LxDg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:33] Document attached:
 - id                   b221da0492a24d9f83c2e49f6bc13d73
 - confidentiality      buyerOnly

[11:56:33] Document attached:
 - id                   855e6f9edf1540a0b01354acda758056
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/3b12f961e3e8458788d2ef18fc93e2bc?Signature=isuuntLYQSxUk76x2%2Bh3GFHBQ8X%2FmD8e9Z%2Fc9FiCi%2BvZUwqlQFpMCgfHGfipf9z3djIeEZj9HFBbgjZkZ5jxAg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:33] Document attached:
 - id                   7bbf117c6666407ebeeaf79a249aa17b
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/915a0c6e2c334996ac149c0940b78069?Signature=WVohnMzGklct5RAmB3Ya4jvKiYt0lsaWzNFnBseOmCgVaEaEen37Fw2X7h5yDrdvfpuqDTIyEEXCOTgn44cCDQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:33] Document attached:
 - id                   68f9bfde37474540a60bd77818229a4f
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/b2ffb779319944b6abe1671f8431c854?Signature=XpweZryFPUXjfayqckVRHoP5ZBarFJSJEqBqT7dN7TYY%2B1UH1GBIIIiwIB7Pkmw8ZsG4jfGpb98uTA25ShSlAA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[11:56:33] Bid created:
 - id                   ddec2b0283d0470da0d7d834861b87dd
 - token                215725bc78d44a13bff58cfb4b7aeeac
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

python setup.py test
```
or
```
API_HOST=https://lb-api-sandbox-2.prozorro.gov.ua API_TOKEN=broker_api_token DS_HOST=https://upload-docs-sandbox-2.prozorro.gov.ua DS_USERNAME=broker_ds_username DS_PASSWORD=broker_ds_password python setup.py test
```
