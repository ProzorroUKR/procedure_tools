# procedure_tools

## Install

Clone and install with pip
```
cd procedure_tools

pip install -e .
```

## Usage
```
usage: procedure [-h] [-a 460800] [-p /api/0/] [-d aboveThresholdUA]
                 [-s tender_create.json] [-w edr-qualification]
                 host token

positional arguments:
  host                  api host
  token                 api token

optional arguments:
  -h, --help            show this help message and exit
  -a 460800, --acceleration 460800
                        acceleration multiplier
  -p /api/0/, --path /api/0/
                        api path
  -d aboveThresholdUA, --data aboveThresholdUA
                        data files path custom or one of
                        ['competitiveDialogueUA', 'reporting',
                        'belowThreshold', 'aboveThresholdUA',
                        'aboveThresholdEU.plan', 'closeFrameworkAgreementUA',
                        'belowThreshold.multilot', 'aboveThresholdEU.tender',
                        'negotiation.quick', 'esco',
                        'aboveThresholdUA.defense', 'competitiveDialogueEU',
                        'aboveThresholdEU.multilot', 'negotiation',
                        'aboveThresholdEU']
  -s tender_create.json, --stop tender_create.json
                        data file name to stop after
  -w edr-qualification, --wait edr-qualification
                        wait for event ('edr-qualification', 'edr-pre-
                        qualification') divided by comma)
```

## Usage example

Create with default data
```
procedure https://lb-api-sandbox.prozorro.gov.ua 59fcc88692e341a2a4a0c184db282e83 --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA
```

Create with default data and stop after specific data file
```
procedure https://lb-api-sandbox.prozorro.gov.ua 59fcc88692e341a2a4a0c184db282e83 --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA
```

Create with custom data files (relative path)
```
procedure https://lb-api-sandbox.prozorro.gov.ua 59fcc88692e341a2a4a0c184db282e83 --acceleration=1000000 --path=/api/0/ --data=customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path)
```
procedure https://lb-api-sandbox.prozorro.gov.ua 59fcc88692e341a2a4a0c184db282e83 --acceleration=1000000 --path=/api/0/ --data=/Users/JonhDoe/customdata/closeFrameworkAgreementUA
```

Create with custom data files (absolute path, Windows)
```
procedure https://lb-api-sandbox.prozorro.gov.ua 59fcc88692e341a2a4a0c184db282e83 --acceleration=1000000 --path=/api/0/ --data=C:\Users\JonhDoe\customdata\closeFrameworkAgreementUA
```

## Output example
```
procedure https://lb-api-sandbox.prozorro.gov.ua 59fcc88692e341a2a4a0c184db282e83 --acceleration=1000000 --path=/api/0/ --data=closeFrameworkAgreementUA --stop=bid_create_4.json
```
```
Creating plan...

Processing data file: plan_create.json

[POST] https://lb-api-sandbox.prozorro.gov.ua/api/0/plans

Plan created:
 - id 				f0fab9d5c79b4862b4fecfa84fbcf430
 - token 			38a4ff8f4a0b4ee192be1ab3d39af33f
 - transfer 			fb806f2190de49678dd9abc2c786b8c9

Creating tender...

Processing data file: tender_create.json

[POST] https://lb-api-sandbox.prozorro.gov.ua/api/0/plans/f0fab9d5c79b4862b4fecfa84fbcf430/tenders

Tender created:
 - id 				bd91b5965c3745819496a6034bbb92d8
 - token 			1690000f86754cd08b25a98ab81b111c
 - transfer 			2d509d46cc5841c8b5a64a31260a3592
 - status 			active.tendering
 - tenderID 			UA-2019-10-05-000068-a
 - procurementMethodType 	closeFrameworkAgreementUA

[GET] https://lb-api-sandbox.prozorro.gov.ua/api/0/tenders/bd91b5965c3745819496a6034bbb92d8

Creating bids...

Processing data file: bid_create_0.json

[POST] https://lb-api-sandbox.prozorro.gov.ua/api/0/tenders/bd91b5965c3745819496a6034bbb92d8/bids

Bid created:
 - id 				887f947c3c064334bffbbbf165dd95fa
 - token 			4e3c4abe45d34c62bdb6a2ba0e9ca7f0
 - status 			pending

Processing data file: bid_create_1.json

[POST] https://lb-api-sandbox.prozorro.gov.ua/api/0/tenders/bd91b5965c3745819496a6034bbb92d8/bids

Bid created:
 - id 				64de343271e84785bc92c50343aed0cd
 - token 			790cd090127e473fac1b9c9b035c4794
 - status 			pending

Processing data file: bid_create_2.json

[POST] https://lb-api-sandbox.prozorro.gov.ua/api/0/tenders/bd91b5965c3745819496a6034bbb92d8/bids

Bid created:
 - id 				47b708d4a74b42fd86f40a807bb7b399
 - token 			2563ba9859e845469f66ca98c2e09c6f
 - status 			pending

Processing data file: bid_create_3.json

[POST] https://lb-api-sandbox.prozorro.gov.ua/api/0/tenders/bd91b5965c3745819496a6034bbb92d8/bids

Bid created:
 - id 				f12f77cac15e4df294304803c7425acd
 - token 			b25ce62ec34e447eba6448972e55f63b
 - status 			pending

```

## Update readme

Pass API token as parameter to README.sh
```
./README.sh 59fcc88692e341a2a4a0c184db282e83
```

## Run tests

```
HOST=https://lb-api-sandbox.prozorro.gov.ua TOKEN=59fcc88692e341a2a4a0c184db282e83 python setup.py test
```
