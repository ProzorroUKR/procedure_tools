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
[23:56:53] Using seed 482913

[23:56:53] Initializing cdb client

[23:56:53] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[23:56:53] Starting new HTTPS connection (1): lb-api-sandbox-2.prozorro.gov.ua:443
[23:56:54] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/spore HTTP/11" 200 1128850
[23:56:54] Response status code: 200

[23:56:54] Client time delta with server: -244 milliseconds

[23:56:54] Initializing ds client

[23:56:54] Creating framework...

[23:56:54] Processing data file: framework_create.json

[23:56:54] Skipping...

[23:56:54] Creating plan...

[23:56:54] Processing data file: plan_create.json

[23:56:54] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[23:56:54] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans HTTP/11" 201 4202
[23:56:54] Response status code: 201

[23:56:54] Plan created:
 - id                   f6b6b62d38414b84af4654720465b85c
 - token                204221397aad4ef48a5e39801bce92de
 - transfer             f6b71b6c193a44db83bcf259e2f956d1
 - status               draft

[23:56:54] Patching plan...

[23:56:54] Processing data file: plan_patch.json

[23:56:54] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/f6b6b62d38414b84af4654720465b85c?acc_token=204221397aad4ef48a5e39801bce92de
[23:56:54] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/plans/f6b6b62d38414b84af4654720465b85c?acc_token=204221397aad4ef48a5e39801bce92de HTTP/11" 200 4101
[23:56:54] Response status code: 200

[23:56:54] Plan patched:
 - id                   f6b6b62d38414b84af4654720465b85c
 - status               scheduled

[23:56:54] Creating tender...

[23:56:54] Processing data file: tender_create.json

[23:56:54] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/f6b6b62d38414b84af4654720465b85c/tenders
[23:56:54] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/plans/f6b6b62d38414b84af4654720465b85c/tenders HTTP/11" 201 7452
[23:56:54] Response status code: 201

[23:56:54] Tender created:
 - id                   009da69202c846a6ba6a2d5a83be03bd
 - token                725955fb17b5448d9eabd7f8f2026fa2
 - transfer             65d6d022fb7b4f15b1bbea95b0e25cb7
 - status               draft
 - tenderID             UA-2025-10-21-000390-a
 - procurementMethodType closeFrameworkAgreementUA

[23:56:54] [GET] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/009da69202c846a6ba6a2d5a83be03bd
[23:56:54] https://lb-api-sandbox-2.prozorro.gov.ua:443 "GET /api/0/tenders/009da69202c846a6ba6a2d5a83be03bd HTTP/11" 200 7347
[23:56:54] Response status code: 200

[23:56:54] Processing data file: tender_document_attach.json

[23:56:54] Processing data file: tender_document_file.txt

[23:56:54] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:54] Starting new HTTPS connection (1): upload-docs-sandbox-2.prozorro.gov.ua:443
[23:56:57] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 576
[23:56:57] Response status code: 200

[23:56:57] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/documents?acc_token=725955fb17b5448d9eabd7f8f2026fa2
[23:56:57] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/documents?acc_token=725955fb17b5448d9eabd7f8f2026fa2 HTTP/11" 201 576
[23:56:57] Response status code: 201

[23:56:57] Document attached:
 - id                   cea7f3521b6b4f0796fc346f562885eb
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/0658277ec5c24539924813253cd9dd3c?Signature=k9T4ctW6qk1mAA8GmssGPnEmkrkdFDZq7QF%2FI2bh4CExljXwrKksN77kpicLaNYErGV0XnaOjMPAUq4YcvgVBQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:56:57] Create tender criteria...

[23:56:57] Processing data file: criteria_create.json

[23:56:57] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/criteria?acc_token=725955fb17b5448d9eabd7f8f2026fa2
[23:56:57] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/criteria?acc_token=725955fb17b5448d9eabd7f8f2026fa2 HTTP/11" 201 93928
[23:56:57] Response status code: 201

[23:56:57] Tender criteria created:
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

[23:56:57] Processing data file: tender_notice_attach.json

[23:56:57] Processing data file: tender_notice_file.p7s

[23:56:57] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:57] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 590
[23:56:57] Response status code: 200

[23:56:57] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/documents?acc_token=725955fb17b5448d9eabd7f8f2026fa2
[23:56:57] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/documents?acc_token=725955fb17b5448d9eabd7f8f2026fa2 HTTP/11" 201 604
[23:56:57] Response status code: 201

[23:56:57] Document attached:
 - id                   2193206ad1314ffc9fc9f80f87e42282
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/c360b465f27d4566abd114737010f2c5?Signature=Z9k%2FoZuja2rndfGS29y%2FBtuJ7VkHSekUqmpv4bM0zPZbb09DOGr25j4NiGPAEfCAxjVBQ68TtUgLUT2sF%2FasAA%3D%3D&KeyID=1331dc52
 - documentType         notice
 - confidentiality      public

[23:56:57] Patching tender...

[23:56:57] Processing data file: tender_patch.json

[23:56:57] [PATCH] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/009da69202c846a6ba6a2d5a83be03bd?acc_token=725955fb17b5448d9eabd7f8f2026fa2
[23:56:57] https://lb-api-sandbox-2.prozorro.gov.ua:443 "PATCH /api/0/tenders/009da69202c846a6ba6a2d5a83be03bd?acc_token=725955fb17b5448d9eabd7f8f2026fa2 HTTP/11" 200 102575
[23:56:57] Response status code: 200

[23:56:57] Tender patched:
 - id                   009da69202c846a6ba6a2d5a83be03bd
 - status               active.tendering

[23:56:57] Skipping complaints creating: bot and reviewer tokens are required

[23:56:57] Creating bids...

[23:56:57] Processing data file: bid_create_0.json

[23:56:57] Processing data file: bid_document_file.txt

[23:56:57] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:58] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 577
[23:56:58] Response status code: 200

[23:56:58] Processing data file: bid_confidential_document_file.txt

[23:56:58] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:58] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 584
[23:56:58] Response status code: 200

[23:56:58] Processing data file: bid_eligibility_document_file.txt

[23:56:58] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:58] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 587
[23:56:58] Response status code: 200

[23:56:58] Processing data file: bid_financial_document_file.txt

[23:56:58] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:58] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 587
[23:56:58] Response status code: 200

[23:56:58] Processing data file: bid_qualification_document_file.txt

[23:56:58] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:58] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 597
[23:56:58] Response status code: 200

[23:56:58] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/bids
[23:56:59] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/bids HTTP/11" 201 5131
[23:56:59] Response status code: 201

[23:56:59] Document attached:
 - id                   05faa87952624603becacf3415477854
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/7978ae3b8e6640bd8731d6fb0de2d666?Signature=vnK9X%2FI%2FhmNZzKph3Mr8iKjFQqtHRctHnUx4J6fV3OK8W67xm81c4r4gMqU%2FCgNwSU3Dab1DvhPsIBh1P%2BY%2BDw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:56:59] Document attached:
 - id                   8d2767f433af490092401fbe89728756
 - confidentiality      buyerOnly

[23:56:59] Document attached:
 - id                   32d90e6173614d09b2bb75d4b1b6dc7d
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/40c26d7d67414116b9c061f02d4883fe?Signature=bpJ%2FAMwgejtwiYHA0RDPjynXJB%2FC4GKHoyCwHnUPKjiCY0U%2BVUQM9y8jtrzu2eAHKyhK%2FdWuHKYlwP6O2SrHBg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:56:59] Document attached:
 - id                   f94918fd9ef342d3b6fd65c4ead4277e
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/337efed9c1a7416a8e66562e879b9732?Signature=vgA07Izyeo6b%2FWJ%2BtJ4Dna83z0ufoZoo%2FQNQJgKGwW65cuYmMitoLkihTump7cO3C0NrU%2FEYw%2FsxRoHapRtmBA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:56:59] Document attached:
 - id                   827b6b6db40045bda0c6683ac622bc4d
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/0f6d5ee55a7d40a19e1901d4ac3c0b63?Signature=mediQwgqyh30SkE%2BcZrAMlvtcVsGBlhVpGBZytqugryeaNSv1o0rvoVeHjXRDFbXfeniqrsEYETaR60EsCPwCQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:56:59] Bid created:
 - id                   0110b2dbbf464b419a5a8969307abf80
 - token                70b1ad70c36740fc9e36087d0ab4f4ed
 - status               draft

[23:56:59] Processing data file: bid_create_1.json

[23:56:59] Processing data file: bid_document_file.txt

[23:56:59] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:59] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 579
[23:56:59] Response status code: 200

[23:56:59] Processing data file: bid_confidential_document_file.txt

[23:56:59] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:59] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 600
[23:56:59] Response status code: 200

[23:56:59] Processing data file: bid_eligibility_document_file.txt

[23:56:59] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:59] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 599
[23:56:59] Response status code: 200

[23:56:59] Processing data file: bid_financial_document_file.txt

[23:56:59] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:59] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 589
[23:56:59] Response status code: 200

[23:56:59] Processing data file: bid_qualification_document_file.txt

[23:56:59] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:59] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 599
[23:56:59] Response status code: 200

[23:56:59] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/bids
[23:56:59] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/bids HTTP/11" 201 5224
[23:56:59] Response status code: 201

[23:56:59] Document attached:
 - id                   a486740eee4b42b0b9eadc71789dc9e5
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/f6714d111ace441ab852473af49872ea?Signature=7NwiBZ6JeSRS%2BNdelYxWfABZh15vv7WNWQwvB5O2n0EA5zNc%2BBjvwAIdpQsrGifPL7b6Vb%2BLHjtmFy4zRkFIDQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:56:59] Document attached:
 - id                   2b175b1b2ba9439486955fbaa04917b4
 - confidentiality      buyerOnly

[23:56:59] Document attached:
 - id                   439821447b47472c9a3a33304e9f94ca
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/5b03df28d7fe444893ec46bbab0196a8?Signature=Ge3wFMFCjOmWnutL7tjKOOD9138t6bdybCuqog1%2BCA%2BR96GhTlKDOJ10C9CVjeqJaX%2BZ6FaRatxU9nLSmJ7JBg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:56:59] Document attached:
 - id                   d4d0b47d9cf044fa9629f175d3130af3
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/2c64f8d8d25148caaebc031db30b93e2?Signature=KeXjgp6IupLGymUsQ03MfEFCe1%2FL%2Bm5m0nWmqPC296d%2BooPlk9w%2Ft1Fj6Np81TzvZ9fMeIqtR6c0LLkSqbsXCA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:56:59] Document attached:
 - id                   540acb6b8ab6419bb01f0238e3137073
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/642f56cf1c3d46cabefcdfb1c92fd216?Signature=HonnjHmfnV4AtbzyO2qZsn3QZOHzQanEcr3gC2wr5dMxw8dqV2faalNERZ57eLoNLrI8%2FcLgw9qInZPHqqHnAA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:56:59] Bid created:
 - id                   a6ce0f92fc424d31a5e4774ec26cce5f
 - token                990a858766e94a779d30249a1e6b5b1c
 - status               draft

[23:56:59] Processing data file: bid_create_2.json

[23:56:59] Processing data file: bid_document_file.txt

[23:56:59] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:59] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 577
[23:56:59] Response status code: 200

[23:56:59] Processing data file: bid_confidential_document_file.txt

[23:56:59] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:56:59] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 594
[23:56:59] Response status code: 200

[23:56:59] Processing data file: bid_eligibility_document_file.txt

[23:56:59] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:57:00] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 607
[23:57:00] Response status code: 200

[23:57:00] Processing data file: bid_financial_document_file.txt

[23:57:00] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:57:00] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 587
[23:57:00] Response status code: 200

[23:57:00] Processing data file: bid_qualification_document_file.txt

[23:57:00] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:57:00] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 609
[23:57:00] Response status code: 200

[23:57:00] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/bids
[23:57:00] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/bids HTTP/11" 201 5220
[23:57:00] Response status code: 201

[23:57:00] Document attached:
 - id                   40fde82ec4eb4fafae68a570dcc575c6
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/910dc9fe867b466d8d1fbc49d421e5d0?Signature=Sluc5tAV7anmnln4gsQvvS7fsIlJ3Bob%2FbhJ3hNes5ijABvO5aq9ycNfMF2Bf4F%2Byp5UxRepSAUV5kVKYUxpBw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:57:00] Document attached:
 - id                   d379c7df65a548d7a6ea9269343f4438
 - confidentiality      buyerOnly

[23:57:00] Document attached:
 - id                   9b42300186634bee8d2709582d36808a
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/3d6bd798891948d580b70618a180f7a9?Signature=mZ1uhIEbWt7MazfK0BAfXVni2W2DQLjxrl%2F7Q2X%2BO4DowOJ07qN9Tmw38U6CeriWtDDOBTJkO9XA0cJwrrSUAQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:57:00] Document attached:
 - id                   d5056090d8b44932bb6d22f29ddeddd9
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/afda66b0a487471892af49d8cd0b1cc1?Signature=FW9cBg2IFr%2BHBZfcrlL4b2JhDIXpTigHb6YSqu9sqGUlMGOO54BkSKeV%2F5Dj4ES0J3su4adov1HTkU9UXV2rCQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:57:00] Document attached:
 - id                   87335a612b1c4535afa251583be07deb
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/a78eb8d78459472aa8acdf46ff53e759?Signature=qcIQ9dKoQbH%2F8o0lv2AVXzkbdDrp2y4cT%2Bn79ZS%2FGHoPBWBZpRoEi76Pn44nUfQDG7YsqXaPWdVEmACThK66Dg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:57:00] Bid created:
 - id                   c232bfaba7884a508c6b629570f9d482
 - token                f83451ac70f94a7f9a4aec6e104bdb41
 - status               draft

[23:57:00] Processing data file: bid_create_3.json

[23:57:00] Processing data file: bid_document_file.txt

[23:57:00] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:57:00] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 597
[23:57:00] Response status code: 200

[23:57:00] Processing data file: bid_confidential_document_file.txt

[23:57:00] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:57:00] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 606
[23:57:00] Response status code: 200

[23:57:00] Processing data file: bid_eligibility_document_file.txt

[23:57:00] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:57:00] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 607
[23:57:00] Response status code: 200

[23:57:00] Processing data file: bid_financial_document_file.txt

[23:57:00] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:57:00] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 595
[23:57:00] Response status code: 200

[23:57:00] Processing data file: bid_qualification_document_file.txt

[23:57:00] [POST] https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[23:57:00] https://upload-docs-sandbox-2.prozorro.gov.ua:443 "POST /upload HTTP/11" 200 585
[23:57:00] Response status code: 200

[23:57:00] [POST] https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/bids
[23:57:01] https://lb-api-sandbox-2.prozorro.gov.ua:443 "POST /api/0/tenders/009da69202c846a6ba6a2d5a83be03bd/bids HTTP/11" 201 5228
[23:57:01] Response status code: 201

[23:57:01] Document attached:
 - id                   302ee6a980c0491691591964837aca99
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/2976f6db07014d49921ab4c2c25af005?Signature=3L3F%2FS66gpXtX2TlM6Xi9Y%2FfxjFXp1fuZm%2BJmmuHaUDLC8IXDLI%2BYwAdUXFBWXdQ%2BSrRHm9jKPOoiNMa7kxFDQ%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:57:01] Document attached:
 - id                   1b817590a4ae4b38a3d48ea26774146a
 - confidentiality      buyerOnly

[23:57:01] Document attached:
 - id                   abcd8bf88963474892ad31add0768a2a
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/29072ed09d7447b6b901555d91be1397?Signature=gFYf6oFdfPJWhbIAIzN4PWuUhfHXjERRJr9%2BugrQAy%2BmrFisLD4wRpP%2Ffyegfo8uybBY51R%2FtmskYwI1NILRCg%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:57:01] Document attached:
 - id                   5f5328ffd43346fc9c55e77fe66f0517
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/da0e6923ad1b4c1993961239476d3027?Signature=jccxckSLAJyK%2FnxObHNKG4g2ZpOE2Lvqk2XAJWR%2BMP3nuI2mXcgGAfYnUF5D4SSmmGLd7yNJ%2FQBMv4Hn9LUgCw%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:57:01] Document attached:
 - id                   292888f070bd4ea9909c3bbc5b764799
 - url                  https://public-docs-sandbox-2.prozorro.gov.ua/get/1197b1573092415d809df07fbd1f8c76?Signature=V6r09Uo7MrCb5l0qECGCfc5Td42P9YGoXp9R8LMjEu7Q27S9mDIY8WpqjFLCrDYA2%2FAImFgekRsreUxrPHQKCA%3D%3D&KeyID=1331dc52
 - confidentiality      public

[23:57:01] Bid created:
 - id                   db03cbdf92f248c2aabd929cd71287a7
 - token                d70d9afc29cf471ab0ee7e743ae47215
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
