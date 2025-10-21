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
                         - dynamicPurchasingSystem.competitiveOrdering.long
                         - dynamicPurchasingSystem.competitiveOrdering.short
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
[15:56:45] Using seed 851202

[15:56:45] Initializing cdb client

[15:56:45] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[15:56:45] Starting new HTTPS connection (1): lb-api-sandbox-2.prozorro.gov.ua:443
[15:56:45] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/spore HTTP/11" 200 1128850
[15:56:46] Response status code: 200

[15:56:46] Client time delta with server: -1043 milliseconds

[15:56:46] Initializing ds client

[15:56:46] Creating framework...

[15:56:46] Processing data file: framework_create.json

[15:56:46] Skipping...

[15:56:46] Creating plan...

[15:56:46] Processing data file: plan_create.json

[15:56:46] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[15:56:46] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans HTTP/11" 201 4202
[15:56:46] Response status code: 201

[15:56:46] Plan created:
 - id                   04808c18a8f040c58e00a240dbe8e49f
 - token                045b2e915f2d4a62bf5316c1597a8aa9
 - transfer             836a9b13a95e4a588c1f3449762bf470
 - status               draft

[15:56:46] Patching plan...

[15:56:46] Processing data file: plan_patch.json

[15:56:46] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/04808c18a8f040c58e00a240dbe8e49f?acc_token=045b2e915f2d4a62bf5316c1597a8aa9
[15:56:46] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/plans/04808c18a8f040c58e00a240dbe8e49f?acc_token=045b2e915f2d4a62bf5316c1597a8aa9 HTTP/11" 200 4101
[15:56:46] Response status code: 200

[15:56:46] Plan patched:
 - id                   04808c18a8f040c58e00a240dbe8e49f
 - status               scheduled

[15:56:46] Creating tender...

[15:56:46] Processing data file: tender_create.json

[15:56:46] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/04808c18a8f040c58e00a240dbe8e49f/tenders
[15:56:46] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans/04808c18a8f040c58e00a240dbe8e49f/tenders HTTP/11" 201 7452
[15:56:46] Response status code: 201

[15:56:46] Tender created:
 - id                   f90fbdd8301c4d71a1e68776da4f9d49
 - token                7cbd1fa08ad44a9db4c6aeddf2d95581
 - transfer             0cfa5d7496c7439e8877bfa82d61f182
 - status               draft
 - tenderID             UA-2025-10-21-000140-a
 - procurementMethodType closeFrameworkAgreementUA

[15:56:46] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49
[15:56:46] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49 HTTP/11" 200 7347
[15:56:46] Response status code: 200

[15:56:46] Processing data file: tender_document_attach.json

[15:56:46] Processing data file: tender_document_file.txt

[15:56:46] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:46] Starting new HTTPS connection (1): upload-docs-sandbox-2.prozorro.gov.ua:443
[15:56:47] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 588
[15:56:47] Response status code: 200

[15:56:47] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/documents?acc_token=7cbd1fa08ad44a9db4c6aeddf2d95581
[15:56:47] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/documents?acc_token=7cbd1fa08ad44a9db4c6aeddf2d95581 HTTP/11" 201 576
[15:56:47] Response status code: 201

[15:56:47] Document attached:
 - id                   6bf38ba48c374766a8c7e8b033b6b1c1
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/52676ae92cd946f5b926701e0df6d78f?Signature=wB43Ty8irNEB86jEn5eUjsv%2BDudkS3kbfL05eVk4hKM4vWXFAqDJ6Ca0x2YMiVVDmpjz4shvV5hR4Xg7rFV2DA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:47] Create tender criteria...

[15:56:47] Processing data file: criteria_create.json

[15:56:47] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/criteria?acc_token=7cbd1fa08ad44a9db4c6aeddf2d95581
[15:56:47] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/criteria?acc_token=7cbd1fa08ad44a9db4c6aeddf2d95581 HTTP/11" 201 93928
[15:56:47] Response status code: 201

[15:56:47] Tender criteria created:
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

[15:56:47] Processing data file: tender_notice_attach.json

[15:56:47] Processing data file: tender_notice_file.p7s

[15:56:47] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:48] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 576
[15:56:48] Response status code: 200

[15:56:48] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/documents?acc_token=7cbd1fa08ad44a9db4c6aeddf2d95581
[15:56:48] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/documents?acc_token=7cbd1fa08ad44a9db4c6aeddf2d95581 HTTP/11" 201 602
[15:56:48] Response status code: 201

[15:56:48] Document attached:
 - id                   e506661326aa4d6ab7a45c3774064e2f
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/738ade9cf097420bab22c98f17e723fe?Signature=B1SCuxqcExfA8Tg2XE6nRd%2Foq3iRTmh50wEE8dlLkNy2CByDpBQPhseZ1bbieah1Uth8KLztkzhS0y0uxP%2BVDw%3D%3D&KeyID=1331dc52
 - documentType         notice
 - confidentiality      public

[15:56:48] Patching tender...

[15:56:48] Processing data file: tender_patch.json

[15:56:48] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49?acc_token=7cbd1fa08ad44a9db4c6aeddf2d95581
[15:56:49] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49?acc_token=7cbd1fa08ad44a9db4c6aeddf2d95581 HTTP/11" 200 102573
[15:56:49] Response status code: 200

[15:56:49] Tender patched:
 - id                   f90fbdd8301c4d71a1e68776da4f9d49
 - status               active.tendering

[15:56:49] Skipping complaints creating: bot and reviewer tokens are required

[15:56:49] Creating bids...

[15:56:49] Processing data file: bid_create_0.json

[15:56:49] Processing data file: bid_document_file.txt

[15:56:49] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:49] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 575
[15:56:49] Response status code: 200

[15:56:49] Processing data file: bid_confidential_document_file.txt

[15:56:49] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:50] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 602
[15:56:50] Response status code: 200

[15:56:50] Processing data file: bid_eligibility_document_file.txt

[15:56:50] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:50] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 597
[15:56:50] Response status code: 200

[15:56:50] Processing data file: bid_financial_document_file.txt

[15:56:50] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:51] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 591
[15:56:51] Response status code: 200

[15:56:51] Processing data file: bid_qualification_document_file.txt

[15:56:51] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:51] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 593
[15:56:51] Response status code: 200

[15:56:51] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/bids
[15:56:51] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/bids HTTP/11" 201 5123
[15:56:52] Response status code: 201

[15:56:52] Document attached:
 - id                   8912d71f04544a55a6274c61a0cdf18f
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/06716c317902400287ae1c679a8d06eb?Signature=8bwPKXP5nP9YRVz4HcGLbdj6ayGaXuG%2BFND%2BBlPxPGqB4gPuvy24YJHhEUr4FIKjZ1etAcjlgranzSdsLA4fDg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:52] Document attached:
 - id                   e77615be136043b08d8a15200a1c7eb8
 - confidentiality      buyerOnly

[15:56:52] Document attached:
 - id                   d858f5f5af6541449d0dfc88e4f21fab
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/c0b64182aa21414e8a83fd23593281cb?Signature=YoaMHG76oxsQMuzbvytplpGQz97%2BUNWvvpn%2FqynpRWnbdxKAEcSyxfjvzVnSz7WwEt2dQ46gM0Y6rCfo2RmFBw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:52] Document attached:
 - id                   8715de2f60ed43b59bbceb14a094840b
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/59aeaa99ae92472c91f9561dba99260d?Signature=bUqTUPYDSJdZ5pLK74AIoreTkbIqxumqEqV7hfnyZ37vk6nW8pix0zM1NlKv4J5IHY65r%2BsgWoSLqvbzjY4eAg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:52] Document attached:
 - id                   f496e12425ce486bb6aace941bc15689
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/1d7933f4fca24d9691ec822efcde11c0?Signature=2%2Bsr%2BpisCrcgtzeKG%2FPHxSFbIXssnyPRyCDdaPCKXLKadAGU%2F1BghpQO0iVBfZUUlqJF9%2BuV98gL%2F1vIhiOwCg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:52] Bid created:
 - id                   5be0627ab64f435b83042e276eb02bed
 - token                3d51008d291e40a99ce771f7b44029dd
 - status               draft

[15:56:52] Processing data file: bid_create_1.json

[15:56:52] Processing data file: bid_document_file.txt

[15:56:52] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:53] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 579
[15:56:53] Response status code: 200

[15:56:53] Processing data file: bid_confidential_document_file.txt

[15:56:53] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:53] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 600
[15:56:53] Response status code: 200

[15:56:53] Processing data file: bid_eligibility_document_file.txt

[15:56:53] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:53] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 597
[15:56:53] Response status code: 200

[15:56:53] Processing data file: bid_financial_document_file.txt

[15:56:53] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:53] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 593
[15:56:53] Response status code: 200

[15:56:53] Processing data file: bid_qualification_document_file.txt

[15:56:53] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:54] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 597
[15:56:54] Response status code: 200

[15:56:54] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/bids
[15:56:54] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/bids HTTP/11" 201 5220
[15:56:54] Response status code: 201

[15:56:54] Document attached:
 - id                   a3fe7954ea794426906402e7c498a29e
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/d8319b6ce46842a09108c2d4f0ddbeee?Signature=N4qRoiRIsBAfcAb42%2FYYMMIcbmMKqYjh3FlnhTkJxFnhimc8PVpLpp6oXkUGe%2Fl5byfA4O2pX3Zrk4nyKPoQCQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:54] Document attached:
 - id                   7306c9db09de42e19e28b73287ac1401
 - confidentiality      buyerOnly

[15:56:54] Document attached:
 - id                   35005542d2424e44b2b8defdbb1d9269
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/742eff76833340f0b17de7f2d0046769?Signature=%2BwDVpm0y9QtqRpepHwtKfNnajnn6EwtzTpgRgQgSaCHk5n66wWaX%2BOho6aUz%2BcWcjoB5aX4BaUd547yGdR3PAw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:54] Document attached:
 - id                   67adf3406e934d15ba7afeb46b7722bb
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/edb59109100b467fab00aec910f35f29?Signature=owViwCzpbL6ktNlIeBvrlKRagWaN2yckxT8QW1ES%2FTWw0lwDAge1sj4xc%2FD7%2FLim9xRWQjBUBNV2Ifwbe341Bg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:54] Document attached:
 - id                   239b966112cd4b9dbb15245f89754b66
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/92e6aa36879f411f95113faae1744e6b?Signature=nKFzhU7UHprfSwrbEQodaefqAAz9tT5D5uUkQ6PjDgD5p%2FElbQJYDUEYYCeHkgzid3JYUt2jD1uKWOik2w5zAw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:54] Bid created:
 - id                   9a1c435007be438f9ae0849355c7272f
 - token                7422b3c04bd94879b620d906be0c2822
 - status               draft

[15:56:54] Processing data file: bid_create_2.json

[15:56:54] Processing data file: bid_document_file.txt

[15:56:54] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:55] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 589
[15:56:55] Response status code: 200

[15:56:55] Processing data file: bid_confidential_document_file.txt

[15:56:55] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:55] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 594
[15:56:55] Response status code: 200

[15:56:55] Processing data file: bid_eligibility_document_file.txt

[15:56:55] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:55] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 607
[15:56:55] Response status code: 200

[15:56:55] Processing data file: bid_financial_document_file.txt

[15:56:55] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:56] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 587
[15:56:56] Response status code: 200

[15:56:56] Processing data file: bid_qualification_document_file.txt

[15:56:56] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:56] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 601
[15:56:56] Response status code: 200

[15:56:56] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/bids
[15:56:56] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/bids HTTP/11" 201 5220
[15:56:56] Response status code: 201

[15:56:56] Document attached:
 - id                   98f159647dc643e481a099ac0fd1dd70
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/0b50f0d1fbe34a268885fc712aba7f14?Signature=VZx2hKhkezImUpxfr9DFgreDus2QM%2FrsOqDRu3CLiUJhYPA4GFnEglYfeJfN1zB%2B5RwQgClyKHk9orggDwG1CA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:56] Document attached:
 - id                   e57c870eee3c406d98f82728bd8efe2f
 - confidentiality      buyerOnly

[15:56:56] Document attached:
 - id                   e199eb5aaba44369951099db9656403b
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/3670d9e1174c4c8690aa7e672f1eeea8?Signature=EriZVi0TdNoz27GT%2FznCBcBwZv%2BQYeVs6wGhrn%2BPO0viCDIOjEuuahTWHUv0fq388GArrnSHLOTW5qvv0XkvBw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:56] Document attached:
 - id                   adebaea6894c46bfbc384906d48929eb
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/4b304887d0e144bba1519268708a3136?Signature=8g5JWxprQka6KrCFFsyPCHOOfo%2BKwSR%2BtOcuBw33YBkJB5L8kkU12rA3NDc%2Fsh%2B9Ytrfi0c789ucwEdYQsgOBw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:56] Document attached:
 - id                   8b23cc28401b4dd9b18f18f0853c3036
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/1f81e8df470543e8b59d9a9bac3053eb?Signature=G4heNMXpI4EzWVS45nsPCqRavP1l5q3snThEqqcezpGim9HTFbZ2rccVTDfnXyfVAPJejspvMw1Spzx5pHjiDA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:56] Bid created:
 - id                   e06123d7ac864f52b8c965c42857f1f8
 - token                4b42fb7490ae44d2b1f9f2b08163ecd8
 - status               draft

[15:56:56] Processing data file: bid_create_3.json

[15:56:56] Processing data file: bid_document_file.txt

[15:56:56] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:56] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 597
[15:56:56] Response status code: 200

[15:56:56] Processing data file: bid_confidential_document_file.txt

[15:56:56] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:57] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 604
[15:56:57] Response status code: 200

[15:56:57] Processing data file: bid_eligibility_document_file.txt

[15:56:57] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:57] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 599
[15:56:57] Response status code: 200

[15:56:57] Processing data file: bid_financial_document_file.txt

[15:56:57] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:59] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 603
[15:56:59] Response status code: 200

[15:56:59] Processing data file: bid_qualification_document_file.txt

[15:56:59] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[15:56:59] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 593
[15:56:59] Response status code: 200

[15:56:59] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/bids
[15:56:59] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/f90fbdd8301c4d71a1e68776da4f9d49/bids HTTP/11" 201 5222
[15:56:59] Response status code: 201

[15:56:59] Document attached:
 - id                   56485534a1f34703a72178ae17dfa87c
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/0c096bb488214ac6b14faaa02e885616?Signature=NIYy%2FJuaSFFOOC6KrByIc0UYXvc4xsk90P0NWVJPrWr2NdWj4CCfN4jJ9xaPdCmEaYZKfLT8xQ6Z6gFNOFraAg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:59] Document attached:
 - id                   e56c2f3cc6114cf19cc0fb470bdf4700
 - confidentiality      buyerOnly

[15:56:59] Document attached:
 - id                   2fad1621ff634574a641a8a54ef5f9b1
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/9ddd67deb6cb45079b44c3b6a0486995?Signature=FRciGdY5gAChOYYAG0wmx7JX%2B%2BKjIBwpoyRPcHqCnhiZtXZJB4sHg92dsl5GUGTcNVUNQPRtaOze015zHdK1Bw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:59] Document attached:
 - id                   34dac537ccc6400d935de8b9a1ce1586
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/a9b519ea3c52476ab8e9b08b6f3b2acf?Signature=pN0qQS6glo%2FMuiLNiHLftdVmkR9KmCSurPiGqRT3fPnh72A0qecIO8Q8TzDl%2F5MRS3XT2%2BJaOGvAE78CQ%2FqOAA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:59] Document attached:
 - id                   540d182a4d6e4e9e9fd506ba23a87a61
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/154c45b916ce449fbf33f87cdf1fd7cc?Signature=OqYlyFrMU9pXYHBepyckCB1RLEHRdZj6kOyKQq0OJfgt79IOc8S%2F3CkG%2FwN0m2vq%2FxIz1cWjuMvZroUOQxbVCw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[15:56:59] Bid created:
 - id                   4003c55265f849668de88e27f64ee9a9
 - token                1f5cd3380a564c6c9869b0f1caaf5701
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
