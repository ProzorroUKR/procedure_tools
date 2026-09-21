# Robot tests

Robot Framework suites that drive real procedures against a CDB instance,
using the same actions as the `procedure-tools` command.

The difference to the command is where the payloads come from. The command
reads them from the JSON files of a data folder; here they are built in memory
by data keywords and handed straight to the action. Nothing is read from a
fixture, so a test states only what it is about - two lots, two bids, no
auction - and the defaults fill in the rest.

## Language

The suites are written in Ukrainian, through Robot Framework's own Ukrainian
localization: every file opens with `language: uk` and uses the Ukrainian
section and setting names (`*** Налаштування ***`, `*** Тест-кейси ***`,
`*** Ключових слова ***`, `Документація`, `Ресурс`, `Налаштування Suite`,
`Розбірка Suite`, `Тестові теги`, `[Документація]`, `[Теги]`, `[Аргументи]`).
Those spellings come from `robot.conf.languages.Uk` and are what Robot
recognises, so they are used exactly as it defines them, awkward ones
included.

The keywords this project owns are Ukrainian too, and their wording is taken
from the Ukrainian source of the API documentation (`docs/source` in
openprocurement.api): закупівля (tender), пропозиція (bid), визначення
переможця / переможець (award), вимога (claim), скарга (complaint), звернення
(question), замовник (procuringEntity), покупці (buyers), постачальник
(supplier), учасник (tenderer), договір (contract), лот (lot), предмет
закупівлі (items), етап (milestone), орган оскарження (the reviewers),
критерій визначення переможця (awardCriteria), нецінові критерії (features),
критерії прийнятності (eligible), кваліфікаційні критерії (selection criteria).
`TESTING.md` has the full table with the sentence each term is taken from.

Four things stay in English, because they are names in the system rather than
prose:

- **Variables** - `${tender}`, `${data}`, `${TENDER}`, `${CRITERIA}`.
- **Keyword arguments** - `index=0`, `lots=3`, `folder=aboveThreshold.lcc`;
  they mirror the Python parameter names.
- **Tags** - `smoke`, `negative`, `procedure:aboveThreshold`, `phase:tendering`;
  CI selects on them and the directory conventions are checked against them.
- **BuiltIn keywords and expected API messages** - `Should Be Equal`,
  `Run Keyword And Expect Error`, and the error text a refusal is matched
  against. Robot does not localize its own keywords, and the API answers in
  English.

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

Without Docker, with the package and Robot Framework installed
(`pip install -e .[test,robot]`):

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
PROCEDURE_ENV=.env.dev robot tests
```

Run it from `robot_tests`, not from the repository root. The env file is looked
up in the working directory first, and the root holds an `.env.dev` of its own -
the one the `procedure-tools` command uses, which sets `DISABLE_QUESTIONS`,
`DISABLE_CLAIMS` and `DISABLE_COMPLAINTS`. A run started from there silently
skips every question, claim and complaint step.

`REVIEWER_TOKEN` and `BOT_TOKEN` are what the complaint suites act with. A run
without them does not fail: the suites that need them skip, saying so.

`ACCELERATION` decides how much of a procedure is waiting, and it can be set
too high. The tendering period is forty days of API time, so at 460800 it is
seven seconds - less than a suite needs to publish its criteria and submit a
bid, and the API then refuses the bid as out of period. Around 20000 the window
is about three minutes, which is comfortable; that is a good place to start.

Run one suite, one test, or one tag:

```shell
robot tests/procedures/reporting
robot tests/procedures/aboveThreshold/complete.robot
robot --test "Відзвітувати Про Закупівлю" tests
robot --include smoke tests
```

The refusals of a procedure live in its own directory, so they are run with it
or on their own:

```shell
robot --suite Negative tests/procedures
robot tests/procedures/aboveThreshold/negative
robot --include negative tests
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
├── tests/
│   ├── procedures/             one directory per procedure, one file per branch
│   └── config/                 one file per config option, tender and framework
├── resources/
│   ├── procedure.resource      session, run settings, the phases
│   └── phases/                 tendering, qualification, contracting
└── libraries/
    ├── ProcedureTools.py       action keywords
    ├── ProcedureData.py        data keywords
    ├── data/                   the data modules behind them
    └── tests/                  unit tests over the data modules
```

A suite is one scenario and its tests are the phases of that procedure, so a
red run says which phase broke; the phases after it are skipped rather than
failing for the same reason. [TESTING.md](TESTING.md) explains why.

## Action keywords

`ProcedureTools` wraps the `procedure_tools` actions one by one. A keyword
hands the action the payload it was given and returns what the action put into
the shared context, so a test reads as a sequence of API calls:

```robotframework
${tender}=      Створити Закупівлю    ${tender_data}
${criteria}=    Опублікувати Критерії Закупівлі    ${criteria_data}
${bid}=         Створити Пропозицію    ${bid_data}    index=0
Дочекатись Статусу Закупівлі    active.qualification    fail_status=unsuccessful
```

The context is the same one the CLI uses: it holds the tender, its token, the
bids, awards and contracts, and the actions keep it up to date. `Отримати
Значення Контексту` reaches anything that has no keyword of its own, and
`Виконати Дію Процедури` reaches an action that has no wrapper yet:

```robotframework
Виконати Дію Процедури    tender_question_create    ${question}    0
```

`Запустити Сесію Процедури` connects, `Скинути Стан Процедури` forgets the
procedure between tests while keeping the connection, and `Зупинити Сесію
Процедури` closes it and removes the generated document files.

## Data keywords

`ProcedureData` builds the payloads. The keywords are modular: each composes
the smaller ones and takes what it composes as an argument, so a test replaces
one piece without restating the rest.

```robotframework
${lots}=      Дані Лотів        2    amount=${5000}
${items}=     Дані Позицій      count=3    lots=${lots}
${tender}=    Дані Закупівлі    lots=${lots}    items=${items}
```

Every keyword also takes dotted overrides, applied last:

```robotframework
${tender}=    Дані Закупівлі     value.amount=200000    items.0.quantity=5
${bid}=       Дані Пропозиції    ${tender}    lotValues.0.value.amount=1999
```

Documents carry their own file content; the keyword that uploads them writes
it to a temporary file, so there is no fixture directory to keep in sync:

```robotframework
${proposal}=    Дані Документа    title=bid_0_proposal.txt
${notice}=      Дані Файлу Підпису
```

Criteria and the bid answers to them are the one place where the data has to
agree with the API. `Дані Критеріїв` builds the criteria with fresh requirement
ids, and `Дані Відповідей На Вимоги` derives the answers from the criteria the
API returned, so the ids always match:

```robotframework
${criteria}=     Опублікувати Критерії Закупівлі    ${{ $data }}
${responses}=    Дані Відповідей На Вимоги    ${criteria}    document_title=bid_0_proposal.txt
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

## Unit tests

The data builders are covered by plain pytest, no network and no test data
created:

```shell
pytest robot_tests/libraries/tests/
```

Run these before a live run: most of what breaks a suite is a payload the API
refuses, and that is visible here in under a second.

## Adding a procedure

How to decide what to write, where it belongs and what it should assert is in
[TESTING.md](TESTING.md). The steps below are the mechanics.

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
