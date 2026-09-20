# Robot tests

Robot Framework suites that drive real procedures against a CDB instance,
using the same actions as the `procedure-tools` command.

The difference to the command is where the payloads come from. The command
reads them from the JSON files of a data folder; here they are built in memory
by data keywords and handed straight to the action. Nothing is read from a
fixture, so a test states only what it is about - two lots, two bids, no
auction - and the defaults fill in the rest.

## Running

1. Copy `.env.example` to `.env` and fill in the broker credentials.
2. Run the suites:

   ```shell
   cd robot_tests
   docker compose up --build
   ```

3. The report lands in `robot_tests/reports/report.html`.

Pick what runs with `ROBOT_OPTIONS` in `.env`:

```env
ROBOT_OPTIONS=--include smoke            # the happy path of each procedure
ROBOT_OPTIONS=--include reporting        # one procedure
ROBOT_OPTIONS=--exclude auction          # skip what waits for an auction
ROBOT_OPTIONS=--loglevel DEBUG
```

## Running locally

Without Docker, with the package installed (`pip install -e .[test]`) plus
`robotframework`:

```shell
cd robot_tests
robot tests
```

The libraries are imported by path, so nothing has to be on `PYTHONPATH`.

The settings come from the environment under the same names the CLI uses
(`API_HOST`, `API_TOKEN`, `DS_HOST`, `DS_USERNAME`, `DS_PASSWORD`,
`ACCELERATION`, `SUBMISSION`), so one env file drives both. A local run reads
them from the shell, or from an env file named by `PROCEDURE_ENV`:

```shell
PROCEDURE_ENV=../.env.dev robot tests
```

Run one suite, one test, or one tag:

```shell
robot tests/reporting.robot
robot --test "Reporting Without A Plan" tests
robot --include smoke tests
```

## Watching a run

A run prints what it is doing - every request, its status and the ids that
came back - the same log the `procedure-tools` command prints:

```
Running tender_create
Creating tender...
POST http://api.../tenders
Response status: 201 Created
Tender created:
 - data.id              49e08359e573463f9966c13dfd7dfd69
 - data.status          draft
```

Robot files whatever a library prints into `log.html`, which is why a suite
otherwise shows nothing but one dot per keyword, so the session mirrors its
log past that capture. Turn it off for a quiet console:

```shell
ROBOT_CONSOLE_LOG=false robot tests
```

`log.html` has the full log either way, and `--consolemarkers off` drops the
dots Robot prints per keyword.

For request and response bodies, the CLI debug switches work here too:

```shell
DEBUG_REQUEST=true DEBUG_JSON_LEVEL=2 robot tests
```

To keep a plain text trace of a run, including every keyword, use Robot's
debug file and follow it from another terminal:

```shell
robot -b debug.txt tests
tail -f debug.txt
```

## Layout

```
robot_tests/
├── tests/                      one suite per procedure
│   ├── aboveThreshold.robot
│   └── reporting.robot
├── resources/
│   └── procedure.resource      keywords more than one procedure needs
└── libraries/
    ├── ProcedureTools.py       action keywords
    ├── ProcedureData.py        data keywords
    └── data/                   the data modules behind them
```

## Action keywords

`ProcedureTools` wraps the `procedure_tools` actions one by one. A keyword
hands the action the payload it was given and returns what the action put into
the shared context, so a test reads as a sequence of API calls:

```robotframework
${tender}=    Create Tender    ${tender_data}
${criteria}=  Post Tender Criteria    ${criteria_data}
${bid}=       Create Bid       ${bid_data}    index=0
Wait Tender Status    active.qualification    fail_status=unsuccessful
```

The context is the same one the CLI uses: it holds the tender, its token, the
bids, awards and contracts, and the actions keep it up to date. `Get Context
Value` reaches anything that has no keyword of its own, and `Run Procedure
Action` reaches an action that has no wrapper yet:

```robotframework
Run Procedure Action    tender_question_create    ${question}    0
```

`Start Procedure Session` connects, `Reset Procedure State` forgets the
procedure between tests while keeping the connection, and `End Procedure
Session` closes it and removes the generated document files.

## Data keywords

`ProcedureData` builds the payloads. The keywords are modular: each composes
the smaller ones and takes what it composes as an argument, so a test replaces
one piece without restating the rest.

```robotframework
${lots}=      Lots Data      2    amount=${5000}
${items}=     Items Data     count=3    lots=${lots}
${tender}=    Tender Data    lots=${lots}    items=${items}
```

Every keyword also takes dotted overrides, applied last:

```robotframework
${tender}=    Tender Data    value.amount=200000    items.0.quantity=5
${bid}=       Bid Data       ${tender}    lotValues.0.value.amount=1999
```

Documents carry their own file content; the keyword that uploads them writes
it to a temporary file, so there is no fixture directory to keep in sync:

```robotframework
${proposal}=    Document Data    title=bid_0_proposal.txt
${notice}=      Signature Document Data
```

Criteria and the bid answers to them are the one place where the data has to
agree with the API. `Criteria Data` builds the criteria with fresh requirement
ids, and `Requirement Responses Data` derives the answers from the criteria the
API returned, so the ids always match:

```robotframework
${criteria}=     Post Tender Criteria    ${{ $data }}
${responses}=    Requirement Responses Data    ${criteria}    document_title=bid_0_proposal.txt
```

An answer satisfies its requirement by construction: a boolean answers what is
expected, a choice answers with an allowed value, a number answers with the
highest value it may take. Only the first requirement group of each criterion
is answered, and criteria the procuring entity answers are skipped. Evidences
go only to the criteria the bidder answers during tendering (``source:
tenderer``); the API rejects them for the ones the winner answers later.

The criterion shapes live in `libraries/data/criteria_templates.py`, lifted
from the CDB criteria catalogue. Regenerate them from the repository root after
a catalogue change:

```shell
python robot_tests/libraries/data/generate_criteria_templates.py
```

## Adding a procedure

1. Add the payload builders the procedure needs to `libraries/data/`, reusing
   `common.py` for the pieces that are not specific to it.
2. Expose them as keywords in `ProcedureData`.
3. Add wrappers to `ProcedureTools` for the actions that have none yet.
4. Write the suite in `tests/`, keeping the steps every procedure shares in
   `resources/procedure.resource`.

Check a new suite without calling the API:

```shell
PYTHONPATH=robot_tests/libraries robot --dryrun robot_tests/tests
```

## Docs

- Robot Framework user guide: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html
- BuiltIn keywords: https://robotframework.org/robotframework/latest/libraries/BuiltIn.html
- The actions behind the keywords: `procedure_tools/actions/`
