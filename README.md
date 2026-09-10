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
usage: procedure [-h] [-v] [-a 460800] [-p /api/0/]
                 [-d aboveThresholdUA [aboveThresholdUA ...]] [--parallel [N]]
                 [-m quick(mode:no-auction)] [-s tender_create.json]
                 [--pause tender_create.json [tender_create.json ...]]
                 [-w edr-qualification [edr-qualification ...]] [-e SEED]
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
[18:12:29] Using seed 55654

[18:12:29] Initializing cdb client

[18:12:29] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/spore
[18:12:29] Response status: 200 OK

[18:12:29] Client time delta with server: -839 milliseconds

[18:12:29] Initializing ds client

[18:12:29] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/constants
[18:12:29] Response status: 200 OK

[18:12:29] Creating framework...

[18:12:29] Processing data file: framework_create.json

[18:12:29] Skipping...

[18:12:29] Creating plan...

[18:12:29] Processing data file: plan_create.json

[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.address`.
[18:12:29] Provider `faker.providers.address` has been localized to `uk_UA`.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.automotive`.
[18:12:29] Provider `faker.providers.automotive` has been localized to `uk_UA`.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.bank`.
[18:12:29] Provider `faker.providers.bank` has been localized to `uk_UA`.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.barcode`.
[18:12:29] Specified locale `uk_UA` is not available for provider `faker.providers.barcode`. Locale reset to `en_US` for this provider.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.color`.
[18:12:29] Provider `faker.providers.color` has been localized to `uk_UA`.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.company`.
[18:12:29] Specified locale `uk_UA` is not available for provider `faker.providers.company`. Locale reset to `en_US` for this provider.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.credit_card`.
[18:12:29] Provider `faker.providers.credit_card` has been localized to `uk_UA`.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.currency`.
[18:12:29] Specified locale `uk_UA` is not available for provider `faker.providers.currency`. Locale reset to `en_US` for this provider.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.date_time`.
[18:12:29] Specified locale `uk_UA` is not available for provider `faker.providers.date_time`. Locale reset to `en_US` for this provider.
[18:12:29] Provider `faker.providers.emoji` does not feature localization. Specified locale `uk_UA` is not utilized for this provider.
[18:12:29] Provider `faker.providers.file` does not feature localization. Specified locale `uk_UA` is not utilized for this provider.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.geo`.
[18:12:29] Specified locale `uk_UA` is not available for provider `faker.providers.geo`. Locale reset to `en_US` for this provider.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.internet`.
[18:12:29] Provider `faker.providers.internet` has been localized to `uk_UA`.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.isbn`.
[18:12:29] Specified locale `uk_UA` is not available for provider `faker.providers.isbn`. Locale reset to `en_US` for this provider.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.job`.
[18:12:29] Provider `faker.providers.job` has been localized to `uk_UA`.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.lorem`.
[18:12:29] Provider `faker.providers.lorem` has been localized to `uk_UA`.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.misc`.
[18:12:29] Specified locale `uk_UA` is not available for provider `faker.providers.misc`. Locale reset to `en_US` for this provider.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.passport`.
[18:12:29] Specified locale `uk_UA` is not available for provider `faker.providers.passport`. Locale reset to `en_US` for this provider.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.person`.
[18:12:29] Provider `faker.providers.person` has been localized to `uk_UA`.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.phone_number`.
[18:12:29] Provider `faker.providers.phone_number` has been localized to `uk_UA`.
[18:12:29] Provider `faker.providers.profile` does not feature localization. Specified locale `uk_UA` is not utilized for this provider.
[18:12:29] Provider `faker.providers.python` does not feature localization. Specified locale `uk_UA` is not utilized for this provider.
[18:12:29] Provider `faker.providers.sbn` does not feature localization. Specified locale `uk_UA` is not utilized for this provider.
[18:12:29] Looking for locale `uk_UA` in provider `faker.providers.ssn`.
[18:12:29] Provider `faker.providers.ssn` has been localized to `uk_UA`.
[18:12:29] Provider `faker.providers.user_agent` does not feature localization. Specified locale `uk_UA` is not utilized for this provider.
[18:12:29] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans
[18:12:30] Response status: 201 Created

[18:12:30] Plan created:
 - data.id              e612239f5c0c449cb9957eaa345e2786
 - access.token         f8344867dabf492d9c7e6dce784b5a8c
 - access.transfer      f9ec1165b75a4f9b8ecdcd699fed49dd
 - data.status          draft

[18:12:30] Patching plan...

[18:12:30] Processing data file: plan_patch.json

[18:12:30] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/e612239f5c0c449cb9957eaa345e2786?acc_token=f8344867dabf492d9c7e6dce784b5a8c
[18:12:30] Response status: 200 OK

[18:12:30] Plan patched:
 - data.id              e612239f5c0c449cb9957eaa345e2786
 - data.status          scheduled

[18:12:30] Creating tender...

[18:12:30] Processing data file: tender_create.json

[18:12:30] Looking for locale `en_US` in provider `faker.providers.address`.
[18:12:30] Provider `faker.providers.address` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.automotive`.
[18:12:30] Provider `faker.providers.automotive` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.bank`.
[18:12:30] Specified locale `en_US` is not available for provider `faker.providers.bank`. Locale reset to `en_GB` for this provider.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.barcode`.
[18:12:30] Provider `faker.providers.barcode` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.color`.
[18:12:30] Provider `faker.providers.color` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.company`.
[18:12:30] Provider `faker.providers.company` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.credit_card`.
[18:12:30] Provider `faker.providers.credit_card` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.currency`.
[18:12:30] Provider `faker.providers.currency` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.date_time`.
[18:12:30] Provider `faker.providers.date_time` has been localized to `en_US`.
[18:12:30] Provider `faker.providers.emoji` does not feature localization. Specified locale `en_US` is not utilized for this provider.
[18:12:30] Provider `faker.providers.file` does not feature localization. Specified locale `en_US` is not utilized for this provider.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.geo`.
[18:12:30] Provider `faker.providers.geo` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.internet`.
[18:12:30] Provider `faker.providers.internet` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.isbn`.
[18:12:30] Provider `faker.providers.isbn` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.job`.
[18:12:30] Provider `faker.providers.job` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.lorem`.
[18:12:30] Provider `faker.providers.lorem` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.misc`.
[18:12:30] Provider `faker.providers.misc` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.passport`.
[18:12:30] Provider `faker.providers.passport` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.person`.
[18:12:30] Provider `faker.providers.person` has been localized to `en_US`.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.phone_number`.
[18:12:30] Provider `faker.providers.phone_number` has been localized to `en_US`.
[18:12:30] Provider `faker.providers.profile` does not feature localization. Specified locale `en_US` is not utilized for this provider.
[18:12:30] Provider `faker.providers.python` does not feature localization. Specified locale `en_US` is not utilized for this provider.
[18:12:30] Provider `faker.providers.sbn` does not feature localization. Specified locale `en_US` is not utilized for this provider.
[18:12:30] Looking for locale `en_US` in provider `faker.providers.ssn`.
[18:12:30] Provider `faker.providers.ssn` has been localized to `en_US`.
[18:12:30] Provider `faker.providers.user_agent` does not feature localization. Specified locale `en_US` is not utilized for this provider.
[18:12:30] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/plans/e612239f5c0c449cb9957eaa345e2786/tenders
[18:12:30] Response status: 201 Created

[18:12:30] Tender created:
 - data.id              52ec4c3892234a6188864c538b1f3fce
 - access.token         63ca69daf1214ed29a19f8494eef7255
 - access.transfer      f13035713b5440adb9cbd03409b7d709
 - data.status          draft
 - data.tenderID        UA-2026-09-10-000173-a
 - data.procurementMethodType closeFrameworkAgreementUA

[18:12:30] GET https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/52ec4c3892234a6188864c538b1f3fce
[18:12:30] Response status: 200 OK

[18:12:30] Processing data file: tender_document_attach.json

[18:12:30] Processing data file: tender_document_file.txt

[18:12:30] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:30] Response status: 200 OK

[18:12:30] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/52ec4c3892234a6188864c538b1f3fce/documents?acc_token=63ca69daf1214ed29a19f8494eef7255
[18:12:30] Response status: 201 Created

[18:12:30] Document attached:
 - data.id              0775225db0bc4d4592f08925f606b64c
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/8e932296d74947cba7b774115464b0a6?Signature=V90oqJupc8dhJ2ubOlKnev018Ned3UAINo7oc6eoWG5c3rpbrKukdIPb5dF%2FlEdLZ78lik%2BbNC3KHMV4umcUCQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:30] Processing data file: contract_proforma_attach.json

[18:12:30] Processing data file: contract_proforma.txt

[18:12:30] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:31] Response status: 200 OK

[18:12:31] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/52ec4c3892234a6188864c538b1f3fce/documents?acc_token=63ca69daf1214ed29a19f8494eef7255
[18:12:31] Response status: 201 Created

[18:12:31] Document attached:
 - data.id              fbe8a676bdb042faac1f1255bc2a57ad
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/f8206684d5ce42bd968e637addcb72ca?Signature=3%2BEQxR%2BryklVpfj7uJOTJ71ZdFh0kCjd%2FLjZDf57WLll%2Bv7yCo5vY4XmHfLsrp4o7TrrnJdZB4fG%2FN75S0wnCw%3D%3D&KeyID=1331dc52
 - data.documentType    contractProforma
 - data.confidentiality public

[18:12:31] Create tender criteria...

[18:12:31] Processing data file: criteria_create.json

[18:12:31] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/52ec4c3892234a6188864c538b1f3fce/criteria?acc_token=63ca69daf1214ed29a19f8494eef7255
[18:12:31] Response status: 201 Created

[18:12:31] Tender criteria created:
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

[18:12:31] Processing data file: tender_notice_attach.json

[18:12:31] Processing data file: tender_notice_file.p7s

[18:12:31] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:31] Response status: 200 OK

[18:12:31] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/52ec4c3892234a6188864c538b1f3fce/documents?acc_token=63ca69daf1214ed29a19f8494eef7255
[18:12:31] Response status: 201 Created

[18:12:31] Document attached:
 - data.id              ce637505e59f45afa14ba0c765d09b71
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/705033241db247f381b3341cf2ffa06c?Signature=C3UjzT24D2qgkZB%2FFkJnuF8FqlpaqB0xYnPVF6tV9TVkle%2FR6ljKrUeeC5VWp2EP%2F8Qb3MpdpGT%2FiLyToXVtBQ%3D%3D&KeyID=1331dc52
 - data.documentType    notice
 - data.confidentiality public

[18:12:31] Patching tender...

[18:12:31] Processing data file: tender_patch.json

[18:12:31] PATCH https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/52ec4c3892234a6188864c538b1f3fce?acc_token=63ca69daf1214ed29a19f8494eef7255
[18:12:32] Response status: 200 OK

[18:12:32] Tender patched:
 - data.id              52ec4c3892234a6188864c538b1f3fce
 - data.status          active.tendering

[18:12:32] Skipping complaints creating: bot and reviewer tokens are required

[18:12:32] Creating bids...

[18:12:32] Processing data file: bid_create_0.json

[18:12:32] Processing data file: bid_document_file.txt

[18:12:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:32] Response status: 200 OK

[18:12:32] Processing data file: bid_confidential_document_file.txt

[18:12:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:32] Response status: 200 OK

[18:12:32] Processing data file: bid_eligibility_document_file.txt

[18:12:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:32] Response status: 200 OK

[18:12:32] Processing data file: bid_financial_document_file.txt

[18:12:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:32] Response status: 200 OK

[18:12:32] Processing data file: bid_qualification_document_file.txt

[18:12:32] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:32] Response status: 200 OK

[18:12:32] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/52ec4c3892234a6188864c538b1f3fce/bids
[18:12:33] Response status: 201 Created

[18:12:33] Document attached:
 - data.id              933c4de0e5b14c7c86c7ebb83c5eee1a
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/62ba07ef96304b11aa8837b6c563912f?Signature=PV4i8ggdOa7ZxTJv5%2BidYOtQH%2FOXlu8tIRwLYMleZaMqIihc2m%2FiGGjumEnJTWWcitrRt2aH%2BGfUDqURyhQ3Bw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:33] Document attached:
 - data.id              07bb2f616b234b1ba1c95c4a39e5ae7e
 - data.confidentiality buyerOnly

[18:12:33] Document attached:
 - data.id              b20759d1d04a4ec1ac877287cc12bc38
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/638b42d633d541b5a465c72027983d4c?Signature=Hc0R0QeBYK7hqrDIckbYNG%2Bj8F67FaHcN9fOjVd2M84m2NimGZkkB5xioLHQZW1bjm0XNbKlqzkQIV2mb9knDQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:33] Document attached:
 - data.id              9c10afdd62034a72aa7c667b2c3bcf2e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/538590d9f5dd4b9dbf67c8a266a21145?Signature=IqYt2GzZFLQU69sqe8YsO0aXRITD4VTyMdNagxMzVild%2BJIGlmYB6JU%2BOkLc3O%2FRcNEnof2xQnvN%2B04zCNZECw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:33] Document attached:
 - data.id              a69b1578e48e4b0da7c8b5bca08b6ade
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/4985a09d6477409f986ba116d6002cc8?Signature=Zjq41C6d4aphqY6thUauZHUdbL4z3c3b%2B%2BRU47gkBM1ZrkKZI0MOQC7hCs1DaLjb3DkRvzN6h3Km7z%2B%2FdGkuBw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:33] Bid created:
 - data.id              e944fc6b489e46cabb306fc6449d20ad
 - access.token         160bd38c9e8449a49f1ab34999bfcdfc
 - data.status          draft

[18:12:33] Processing data file: bid_create_1.json

[18:12:33] Processing data file: bid_document_file.txt

[18:12:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:33] Response status: 200 OK

[18:12:33] Processing data file: bid_confidential_document_file.txt

[18:12:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:33] Response status: 200 OK

[18:12:33] Processing data file: bid_eligibility_document_file.txt

[18:12:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:33] Response status: 200 OK

[18:12:33] Processing data file: bid_financial_document_file.txt

[18:12:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:33] Response status: 200 OK

[18:12:33] Processing data file: bid_qualification_document_file.txt

[18:12:33] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:34] Response status: 200 OK

[18:12:34] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/52ec4c3892234a6188864c538b1f3fce/bids
[18:12:34] Response status: 201 Created

[18:12:34] Document attached:
 - data.id              d9ec77df23174591afd3c24f112ebdba
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/9c3be9d657a94b04a8e1a39915c8ad43?Signature=G1%2B2ANc4uLwgjkUycHH9WaNYPlsLbp8fYgIBE7pfDcfchj8PaeWXuTcmegje3Ms44p%2BXLt%2BuEvUvX%2Fl9%2F3sACg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:34] Document attached:
 - data.id              2d40af94470f48359101068bfa6f6cae
 - data.confidentiality buyerOnly

[18:12:34] Document attached:
 - data.id              f7a9f652856d414381a3fb5e7363e8ca
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/f4519c16e524450bb0c9ebf1b5fe5bb1?Signature=rB9iT0SkkH7iz2hlCUckNNSc20P72jPvWeK41JWv5UqdFCUB4KpIMaPH%2FwFjEw7IRWQNzJoaHno%2FezhVlEsnDw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:34] Document attached:
 - data.id              9e61d1807859469496217c1f3ae7ce47
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/26cc8891bf894a70b597862e460d4698?Signature=rwRDxC%2BkRZjzgX5uJ3yjvHNlw3VFs1LvgMZj9%2FFJJF3z0Ii9yYOL3jFhTewdwJuqQ64DnfBY9oaDckoj1g8OAQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:34] Document attached:
 - data.id              f80b6b8235d8413594865942083e20b9
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/d8049239cba14196b057c76a1eca98fa?Signature=XKyHjgBBPX8u1tSqCyiEPSuYiLP8qcjgMGscyIMATrcBr3%2BU1ocS61aaagFrscxCV7%2BHAuZC%2B2g84alXIo%2FJDg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:34] Bid created:
 - data.id              498a853d4914421f82e3058043a78734
 - access.token         724e6255c82749da855e16c6e453b64b
 - data.status          draft

[18:12:34] Processing data file: bid_create_2.json

[18:12:34] Processing data file: bid_document_file.txt

[18:12:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:34] Response status: 200 OK

[18:12:34] Processing data file: bid_confidential_document_file.txt

[18:12:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:34] Response status: 200 OK

[18:12:34] Processing data file: bid_eligibility_document_file.txt

[18:12:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:34] Response status: 200 OK

[18:12:34] Processing data file: bid_financial_document_file.txt

[18:12:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:34] Response status: 200 OK

[18:12:34] Processing data file: bid_qualification_document_file.txt

[18:12:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:34] Response status: 200 OK

[18:12:34] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/52ec4c3892234a6188864c538b1f3fce/bids
[18:12:34] Response status: 201 Created

[18:12:34] Document attached:
 - data.id              bd1a7d32c96a42c0901f6bf5f1e3a63e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/a2af76004c31493ea4a5473b6a9e8bf7?Signature=hAvuXpW2YzzydyWcrKHGnXjB0pOgNN%2BCmv8UhNhlxbm4pnIvewrPkZ4tXLfiSkibaYtTAcK%2BhrtOT15uUSUGDQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:34] Document attached:
 - data.id              e7b1b9e9a2094f37b7b716f6962cc12a
 - data.confidentiality buyerOnly

[18:12:34] Document attached:
 - data.id              cef75d59022e4fd993c385061b2e7926
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/129182ab5e2342c38071f54a119c29fb?Signature=%2FJaXMUjkggmMummyHZWDWq6CSkLSHl%2FIh1RDLVTpACyrpuzy9K4TBpv0As6%2F0ozcq%2FG99ywvN4LMFmOiyVAVDw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:34] Document attached:
 - data.id              9b0e4e74a38d4b1bbe875260ffbdec5d
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/1040b5564b27433083d83e05faf7ee44?Signature=6aHPgOmuS3msJxwrmLnfhTLoDhpq63l3dER4Hxx4%2Flk1T8x7w69ZJtNy%2FMNGrROeGbljZHUif8TqDsEo46dnDQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:34] Document attached:
 - data.id              9391281cc8ba4016921e728a0386858b
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/aa3a008eb4294b448f808520b7449c0a?Signature=gAghlR1wyw5Z%2FHGAxbcsl%2FdNQOV5vOxYgQVItqVNBPHCN%2FDNw%2F%2Fqu9w%2FxUlnYED2zQZPZQt4bku6wJhUovd%2BCQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:34] Bid created:
 - data.id              62f8c8bf23814c52afccca164d957af6
 - access.token         529ea0d9bb714dac8a6b029e9ca7adf6
 - data.status          draft

[18:12:34] Processing data file: bid_create_3.json

[18:12:34] Processing data file: bid_document_file.txt

[18:12:34] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:35] Response status: 200 OK

[18:12:35] Processing data file: bid_confidential_document_file.txt

[18:12:35] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:35] Response status: 200 OK

[18:12:35] Processing data file: bid_eligibility_document_file.txt

[18:12:35] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:35] Response status: 200 OK

[18:12:35] Processing data file: bid_financial_document_file.txt

[18:12:35] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:35] Response status: 200 OK

[18:12:35] Processing data file: bid_qualification_document_file.txt

[18:12:35] POST https://upload-docs-sandbox-2.prozorro.gov.ua/upload
[18:12:35] Response status: 200 OK

[18:12:35] POST https://lb-api-sandbox-2.prozorro.gov.ua/api/0/tenders/52ec4c3892234a6188864c538b1f3fce/bids
[18:12:35] Response status: 201 Created

[18:12:35] Document attached:
 - data.id              4c6471b73a6c4ee683d99f41262db5f2
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/aaed15d55dc844f2b76da97875aea490?Signature=a8i3MIjjlKshwBe3OvK8I1cib6xV1XdohKV3lUIUgDit4mSRNLMwFl5rO9tpQTroRPyuqn4Gpe8fm5bihrZYBg%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:35] Document attached:
 - data.id              fec799d49c2643639290fc33b66953ca
 - data.confidentiality buyerOnly

[18:12:35] Document attached:
 - data.id              12c2c99de2444cf6b96b27936b92867e
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/aa286aeb52ac4d75a62729157e3b4bbb?Signature=9rkdHL5d67%2B5I0kmWmtCJBvrcSXQH3qerLvr05eCKIJjqZn20WkP7HqMXsmhbWoyybRDRFZ3WPfL0me6Q0JLCQ%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:35] Document attached:
 - data.id              b681bb722cf54e83aff0c5f2f17ebea3
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/32625c1007b14620afa9b8156ca3c5f8?Signature=b1aky5beC3mtMoz1RyQXL5ZqzQdqoOkOsXnU6XQ%2FrprzCll67dU6aZbmWyHKbq68z8qupRMyzLaNYL22bwhMDA%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:35] Document attached:
 - data.id              c81904ab28b145e5afbd7f00bdc3e54f
 - data.url             https://public-docs-sandbox-2.prozorro.gov.ua/get/0223d1f395804c0394424ae9b2d8c4db?Signature=KStIoz41qycRchzHHN0dWJduB%2BeIbXYSS5vChhC%2BeF9laxCq%2BIx%2FRHDqKQx1xzI0sDyz2Y2EDVGnprMvO6utCw%3D%3D&KeyID=1331dc52
 - data.confidentiality public

[18:12:35] Bid created:
 - data.id              4b94a3b2cd7542f481a89348c61eddeb
 - access.token         cf9bd9a358a24011815705456004e85e
 - data.status          draft

[18:12:35] Completed.

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
