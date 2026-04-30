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
                 [--debug] [--debug-req]
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
03:39:37 Using seed 497881

03:39:37 Initializing cdb client

03:39:37 [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
03:39:37 Response status code: 200

03:39:37 Response status code: 200

03:39:37 Client time delta with server: -951 milliseconds

03:39:37 Initializing ds client

03:39:37 Creating framework...

03:39:37 Processing data file: framework_create.json

03:39:37 Skipping...

03:39:37 Creating plan...

03:39:37 Processing data file: plan_create.json

03:39:37 [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
03:39:38 Response status code: 201

03:39:38 Plan created:
 - id                   4adaa946b0274b26b3cc85232e9c6867
 - token                945177289cd3436bb1831c9ebc177bbd
 - transfer             81e946d510f545089db2f4a1cbef46b5
 - status               draft

03:39:38 Patching plan...

03:39:38 Processing data file: plan_patch.json

03:39:38 [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/4adaa946b0274b26b3cc85232e9c6867?acc_token=945177289cd3436bb1831c9ebc177bbd
03:39:38 Response status code: 200

03:39:38 Plan patched:
 - id                   4adaa946b0274b26b3cc85232e9c6867
 - status               scheduled

03:39:38 Creating tender...

03:39:38 Processing data file: tender_create.json

03:39:38 [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/4adaa946b0274b26b3cc85232e9c6867/tenders
03:39:38 Response status code: 201

03:39:38 Tender created:
 - id                   3a10ece1bfa949148cf699c8b9e44be1
 - token                1b923f5dc4d84fd2a80f4f7dfa260367
 - transfer             0f4d49d834b24a019d5ca493c23294de
 - status               draft
 - tenderID             UA-2026-04-30-000068-a
 - procurementMethodType closeFrameworkAgreementUA

03:39:38 [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/3a10ece1bfa949148cf699c8b9e44be1
03:39:38 Response status code: 200

03:39:38 Processing data file: tender_document_attach.json

03:39:38 Processing data file: tender_document_file.txt

03:39:38 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:39 Response status code: 200

03:39:39 [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/3a10ece1bfa949148cf699c8b9e44be1/documents?acc_token=1b923f5dc4d84fd2a80f4f7dfa260367
03:39:39 Response status code: 201

03:39:39 Document attached:
 - id                   9c345a5b59434e20a8fecfad63e53866
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/37865314b2c64d848f899f784f8f2056?Signature=fqQwuUZU1%2FE7%2FxoQRIXtjfLUbQ6neBsu5Ch0%2FRb0fW6%2FkKFYQHAeQ0AlJHqsJS8t%2F%2BH6kLyftTFFgDO62ynkAA%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:39 Processing data file: contract_proforma_attach.json

03:39:39 Processing data file: contract_proforma.txt

03:39:39 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:39 Response status code: 200

03:39:39 [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/3a10ece1bfa949148cf699c8b9e44be1/documents?acc_token=1b923f5dc4d84fd2a80f4f7dfa260367
03:39:39 Response status code: 201

03:39:39 Document attached:
 - id                   7e48f5289c8f4c0fb209ba74a7d0bfc7
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/5172a0b7c3d9490e8846dd2b9418a845?Signature=gviIgOWPrMyytCRTwBWwSK1%2BOYWwCMU2fA1n0ozcqz3B0vXWFFaKphsv3MQkBsci8DuOvqA968xHHYv1sGw1Cw%3D%3D&KeyID=1331dc52
 - documentType         contractProforma
 - confidentiality      public

03:39:39 Create tender criteria...

03:39:39 Processing data file: criteria_create.json

03:39:39 [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/3a10ece1bfa949148cf699c8b9e44be1/criteria?acc_token=1b923f5dc4d84fd2a80f4f7dfa260367
03:39:39 Response status code: 201

03:39:39 Tender criteria created:
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

03:39:39 Processing data file: tender_notice_attach.json

03:39:39 Processing data file: tender_notice_file.p7s

03:39:39 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:40 Response status code: 200

03:39:40 [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/3a10ece1bfa949148cf699c8b9e44be1/documents?acc_token=1b923f5dc4d84fd2a80f4f7dfa260367
03:39:40 Response status code: 201

03:39:40 Document attached:
 - id                   1d64c52c64c54f4e83c95c217cf4b9bd
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/15d141ef5edd4978857521cda59284c9?Signature=pHDZyFEy%2Fkjfcb7Sg6RAYToPt08qvvfxZCQ56kUudwVjc1ApQOBYifvY0ZNPLetKPqolozL4%2FijocjV7U9t9Cg%3D%3D&KeyID=1331dc52
 - documentType         notice
 - confidentiality      public

03:39:40 Patching tender...

03:39:40 Processing data file: tender_patch.json

03:39:40 [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/3a10ece1bfa949148cf699c8b9e44be1?acc_token=1b923f5dc4d84fd2a80f4f7dfa260367
03:39:40 Response status code: 200

03:39:40 Tender patched:
 - id                   3a10ece1bfa949148cf699c8b9e44be1
 - status               active.tendering

03:39:40 Skipping complaints creating: bot and reviewer tokens are required

03:39:40 Creating bids...

03:39:40 Processing data file: bid_create_0.json

03:39:40 Processing data file: bid_document_file.txt

03:39:40 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:41 Response status code: 200

03:39:41 Processing data file: bid_confidential_document_file.txt

03:39:41 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:41 Response status code: 200

03:39:41 Processing data file: bid_eligibility_document_file.txt

03:39:41 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:41 Response status code: 200

03:39:41 Processing data file: bid_financial_document_file.txt

03:39:41 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:41 Response status code: 200

03:39:41 Processing data file: bid_qualification_document_file.txt

03:39:41 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:42 Response status code: 200

03:39:42 [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/3a10ece1bfa949148cf699c8b9e44be1/bids
03:39:42 Response status code: 201

03:39:42 Document attached:
 - id                   280fcff4e2ff47b8bbefddcea18a17d4
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/878ac72c24264215953fe8d7fb9ff812?Signature=WIWTEdEE7E%2BBkId6t22Afjs0ynpisuOPJh1HiYmgJu84HKIHf0UiT5DgMHaRVNP1Hayu7ex3FsSn%2BV07W5DPBQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:42 Document attached:
 - id                   0c920f0ef35141b1a3adff3d08ce2a83
 - confidentiality      buyerOnly

03:39:42 Document attached:
 - id                   8bcd4ca416b44d5b9532a158dbb671ad
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/d8784ffbe2114fa78fd936913a1b96c1?Signature=BTj1gVAFwJt0WyycLi%2BChTbFhYm88evFx0qgHOfZ%2Bki3ReobupIjYHnVUhqqMvdkndPX164hiZRhKI9vzCLfAA%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:42 Document attached:
 - id                   88c0f9e1e87d4a749e76a0fcad389397
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/3651ecd41f634d7a96d8cc43b61ffbc8?Signature=zYNz%2BM3d%2FuJklR1XSf0OAkw7f9af4I%2BWn1DoyiLuDn7Ag4If3QuHr8z9E1Hk5HIdwTg5U87YTge75KI3RtnfBw%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:42 Document attached:
 - id                   1bd5f29dba3b401bbc3c126e9f8591b6
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/5709bd398e4a40f393e4d1b78fe72178?Signature=u3LlSQQtkOhskJe74L4rn3o4eHxYVqoVIiBHzLZjWzOzS1S61i5w3KjXRzYvNjTaQzCVi0oBhALV%2FWvGv3zWBA%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:42 Bid created:
 - id                   fa38c2b7fd5f4b5fb0e5cb8f3821e254
 - token                b9c0a58a95754595a5fd09bab1397e30
 - status               draft

03:39:42 Processing data file: bid_create_1.json

03:39:42 Processing data file: bid_document_file.txt

03:39:42 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:42 Response status code: 200

03:39:42 Processing data file: bid_confidential_document_file.txt

03:39:42 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:42 Response status code: 200

03:39:42 Processing data file: bid_eligibility_document_file.txt

03:39:42 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:42 Response status code: 200

03:39:42 Processing data file: bid_financial_document_file.txt

03:39:42 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:42 Response status code: 200

03:39:42 Processing data file: bid_qualification_document_file.txt

03:39:42 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:42 Response status code: 200

03:39:42 [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/3a10ece1bfa949148cf699c8b9e44be1/bids
03:39:43 Response status code: 201

03:39:43 Document attached:
 - id                   7bbba7aafe574c9da3cda5dff6f73a70
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/b28b2a7149a147648c38f574e8e2aad3?Signature=UIRA%2BIRUe4tu8pQMnRszmBeCL8kRv%2F4jwdIadxInXWxoF24MCXBTrHNQeXGKWGvupEVE0Rl%2Ft7sNMDHw2jgLCg%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:43 Document attached:
 - id                   426ced9665f64226933acd6f105f20b6
 - confidentiality      buyerOnly

03:39:43 Document attached:
 - id                   1475de9dbfbf48eda25de3376ecdc74d
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/9072a228c2c44c4a9d7aabe13a671d1b?Signature=FMZhprRnfjKba948T7PxSU42bsqG2O6sVjyJKj%2B5VBp2IzgQRs%2B7Dt7u%2Bs8t30YrzKBI1WlT0luaUd9iGzKzCA%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:43 Document attached:
 - id                   c66b21be8a94401794f9ccae1f9b8406
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/9e78a615b11e434e95979ff5a8acc296?Signature=QPSB34RBdmyM3zI83DhmDR0u3zYqDU1HHQHb4m%2BO2Zm1B8JfwvJCVApgT%2BWoaFoAxaKJxRaq6knzQfcby0cCBg%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:43 Document attached:
 - id                   c39ebbf61ea546f590825b1d1d3efba4
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/42ddd87f66db418d99f518ac665c3244?Signature=uY6aRy6g2vltLxaKrerj%2BEGiFNOvcvYcKs8WOJMQlaJKORMSMugSAs4FKJtDywWcYRmogYfv9nyiM%2Bs%2B8U%2BsAg%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:43 Bid created:
 - id                   c75f932d766b4498818e78ba5262e571
 - token                ca2c3fe4580a4508a0d9aeb9e6715afa
 - status               draft

03:39:43 Processing data file: bid_create_2.json

03:39:43 Processing data file: bid_document_file.txt

03:39:43 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:43 Response status code: 200

03:39:43 Processing data file: bid_confidential_document_file.txt

03:39:43 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:43 Response status code: 200

03:39:43 Processing data file: bid_eligibility_document_file.txt

03:39:43 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:43 Response status code: 200

03:39:43 Processing data file: bid_financial_document_file.txt

03:39:43 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:43 Response status code: 200

03:39:43 Processing data file: bid_qualification_document_file.txt

03:39:43 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:43 Response status code: 200

03:39:43 [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/3a10ece1bfa949148cf699c8b9e44be1/bids
03:39:43 Response status code: 201

03:39:43 Document attached:
 - id                   c2d664f309634e4e90a6ea3eb559268a
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/ac142c7b04564ffc9d125a089c613782?Signature=iBODiPfmblSMw%2FHbBD%2BeOBdomVx%2BlDaT5zj8N5XdwjgLft591vq59kts3n7Kkt41rq6GThEbi69xi52J5vFxBQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:43 Document attached:
 - id                   396c0a2b13714c79afe0c9f1d3ade5a3
 - confidentiality      buyerOnly

03:39:43 Document attached:
 - id                   e74792341d914b4a8b7ef6d6fb8497e2
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/63c95427ff7943249a01af0ee6fdcc6a?Signature=2EgaK7WdyVSwTBrumP253rkfBBIUMXAUsgIVV3Zof5C3G1kdW1QAwXkD%2FPs5rIuhWbXN0fDHiwsHRKgRvAZ0DQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:43 Document attached:
 - id                   f3b12132e3604c18879aef1253620e01
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/2c142f8c0a1a4b8889cf95133ead1882?Signature=IUBtxyoObG1hT2uX9EzYqSXRWHWfiChJXs1q6Q9%2BoU1uxQs0QkKfLUYXKIAVKSCuUvz98AmwaoVd6XOvLTWgDQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:43 Document attached:
 - id                   2b4a91538a454a8e8d8a034a586ecd5b
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/16731c6a566d4881a9b74df64af3b582?Signature=Dbuj8W9fM3g27s7ZH3MdPyY9wKBBjuAsleQD9%2FBzQevwsmqnInre4h%2Fm1AYIIvRXhrWZlKbXgDtmNgyCUpZvBA%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:43 Bid created:
 - id                   bf8e0b6868274ad49ac827680624ef6d
 - token                7abe6a015b79423380cb15d95ecad6c5
 - status               draft

03:39:43 Processing data file: bid_create_3.json

03:39:43 Processing data file: bid_document_file.txt

03:39:43 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:44 Response status code: 200

03:39:44 Processing data file: bid_confidential_document_file.txt

03:39:44 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:44 Response status code: 200

03:39:44 Processing data file: bid_eligibility_document_file.txt

03:39:44 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:44 Response status code: 200

03:39:44 Processing data file: bid_financial_document_file.txt

03:39:44 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:44 Response status code: 200

03:39:44 Processing data file: bid_qualification_document_file.txt

03:39:44 [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
03:39:44 Response status code: 200

03:39:44 [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/3a10ece1bfa949148cf699c8b9e44be1/bids
03:39:44 Response status code: 201

03:39:44 Document attached:
 - id                   097df5f0e18f494699ffb3624bd2aeeb
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/8370f9fc7a914f94bf8efe62c7216637?Signature=IOiwGxsA7FBaicZ3%2F1ET%2BfNFTreW0%2Ftn6Z%2B01qCuiPs7WgoFOi1uNF1Rd7zGrh7HYU5zXjCRerzoOTeH1S%2B%2BDQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:44 Document attached:
 - id                   873df6cfe4114541976839e348295bb6
 - confidentiality      buyerOnly

03:39:44 Document attached:
 - id                   1adf8beaf055426bba48f2bcddaab59e
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/2cd8a5074e12407796a595020a6095a7?Signature=1iPkb7eXLw1%2Bxs8i1w%2BP9VkofTmGic0Wn0NjU9%2Bz9f2%2BADPSbq%2FIam6AgKbnq0oFxe7QuHAhBHEthhL7y4vLBQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:44 Document attached:
 - id                   5309cc045ac3435d8a9619fad270fcaa
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/a9c0b427805b4320a3959e5e360486b9?Signature=rrZy5fhkUnM7IAbtM6XKJkQZ9xWPXJ81rpDhJNfPxcLYtFgF2%2F%2FXuR%2BnnL8an3GfgUnk%2BbmmFi0ivrg4LRwcDQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:44 Document attached:
 - id                   2934a3ada43149c48bc8e41b6b0574d3
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/f2077b91aef8455fb7eb0a794df64732?Signature=T1fD4%2BgKDCkh8hDj2%2BBcAQ%2FNwsrvR9GTtjm3gEYXBDQ0fS6%2BykGWEmJXb2UH8B71oQPmi1L6Pm25WGM1u5g%2BAQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

03:39:44 Bid created:
 - id                   736408bbea3745c4aa7f317888c45b2f
 - token                5a3feabbde194e8cabd83b55ca63e3d3
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
