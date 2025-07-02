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
[13:10:10] Using seed 787006

[13:10:10] Initializing cdb client

[13:10:10] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[13:10:10] Starting new HTTPS connection (1): lb-api-sandbox-2.prozorro.gov.ua:443
[13:10:11] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/spore HTTP/11" 200 1219580
[13:10:11] Response status code: 200

[13:10:11] Client time delta with server: -204 milliseconds

[13:10:11] Initializing ds client

[13:10:11] Creating framework...

[13:10:11] Processing data file: framework_create.json

[13:10:11] Skipping...

[13:10:11] Creating plan...

[13:10:11] Processing data file: plan_create.json

[13:10:11] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[13:10:11] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans HTTP/11" 201 4202
[13:10:11] Response status code: 201

[13:10:11] Plan created:
 - id                   7ba43b50cb5c43d3af5a7d2719211047
 - token                c93ffa60b5aa4300b8f3f9051450aea2
 - transfer             734a5df2f5f14d30ab2ccc34119eef63
 - status               draft

[13:10:11] Patching plan...

[13:10:11] Processing data file: plan_patch.json

[13:10:11] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/7ba43b50cb5c43d3af5a7d2719211047?acc_token=c93ffa60b5aa4300b8f3f9051450aea2
[13:10:11] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/plans/7ba43b50cb5c43d3af5a7d2719211047?acc_token=c93ffa60b5aa4300b8f3f9051450aea2 HTTP/11" 200 4101
[13:10:11] Response status code: 200

[13:10:11] Plan patched:
 - id                   7ba43b50cb5c43d3af5a7d2719211047
 - status               scheduled

[13:10:11] Creating tender...

[13:10:11] Processing data file: tender_create.json

[13:10:11] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/7ba43b50cb5c43d3af5a7d2719211047/tenders
[13:10:11] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans/7ba43b50cb5c43d3af5a7d2719211047/tenders HTTP/11" 201 7426
[13:10:11] Response status code: 201

[13:10:11] Tender created:
 - id                   e27104e551764b24b8c0487faf67b6fe
 - token                f22051fef57647f8adb4a518ed9b7f63
 - transfer             217d8625a7b1498d8adbba0c34075d32
 - status               draft
 - tenderID             UA-2025-07-02-000014-a
 - procurementMethodType closeFrameworkAgreementUA

[13:10:11] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e27104e551764b24b8c0487faf67b6fe
[13:10:11] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/tenders/e27104e551764b24b8c0487faf67b6fe HTTP/11" 200 7321
[13:10:11] Response status code: 200

[13:10:11] Processing data file: tender_document_attach.json

[13:10:11] Processing data file: tender_document_file.txt

[13:10:11] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:11] Starting new HTTPS connection (1): upload-docs-sandbox-2.prozorro.gov.ua:443
[13:10:11] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 578
[13:10:11] Response status code: 200

[13:10:11] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e27104e551764b24b8c0487faf67b6fe/documents?acc_token=f22051fef57647f8adb4a518ed9b7f63
[13:10:11] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/e27104e551764b24b8c0487faf67b6fe/documents?acc_token=f22051fef57647f8adb4a518ed9b7f63 HTTP/11" 201 578
[13:10:11] Response status code: 201

[13:10:11] Document attached:
 - id                   a891b5cd5bcc4eeebe7ee53f041ca6f4
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/8b9368ed65ca48ccb96f5cb374bde31c?Signature=3KGtpzBKO7k8I%2BBxJhJf42dovWpZ4MxCJI5Z9BJW5WFSMw0d5CEJXR3hXJCYe823R%2BMZS1EpgCG8BCXPofOZAg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:11] Create tender criteria...

[13:10:11] Processing data file: criteria_create.json

[13:10:11] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e27104e551764b24b8c0487faf67b6fe/criteria?acc_token=f22051fef57647f8adb4a518ed9b7f63
[13:10:12] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/e27104e551764b24b8c0487faf67b6fe/criteria?acc_token=f22051fef57647f8adb4a518ed9b7f63 HTTP/11" 201 86348
[13:10:12] Response status code: 201

[13:10:12] Tender criteria created:
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

[13:10:12] Processing data file: tender_notice_attach.json

[13:10:12] Processing data file: tender_notice_file.p7s

[13:10:12] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:12] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 576
[13:10:12] Response status code: 200

[13:10:12] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e27104e551764b24b8c0487faf67b6fe/documents?acc_token=f22051fef57647f8adb4a518ed9b7f63
[13:10:12] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/e27104e551764b24b8c0487faf67b6fe/documents?acc_token=f22051fef57647f8adb4a518ed9b7f63 HTTP/11" 201 600
[13:10:12] Response status code: 201

[13:10:12] Document attached:
 - id                   68642016086f4ff59cf686abc1a07174
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/9e2d6455725f4e48a1bf9b2be60ea750?Signature=TQv3w1D5KxC8neABL8LBh9kbHAvGDhKdZ2vZI8DO6BT%2B9t0IwaguLN8TCivTARgEEwmvUaRFJu7MfYklxX3CBg%3D%3D&KeyID=1331dc52
 - documentType         notice
 - confidentiality      public

[13:10:12] Patching tender...

[13:10:12] Processing data file: tender_patch.json

[13:10:12] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e27104e551764b24b8c0487faf67b6fe?acc_token=f22051fef57647f8adb4a518ed9b7f63
[13:10:12] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/tenders/e27104e551764b24b8c0487faf67b6fe?acc_token=f22051fef57647f8adb4a518ed9b7f63 HTTP/11" 200 94967
[13:10:12] Response status code: 200

[13:10:12] Tender patched:
 - id                   e27104e551764b24b8c0487faf67b6fe
 - status               active.tendering

[13:10:12] Skipping complaints creating: bot and reviewer tokens are required

[13:10:12] Creating bids...

[13:10:12] Processing data file: bid_create_0.json

[13:10:12] Processing data file: bid_document_file.txt

[13:10:12] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:12] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 577
[13:10:12] Response status code: 200

[13:10:12] Processing data file: bid_confidential_document_file.txt

[13:10:12] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:13] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 592
[13:10:13] Response status code: 200

[13:10:13] Processing data file: bid_eligibility_document_file.txt

[13:10:13] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:13] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 599
[13:10:13] Response status code: 200

[13:10:13] Processing data file: bid_financial_document_file.txt

[13:10:13] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:13] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 599
[13:10:13] Response status code: 200

[13:10:13] Processing data file: bid_qualification_document_file.txt

[13:10:13] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:13] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 595
[13:10:13] Response status code: 200

[13:10:13] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e27104e551764b24b8c0487faf67b6fe/bids
[13:10:13] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/e27104e551764b24b8c0487faf67b6fe/bids HTTP/11" 201 5137
[13:10:13] Response status code: 201

[13:10:13] Document attached:
 - id                   7a07c20bffdd4bf781929fcaa828be13
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/044f8c3144184444bc71ef10b16b17ba?Signature=zT2I9eBy2v%2Fa%2FLv72IbOZ27Da%2FclvyByNxA4gJVSK%2B%2Fc8WzCdZw0yCVLCakSizb8gh2zW%2BuUq5bqOSweqqF9Dg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:13] Document attached:
 - id                   1254c689d59a439395a750a9e039e9a9
 - confidentiality      buyerOnly

[13:10:13] Document attached:
 - id                   6876033e26654932aca8c4934b059bb4
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/e3b03b5552e940888b08b6e0a7484518?Signature=NoU%2FGmSUuzNN8e%2BWk34%2FuztfpBjEgjfNwY1OL5peJIm%2FFFyfGpWmeKCbiWARwBq%2BslXc2yJ6eOp4MQE4Ft1OAw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:13] Document attached:
 - id                   c36efbfdb01c40d8b175ca389b25db92
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/bffe11da4e79421db7220ba5e51d5b8a?Signature=bg%2BjH1T%2BcI5jnApVEtnUssvw07puzQuDDV7hxL4%2Bc2%2FZ9uiCakIqvU3oXnsiB09Xlzb2cZQNhdfF51l4n5z1Bw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:13] Document attached:
 - id                   3be4f34985904d68b38a6620201b093c
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/e7a5894e9ad64becaba57027f5badd49?Signature=gpkSzwb%2BRbDcB1h%2BwSnm1V%2FeCWMqiZpH9CvFolvdV7KWVj8FKNJJT32xzpOIwyuMqZRrSh0fhkSPP5sCQoujDA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:13] Bid created:
 - id                   6a5bae537d704d9e8beb05c393370782
 - token                f10b535a3ece49a5b278eb2d2a9abd74
 - status               draft

[13:10:13] Processing data file: bid_create_1.json

[13:10:13] Processing data file: bid_document_file.txt

[13:10:13] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:13] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 579
[13:10:13] Response status code: 200

[13:10:13] Processing data file: bid_confidential_document_file.txt

[13:10:13] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:13] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 594
[13:10:13] Response status code: 200

[13:10:13] Processing data file: bid_eligibility_document_file.txt

[13:10:13] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:13] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 601
[13:10:13] Response status code: 200

[13:10:13] Processing data file: bid_financial_document_file.txt

[13:10:13] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:13] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 601
[13:10:13] Response status code: 200

[13:10:13] Processing data file: bid_qualification_document_file.txt

[13:10:13] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:14] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 593
[13:10:14] Response status code: 200

[13:10:14] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e27104e551764b24b8c0487faf67b6fe/bids
[13:10:14] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/e27104e551764b24b8c0487faf67b6fe/bids HTTP/11" 201 5210
[13:10:14] Response status code: 201

[13:10:14] Document attached:
 - id                   fc68db2abde24058a6cbfc2e1e1f9d3d
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/be6b962c9d5b44dd8040aa579392d909?Signature=oe6LBUuT5%2ByiaTv5Vv%2FRNmaeeRmPSr5RnIbhVggdIetd2hXve4NN6M7s6B4xg1N8xKe7wFDnZkYmwlRfdgibDA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:14] Document attached:
 - id                   1aafe5d54d6342ebb37473fd60f66e66
 - confidentiality      buyerOnly

[13:10:14] Document attached:
 - id                   32d52bfed02a4f22b7e9667ef7b62b3f
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/1e5fb2d71b134306b7763791add2194f?Signature=cg9%2Bs5kQGtMDyoQLbk9TDO5CiHusr84CXLxG09RxAb2N5F3bYMxY1cflazunIi8C33EJk4TX4zxFKwhzYiuXBA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:14] Document attached:
 - id                   27a35cac7e66458d9f284d7071e678b7
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/7a0ac0e5edcf409a84d6237d2582b506?Signature=95pOFuKsaWHKYTc2P85qtZ1uI1L6Lzr9QMoaraeNnTOv6Jv5mhwLUVDBFgPXbVvTIfmtFzqs1lB4ftKvxgY7Ag%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:14] Document attached:
 - id                   50f00835726541f395533309211ea206
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/fbe79039f26d48ef9126c5b624d19b7e?Signature=nEki9wJbv7UdBUP34if3CBhLeK2sPSSnQtcDoh3Q8D7Acmvg5iNRJJ1gNi30FI8C4Eqt%2BQu8DHB9cBYZlnBQBg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:14] Bid created:
 - id                   dea36dfbde9e43c69d1a32bee45f0b1d
 - token                a07fe2af83bb4471bd8957d448863fac
 - status               draft

[13:10:14] Processing data file: bid_create_2.json

[13:10:14] Processing data file: bid_document_file.txt

[13:10:14] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:14] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 587
[13:10:14] Response status code: 200

[13:10:14] Processing data file: bid_confidential_document_file.txt

[13:10:14] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:14] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 596
[13:10:14] Response status code: 200

[13:10:14] Processing data file: bid_eligibility_document_file.txt

[13:10:14] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:14] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 595
[13:10:14] Response status code: 200

[13:10:14] Processing data file: bid_financial_document_file.txt

[13:10:14] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:14] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 593
[13:10:14] Response status code: 200

[13:10:14] Processing data file: bid_qualification_document_file.txt

[13:10:14] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:14] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 593
[13:10:14] Response status code: 200

[13:10:14] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e27104e551764b24b8c0487faf67b6fe/bids
[13:10:14] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/e27104e551764b24b8c0487faf67b6fe/bids HTTP/11" 201 5214
[13:10:14] Response status code: 201

[13:10:14] Document attached:
 - id                   16a0522fe9a54d95b15f88cf937add63
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/4714914e683449888318514956d6a9d7?Signature=MA63FuFSM7YAtJuqJ66NWUM5LJFuQPTxxkO7%2FwNz2UrzSqmvSuyPN5AaqU5qFbD6MS%2F5K%2BPHk2cRF2gLUFsZAQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:14] Document attached:
 - id                   53c7ad789bda49d5ba963486a23f6a6d
 - confidentiality      buyerOnly

[13:10:14] Document attached:
 - id                   8495e63172b642f89441f343ddb90a07
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/19de9f61f4734118853f4893c68806e1?Signature=piWUhqrbp5zlacvEVeg08qm8XcOp1xMlpmNPySQiVp84mgReo6AL3DG8bYu44cq4Kh8uNE07vwFISd705IrtBQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:14] Document attached:
 - id                   7cb3a66841ca4ae996a63d50f3a79713
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/17a09386c6eb4138a54ba8265ede367e?Signature=goXsVS0soy0vO1xHh0MFx9zyrM6GIrzAXkq3fXDz8uY0xuN5lOT1lTzIR70O%2Bn4BL2T2SPu4ZexQA8BbWiDbCA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:14] Document attached:
 - id                   4f921c28ee094959a00b09f080736d87
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/1cff9b75f8f14898b0e8244d6b7b0235?Signature=YhtWiYpQb1cKWQFZHdDFzcn58HO4tY7CCFTl%2FN1fJ37sgP43nB1P7s2HTpqHZ%2FrO5i5OctY7HXOiqcQL9XZHDw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:14] Bid created:
 - id                   6fbf4b1b7c734628808d2019b44b5c1e
 - token                b95c7abb2f15440191bc0d9758be291b
 - status               draft

[13:10:14] Processing data file: bid_create_3.json

[13:10:14] Processing data file: bid_document_file.txt

[13:10:14] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:14] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 593
[13:10:14] Response status code: 200

[13:10:14] Processing data file: bid_confidential_document_file.txt

[13:10:14] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:14] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 598
[13:10:14] Response status code: 200

[13:10:14] Processing data file: bid_eligibility_document_file.txt

[13:10:14] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:15] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 595
[13:10:15] Response status code: 200

[13:10:15] Processing data file: bid_financial_document_file.txt

[13:10:15] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:15] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 603
[13:10:15] Response status code: 200

[13:10:15] Processing data file: bid_qualification_document_file.txt

[13:10:15] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[13:10:15] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 619
[13:10:15] Response status code: 200

[13:10:15] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/e27104e551764b24b8c0487faf67b6fe/bids
[13:10:15] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/e27104e551764b24b8c0487faf67b6fe/bids HTTP/11" 201 5232
[13:10:15] Response status code: 201

[13:10:15] Document attached:
 - id                   926875044ce049f5bc700c357714181f
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/16ef839addb64b49ad995167fb7b0e14?Signature=TznTroXAfUzOzKTZ%2F8KmT5zj%2B8OMwM2mN5%2FF4ZaOgpFXdpxFI32iezvz4XeW4XC8chI%2BX6GkWkxL2fi%2FDCA2AQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:15] Document attached:
 - id                   4b62acd9b68841889aa73d86723d4468
 - confidentiality      buyerOnly

[13:10:15] Document attached:
 - id                   df72d3f0b69b4249aa3557a33cf4dfe6
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/12c362d494f94f729da8f02a11e22bca?Signature=uE6lD%2FpAIgEqDm%2B%2BUmwXU1aNk8y6Z%2Buc0wj1OU3tffA7Req%2BYZ%2BKIVIsw%2BCIjM895NOIVFi7q4ghnqT6T5isAg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:15] Document attached:
 - id                   5f442032e5de4126838aaea294c3d990
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/5eb322559d0145bc9baf5ee83039ee87?Signature=My6vD%2BAzThjV02m2%2BmYxiTyjaSblmCkvt7ZdifsznChaAvmv2i2uwr9ZX90jNfrPI2OGTZcK9gHg0GjLYvaNAw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:15] Document attached:
 - id                   77caeda78fe6408fbc179b78764ac9c7
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/07ec482c70b547ab8180b75ecc4e1eb7?Signature=5shv9uIIF66d9DSTxdbZQRfXtpT9UDtk8EWiHpu3KaUhr%2FQsshtCFEl3Ls6Tc61iOXG21KZt0WqVmKKJ5j9PBA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[13:10:15] Bid created:
 - id                   cb2e7c0b6ccc401c9648aef00e2690fb
 - token                cc677c2e656e4e98a74a53b01d000afe
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
