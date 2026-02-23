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
[00:13:59] Using seed 682565

[00:13:59] Initializing cdb client

[00:13:59] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[00:13:59] Starting new HTTPS connection (1): lb-api-sandbox-2.prozorro.gov.ua:443
[00:13:59] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/spore HTTP/11" 200 1205740
[00:13:59] Response status code: 200

[00:13:59] Client time delta with server: -822 milliseconds

[00:13:59] Initializing ds client

[00:13:59] Creating framework...

[00:13:59] Processing data file: framework_create.json

[00:13:59] Skipping...

[00:13:59] Creating plan...

[00:13:59] Processing data file: plan_create.json

[00:13:59] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[00:13:59] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans HTTP/11" 201 4202
[00:13:59] Response status code: 201

[00:13:59] Plan created:
 - id                   688207fd911b4352a256187cae18de5e
 - token                b64000033fbf4ef5bb554db8821b2e83
 - transfer             0517d7b664354298bf57f66a9a475470
 - status               draft

[00:13:59] Patching plan...

[00:13:59] Processing data file: plan_patch.json

[00:13:59] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/688207fd911b4352a256187cae18de5e?acc_token=b64000033fbf4ef5bb554db8821b2e83
[00:13:59] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/plans/688207fd911b4352a256187cae18de5e?acc_token=b64000033fbf4ef5bb554db8821b2e83 HTTP/11" 200 4101
[00:13:59] Response status code: 200

[00:13:59] Plan patched:
 - id                   688207fd911b4352a256187cae18de5e
 - status               scheduled

[00:13:59] Creating tender...

[00:13:59] Processing data file: tender_create.json

[00:13:59] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/688207fd911b4352a256187cae18de5e/tenders
[00:14:00] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans/688207fd911b4352a256187cae18de5e/tenders HTTP/11" 201 28426
[00:14:00] Response status code: 201

[00:14:00] Tender created:
 - id                   702dc23f89304148ab3e7ba2f5fd7687
 - token                2fcc0122003d41c283af99b687aaef15
 - transfer             a31875c1b763494892a2693206b16591
 - status               draft
 - tenderID             UA-2026-02-23-000011-a
 - procurementMethodType closeFrameworkAgreementUA

[00:14:00] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687
[00:14:00] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687 HTTP/11" 200 28321
[00:14:00] Response status code: 200

[00:14:00] Processing data file: tender_document_attach.json

[00:14:00] Processing data file: tender_document_file.txt

[00:14:00] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:00] Starting new HTTPS connection (1): upload-docs-sandbox-2.prozorro.gov.ua:443
[00:14:00] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 582
[00:14:00] Response status code: 200

[00:14:00] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/documents?acc_token=2fcc0122003d41c283af99b687aaef15
[00:14:00] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/documents?acc_token=2fcc0122003d41c283af99b687aaef15 HTTP/11" 201 576
[00:14:00] Response status code: 201

[00:14:00] Document attached:
 - id                   2b4c095bf37445ec93de092edeb54171
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/42d638c79627475595c30b4fb8baf4a2?Signature=uKnLwchQfvCpdrB5amOeSPnz7BFDQ1e5YIloXhV0893n8AqP2L0CF4sgTg1Uvn%2FaHQTVweniE0DqTc3riW7MCA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:00] Processing data file: contract_proforma_attach.json

[00:14:00] Processing data file: contract_proforma.txt

[00:14:00] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:00] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 583
[00:14:00] Response status code: 200

[00:14:00] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/documents?acc_token=2fcc0122003d41c283af99b687aaef15
[00:14:00] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/documents?acc_token=2fcc0122003d41c283af99b687aaef15 HTTP/11" 201 617
[00:14:00] Response status code: 201

[00:14:00] Document attached:
 - id                   78be3c25406f4248b9bc045b131e8752
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/8ad81d93259a4e5c8452e8296e76656c?Signature=G2voDb4lo4u%2B660gy6DEa5wYgn6NCYkckjEj0%2B5IaLaxIPmAFgRqtEH%2BDKm4hkJcaz%2BUzh%2FvdSuk5w8pRycbAw%3D%3D&KeyID=1331dc52
 - documentType         contractProforma
 - confidentiality      public

[00:14:00] Create tender criteria...

[00:14:00] Processing data file: criteria_create.json

[00:14:00] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/criteria?acc_token=2fcc0122003d41c283af99b687aaef15
[00:14:00] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/criteria?acc_token=2fcc0122003d41c283af99b687aaef15 HTTP/11" 201 93928
[00:14:00] Response status code: 201

[00:14:00] Tender criteria created:
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

[00:14:00] Processing data file: tender_notice_attach.json

[00:14:00] Processing data file: tender_notice_file.p7s

[00:14:00] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:01] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 588
[00:14:01] Response status code: 200

[00:14:01] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/documents?acc_token=2fcc0122003d41c283af99b687aaef15
[00:14:01] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/documents?acc_token=2fcc0122003d41c283af99b687aaef15 HTTP/11" 201 604
[00:14:01] Response status code: 201

[00:14:01] Document attached:
 - id                   1b441e7cd89c4d4198896c871ed3f1cb
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/4cbf66c8547c45db9f29d2fcb084d8b3?Signature=bgqWs1gufQ%2BZH9%2FdG5uDPPcDQHXH60%2F3aHCnWXsEd1H1ZXHbIxX56gTI5jUikD1flTXqpEmUs0et0BYqiBmPDw%3D%3D&KeyID=1331dc52
 - documentType         notice
 - confidentiality      public

[00:14:01] Patching tender...

[00:14:01] Processing data file: tender_patch.json

[00:14:01] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687?acc_token=2fcc0122003d41c283af99b687aaef15
[00:14:01] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687?acc_token=2fcc0122003d41c283af99b687aaef15 HTTP/11" 200 124158
[00:14:01] Response status code: 200

[00:14:01] Tender patched:
 - id                   702dc23f89304148ab3e7ba2f5fd7687
 - status               active.tendering

[00:14:01] Skipping complaints creating: bot and reviewer tokens are required

[00:14:01] Creating bids...

[00:14:01] Processing data file: bid_create_0.json

[00:14:01] Processing data file: bid_document_file.txt

[00:14:01] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:01] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 575
[00:14:01] Response status code: 200

[00:14:01] Processing data file: bid_confidential_document_file.txt

[00:14:01] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:01] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 584
[00:14:01] Response status code: 200

[00:14:01] Processing data file: bid_eligibility_document_file.txt

[00:14:01] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:01] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 603
[00:14:01] Response status code: 200

[00:14:01] Processing data file: bid_financial_document_file.txt

[00:14:01] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:01] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 591
[00:14:01] Response status code: 200

[00:14:01] Processing data file: bid_qualification_document_file.txt

[00:14:01] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:01] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 603
[00:14:01] Response status code: 200

[00:14:01] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/bids
[00:14:02] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/bids HTTP/11" 201 5119
[00:14:02] Response status code: 201

[00:14:02] Document attached:
 - id                   7d0dee12f7984ad1b4611ab68f1b6546
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/ea107301fdbb4bcab8d718c14bf87c77?Signature=lVZcv5zCcomgskiZlL7mUJ5dO%2FvuXIUDUksxLM2YCV4v1Ps%2BI7eEmhbdknh6THmsO8XxfyF408jIBjG6GU%2FTDw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:02] Document attached:
 - id                   d69f2df14ac94bb29a991a348647294a
 - confidentiality      buyerOnly

[00:14:02] Document attached:
 - id                   fa8888e8f5664285b1f4f0bb611d43d8
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/55b6a92f5f774c25a2faaae382c6042b?Signature=yEJWLl%2FJkNkjDVOobG3QMxSM3ZDlEPytQ5aydOm7OfD0DwLQtttjDUJGJjGoEp4RjzJFbqibpVBhVmpxSZxRAQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:02] Document attached:
 - id                   78b652e18b334476b725bb18cd2b2863
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/6bbc6a97db2d49d0bef3b638bea221f1?Signature=i05we%2BCfNw88PACxte41vvSPyF31xTNqUtx%2B8%2Fu583T5XfAAavFmG626Sc%2F94GJ7tM95f4H79NzN06n3bZVNBA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:02] Document attached:
 - id                   72f0e0193cec45b3890fd290b98295e8
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/e9c1ae26e3144ea6a03313e6e2e7e69f?Signature=wXHf2AoZb8LQEhB0r5yQ6O4JgCoQs3hPO%2BkhkJsdx4YEjqBsLw2udD2djFsQciMRfCS7qEqTuj8Ji1JCtSkADg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:02] Bid created:
 - id                   c6a2ac53930d44858320f740b8d83317
 - token                5d1bb31c6ab24d67b02fca772183d16d
 - status               draft

[00:14:02] Processing data file: bid_create_1.json

[00:14:02] Processing data file: bid_document_file.txt

[00:14:02] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:02] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 587
[00:14:02] Response status code: 200

[00:14:02] Processing data file: bid_confidential_document_file.txt

[00:14:02] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:02] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 598
[00:14:02] Response status code: 200

[00:14:02] Processing data file: bid_eligibility_document_file.txt

[00:14:02] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:02] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 603
[00:14:02] Response status code: 200

[00:14:02] Processing data file: bid_financial_document_file.txt

[00:14:02] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:02] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 597
[00:14:02] Response status code: 200

[00:14:02] Processing data file: bid_qualification_document_file.txt

[00:14:02] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:02] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 587
[00:14:02] Response status code: 200

[00:14:02] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/bids
[00:14:02] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/bids HTTP/11" 201 5234
[00:14:02] Response status code: 201

[00:14:02] Document attached:
 - id                   b0c2dbf3562e4156b0cb681c3929e928
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/6dccf312785d4962a2fea9b1642a21f7?Signature=B9cuG2XDuBXtShiEOkOvsNjPiHxOYcQWlU4uKNcDGM5TCRfNB0HaOUiVUy%2BRGezT0bsdEeFNv6%2Bfb44XFszhDw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:02] Document attached:
 - id                   744621a51c444a20ad174f18af1edae0
 - confidentiality      buyerOnly

[00:14:02] Document attached:
 - id                   5f26af4b047c422d99dd7bf564b4ba5a
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/940d33ed753648f18b26ed007a5007ba?Signature=szZ3qXRGPMfIQ8jIhgNx%2FNiikP%2BVgsaV7vevNK%2B5dhYw%2B3EDegyHECArH%2FuKW4fZiEqSqAyu6F0DUlzBS%2FXVCw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:02] Document attached:
 - id                   7b1cb70a3c4c405b9e987341dd8a4223
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/4701c29c421d40158b56776c09a53ec2?Signature=H2olbARvfH%2BTGaiejhUCA5MpCn%2B9KbOu%2BM4qwoaWXa3wm%2FpUlHJeCGEZ3v4We0XXfCk5j4%2FHWVcgGp1CgsCyCA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:02] Document attached:
 - id                   3d86bf4b98a64f1b8072b3e2e8deae53
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/e3200d09b6234f3394f04dd6a2b4545f?Signature=BJUQjyDyG2hB6xlE0kot0qhLiDV8aYdUempBLpMMB4BeUA8cb44Ix6t%2BRh4vAcEAyT3JBpFe%2B8HmYWs%2FC0BaAA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:02] Bid created:
 - id                   7447007d53744cd4a539479f277c8586
 - token                5923ca733d8b400ca651d17b24a58677
 - status               draft

[00:14:02] Processing data file: bid_create_2.json

[00:14:02] Processing data file: bid_document_file.txt

[00:14:02] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:02] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 591
[00:14:02] Response status code: 200

[00:14:02] Processing data file: bid_confidential_document_file.txt

[00:14:02] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:03] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 592
[00:14:03] Response status code: 200

[00:14:03] Processing data file: bid_eligibility_document_file.txt

[00:14:03] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:03] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 601
[00:14:03] Response status code: 200

[00:14:03] Processing data file: bid_financial_document_file.txt

[00:14:03] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:03] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 607
[00:14:03] Response status code: 200

[00:14:03] Processing data file: bid_qualification_document_file.txt

[00:14:03] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:03] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 601
[00:14:03] Response status code: 200

[00:14:03] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/bids
[00:14:03] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/bids HTTP/11" 201 5216
[00:14:03] Response status code: 201

[00:14:03] Document attached:
 - id                   ae43712fdbfc4627b3f122dfee9d1979
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/290c7d01ec3a4d2ca37d09c89ac9f1e1?Signature=UCrt1nO7VC4SHJXMylZyKdwWvWn6Wae%2BLlL94CLwf5IMIMb1amQBMa7%2B%2FZE4WIPB6DHQVOBFsPQB8MW6Qqc5AQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:03] Document attached:
 - id                   d13021ac9d104d6a9cbbaf8ba4869902
 - confidentiality      buyerOnly

[00:14:03] Document attached:
 - id                   83bdda2b687443b8af240c3e3c83b7dc
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/c13b3983a84c42758c698dcf169e4c25?Signature=nHlhnLAN20z1uJQuM2ygI7KaocPkajbuOzZJvkVNCmWtxNur4IcAIq2IBsrzTEPDMkq6lvQLG3t2iLPBCP5TBg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:03] Document attached:
 - id                   9d84cc852ed64c87b789727ccaddce07
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/58dd3aa2a99e474d9539db63fa173a54?Signature=GLo7VA5mT7Bg5nZ3NVWvhvxGcFCqtcwFJDLkhJFEiHJxkH0UbLz4%2FOH4QxS3c%2BuQosCuQfbHL5oII4wWftIvAQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:03] Document attached:
 - id                   4dc0ee49ba614c0380919d759730a922
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/a74513c1b4ec466a853dba5c5a303c45?Signature=fmpEVp3V0n3LRS8uoW5kseaoLifc20atEzqNfqfFCEE8Tvw%2BCiK2AsfLynDgtnqzNgpd5zZuxsM1DOC3ciG%2FDQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:03] Bid created:
 - id                   e23bd7dd1b5c40638124cfd632768668
 - token                91f35592f8b4411fb42c13953d6015e0
 - status               draft

[00:14:03] Processing data file: bid_create_3.json

[00:14:03] Processing data file: bid_document_file.txt

[00:14:03] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:03] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 577
[00:14:03] Response status code: 200

[00:14:03] Processing data file: bid_confidential_document_file.txt

[00:14:03] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:03] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 596
[00:14:03] Response status code: 200

[00:14:03] Processing data file: bid_eligibility_document_file.txt

[00:14:03] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:03] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 599
[00:14:03] Response status code: 200

[00:14:03] Processing data file: bid_financial_document_file.txt

[00:14:03] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:03] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 593
[00:14:03] Response status code: 200

[00:14:03] Processing data file: bid_qualification_document_file.txt

[00:14:03] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[00:14:03] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 601
[00:14:03] Response status code: 200

[00:14:03] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/bids
[00:14:04] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/702dc23f89304148ab3e7ba2f5fd7687/bids HTTP/11" 201 5232
[00:14:04] Response status code: 201

[00:14:04] Document attached:
 - id                   113ee7f68f5b4934af656da10b40d95e
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/5fc6d70692fe4687805bd0d8e79fe066?Signature=RdVxBg80h7k1iFhaKyiX2qq3ij7W9lLGQT16DoobHTuAxQmiY4STYj%2Fwq6iY%2BDf8zhocYZ%2FbP6AYqF3wICMABQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:04] Document attached:
 - id                   2ce4225330414e2e8b6cfa3ff8af6d78
 - confidentiality      buyerOnly

[00:14:04] Document attached:
 - id                   7f1f33863a7140c6a51cdfa9c05c9db8
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/2d4bcb3920244229b3c4d622859d7392?Signature=%2B8%2BGCxicsaCjzgtoOmSJUdoTZvtC%2BBHViALq3%2Bc18hxtt%2FtSKsv%2BuJYD4B9x%2BnQ1FmlItWlySNfzSiEB4VCEDg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:04] Document attached:
 - id                   345f8cd9337544dbb66109ccdd842bcb
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/1164e63de4594fdda372f9736b2fc8fe?Signature=4dzztMJX42uqdBEFzvjIF8Y%2BPkp3hXv414EusmTjf5WMqaZFHHYSwUZfVWF3K1j0HKqmyBsDR5bYknaogVe8AA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:04] Document attached:
 - id                   85ecb39b4001438cb17e25ad08db9557
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/d0e7afa228f042c4a6c3484c8031b8e5?Signature=XSa3Pli2piCWIMmNpOh%2ByTC%2FnmuliOIRIG3u7G%2Fn0xrRBz73N6TrOfxf%2BAQFRl4eAG0pK6haNy56L0bJuswwBg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[00:14:04] Bid created:
 - id                   5edba6149641428b8f1209a75c782405
 - token                58aa3d378d89403291165450f2bda298
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
