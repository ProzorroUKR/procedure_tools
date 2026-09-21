# How these tests are built

`ROBOT.md` says how to run the suites. This file says how to decide what to
write, where it goes and what it should check.

## What robot_tests is for

The CLI and the suites do overlapping things for different reasons, and keeping
the line between them clear is what stops one becoming a worse copy of the
other.

| | `procedure-tools -d <folder>` | `robot_tests` |
|---|---|---|
| Purpose | bring a procedure to a state, by hand | prove the procedure behaves |
| Used by | a person, interactively, then switching to manual requests | CI, unattended |
| Passes when | the API accepted every request | the API accepted every request **and** the result is what was expected |
| Flow shape | linear, fixed by the file names | branches on what the API returned |

So a suite that only walks a procedure end to end and asserts nothing is a
slower copy of the CLI. The reason to write it here is the assertions: that the
winner is the cheaper bidder, that there is one contract per lot, that a
forbidden transition is refused with the right error.

Read that as the acceptance test for a new suite: **if you removed every
assertion and nothing was lost, the suite belongs in a data folder instead.**

## Levels

Cheap checks first; each level only carries what the one below cannot.

1. **Unit** (`pytest`, no network) - the data builders. That a payload has the
   shape the API expects, that overrides land where they should, that the bid
   answers cover the criteria they were built from. Seconds, free, no test data
   created.
2. **Dry run** (`robot --dryrun`) - that every keyword resolves and every
   argument matches. Catches a rename before it costs a procedure run.
3. **Smoke** (live, minutes) - the shortest path through the few procedures
   that matter most. Runs on every change.
4. **Full** (live, long) - every procedure, every branch, every config. Runs on
   a schedule.

Most defects found so far - a rogue field in a payload, a stripped id, an
evidence sent in the wrong phase - are level 1 defects that were found at level
3, one per run. Anything that can be pushed down a level should be.

## Granularity: a test is a phase

A procedure is stateful: an award cannot be patched without a tender, bids and
an auction behind it. That rules out a test per action, and it makes a single
test per procedure coarse. The middle is a **phase**:

```
Publish The Tender        PASS   0:12
Зібрати Пропозиції        PASS   1:40
Run The Auction           FAIL   3:05
Кваліфікувати Переможців  SKIP
Sign The Contracts        SKIP
```

Four to six per procedure, named after what a person would call that part of
the procedure, so a red run says where it broke without opening the log.

Two rules make this work, and `procedure.resource` provides both:

- **Fail once, skip the rest.** `Remember A Failed Phase` as the test teardown
  and `Skip If An Earlier Phase Failed` as the test setup. One real failure
  produces one red row followed by skips, not a cascade of confusing ones.
- **Reset per suite, not per test.** `Відкрити Сесію Процедури` as the suite
  setup starts the procedure; the phases share it. A test setup that reset the
  state would break the chain.

State that later phases need is handed on with `Set Suite Variable` - the
tender and its criteria, typically.

What this deliberately does not do is make phases independently runnable.
`--test "Підписати Договори"` cannot work - the state is not there. Select
whole suites, not phases.

## Layout

One file is one **scenario**: `complete.robot` for what the procedure normally
does, and one file per branch off it. Branches differ in a small part of the
flow, so the shared part lives in reusable phase keywords and a new scenario
costs a few lines rather than a copy of everything.

```
tests/
  procedures/             one directory per procedure
    aboveThreshold/       complete.robot plus one file per branch
      negative/           what this procedure refuses
        creation            what a tender cannot be created with
        transitions         what cannot be done to a published tender
        bids                what a bid cannot offer
    reporting/            complete.robot plus one file per branch
      negative/
        creation            fields an open tender has and reporting does not
        transitions         stages a limited procedure does not pass through
        awards              the award rules a limited procedure keeps
        cancellation        calling a reporting tender off
  config/                 one directory per config option, see below
    tender/<option>/
    framework/<option>/
resources/
  libraries.resource      the library imports, by path
  phases/                 tendering, qualification, contracting
  procedure.resource      session, run settings, the skip cascade, the phases
libraries/
  ProcedureTools.py       action keywords
  ProcedureData.py        data keywords
  data/                   the builders behind them
  tests/                  unit tests over the builders
```

There is no `smoke/` directory: the shortest paths are marked with the `smoke`
tag instead, so a scenario can be both a smoke test and the canonical example
of its procedure without being written twice.

Every procedure directory holds a `negative/` of its own. What is refused is
part of what the procedure is - reporting refuses a `tenderPeriod` where an
open tender requires one, and activates an award without eligibility where an
open tender cannot - so the refusals belong beside the flows they are the other
side of, not in a heap of their own. A refusal that reads the same in two
procedures is written twice, once in each, because the two are free to diverge.

`negative/` earns its place by cost: dozens of validation checks against one
created tender, where a scenario spends minutes to make a handful of
assertions. It is the cheapest coverage available.

Three rules keep it honest.

**Say which procedure it is about.** The suite sits in that procedure's
directory and tags itself `procedure:<name>`, so a run filtered to one
procedure gets its refusals too.

**Name the reason.** `Run Keyword And Expect Error    *` passes on any failure,
including the wrong one, so every check matches the message the API actually
returns. The patterns are Robot globs, where `[` opens a character set - so a
message ending in a list of allowed values is matched up to the bracket and no
further.

**Check what the API does, not what its source says it should.** Several of the
refusals written from reading the code turned out not to happen: the
procuringEntity kind check is switched on by a date that has not come yet, a
lot's minimalStep currency is silently overwritten from the tender's rather
than refused, and a bid's item quantities are only compared with the tender's
when the bid is submitted, not when it is written. Each of those is now a test
of what really happens, with the reason in its documentation.

## Config coverage

Config is how the CDB actually branches, and what a procedure may put in its
config is decided by the JSON schemas in the **standards** library
(`data_model/schema/TenderConfig/*.json` and `FrameworkConfig/*.json`), not by
the API code. Read those before writing a config test.

Three things about them shape the tests:

- **Most keys are pinned.** A schema entry with a single `enum` value, or with
  `minimum == maximum`, is fixed for that procedure. Sending anything else is
  refused outright (`False is not one of [True]`). There is no behaviour to
  cover, only the refusal.
- **The same key is free in one procedure and pinned in another.**
  `hasAwardingOrder` may be chosen in `competitiveOrdering` and
  `requestForProposal`; in `aboveThreshold` it is pinned to true.
- **The same key defaults differently per procedure.** `hasAwardingOrder`
  defaults to true in `competitiveOrdering` and false in `requestForProposal`;
  `hasAuction` defaults to true in `aboveThreshold` and false in
  `competitiveOrdering.short`. A test that assumes one default is wrong
  somewhere else.

That makes the test space finite and countable: **49 (procedure, key) pairs**
across 25 procedures can vary at all. Everything else is pinned.

| Procedure | Keys it may choose |
|---|---|
| `competitiveOrdering` | 14 |
| `requestForProposal` | 11 |
| `competitiveOrdering.long`, `competitiveOrdering.short` | 6 each |
| `aboveThreshold`, `belowThreshold` | 2 (`hasAuction`, `hasValueRestriction`) |
| `aboveThresholdEU`, `aboveThresholdUA`, `aboveThresholdUA.defense`, `simple.defense` | 1 (`hasAuction`) |
| `priceQuotation` | 1 (`restricted`) |
| `dynamicPurchasingSystem`, `internationalFinancialInstitutions` (frameworks) | 2 (`hasItems`, `restrictedDerivatives`) |

`hasAuction` is the option the most procedures may choose - ten of them - so it
is the one worth covering widest. `competitiveOrdering` and
`requestForProposal` are where config testing pays off most; the above
threshold family is nearly fully pinned and needs almost none.

The schemas are snapshotted into `libraries/data/config_schemas.py` so the
tests can read them without a standards checkout, and queried through
`libraries/data/config.py`:

```python
variable_pairs()  # the whole test space
procedures_varying("hasAuction")  # where a key is a real branch
config_defaults("requestForProposal")  # what it is without being set
is_variable("restricted", "aboveThreshold")  # False - pinned here
```

Regenerate the snapshot against the standards version the environment under
test runs; a different branch can pin different values:

```shell
python robot_tests/libraries/data/generate_config_schemas.py ../standards
```

**A directory per config option, named after it**, holding the variations of
that option - one file per procedure, or per value where a procedure has more
than one worth covering. The directory is what keeps the set readable:
everything known about `hasAuction` is in one place, whatever it covers.

```
config/tender/has_auction/
  aboveThreshold_off.robot            the option switched off
  belowThreshold_off.robot            the same option, another procedure
config/tender/has_awarding_order/
  aboveThreshold_pinned.robot         pinned here, so the refusal is the test
config/tender/value_currency_equality/
  aboveThreshold_pinned.robot
config/framework/restricted_derivatives/
  dynamicPurchasingSystem_on.robot
```

The file name says the procedure and what is done to the option, since the
directory already says which option it is. Procedure names keep the spelling
the schemas use, so they can be grepped against them.

Every suite is tagged `config:<key>` and `procedure:<name>`.
`Tender Config Data` and `Framework Config Data` take the defaults of a working
procedure and change only the option under test.

`test_config.py` checks the tag against the directory a suite sits in - one
about `hasAuction` in the `has_awarding_order` directory fails before it ever
reaches the API - and that every config suite is aimed where its key can
actually vary. Getting that wrong is easy and expensive - the suite then fails
against the API for a reason that has nothing to do with the behaviour it meant
to cover. A suite tagged `negative` is the exception: it asserts the refusal,
so it belongs exactly where the key is pinned.

A config test does not need a full procedure. Take it only as far as the option
has an effect: most boolean keys show themselves by the time the tender is
published.

## What a procedure directory holds

Every procedure directory holds **`complete.robot`**: the shortest path from
nothing to a completed tender, with no options taken. It is the one suite a
procedure cannot be without - it says what the procedure normally does - and it
is tagged `smoke`, because it is the one that has to stay fast and green.
`test_suites.py` fails when a procedure directory has no `complete.robot`.

Everything else in the directory is one branch off it, named after what it
adds:

```
tests/procedures/aboveThreshold/
  complete.robot              THE MINIMAL FLOW: one lot, one bid, complete
  auction.robot               two lots, two bidders, a real auction
  unsuccessful.robot          ends unsuccessful: nobody bid
  cancellation.robot          ends cancelled, after a complaint period
  lot_cancellation.robot      one lot cancelled, the tender carries on
  questions.robot             questions asked and answered
  unanswered_question.robot   an unanswered question blocks tendering
  tender_complaints.robot     a complaint about the tender, satisfied
  award_claims.robot          a claim about an award, resolved
  award_complaints.robot      a complaint about an award, declined
tests/procedures/reporting/
  complete.robot              THE MINIMAL FLOW: reported, awarded, closed
  contract_change.robot       the contract repriced and amended
  without_plan.robot          created without a plan behind it
  cancellation.robot          ends cancelled, with no complaint period
```

The two cancellation suites are the same branch in two procedures, and that is
the point: reporting has no cancellation complaints, so a submitted
cancellation takes effect at once; above threshold has them, so it waits out a
period in ``pending`` first. A suite that only checked "the tender ended
cancelled" would not tell the two apart.

A branch file adds only the steps its branch needs and reuses the phases for
the rest. Naming it after what it adds, rather than after the procedure, is
what keeps the directory readable as it grows.

### The branches worth having

These come from the API rather than from guesswork - the status machines in
`tender/core/procedure/state/` and the API's own scenario tests under
`docs/tests/` and `src/openprocurement/tender/<pkg>/tests/*_blanks.py`, which
are the closest thing to an inventory of what can happen.

**Terminal status** - every procedure ends in exactly one of these, and each is
a branch worth owning:

| Ending | What causes it | Covered by |
|---|---|---|
| `complete` | every contract activated (per lot, when there are lots) | `complete.robot` in each procedure |
| `cancelled` | a cancellation becomes active | `cancellation.robot`, in both procedures |
| `unsuccessful` | fewer bids than `minBidsNumber`, or every award unsuccessful | `unsuccessful.robot` (too few bids) |
| `draft.unsuccessful` | `closeFrameworkAgreementSelectionUA` only, when the agreement does not fit | nothing yet |

Arriving at a terminal status is half the check; the other half is that the
tender cannot leave it. `The Tender Should Be Terminated` asserts both, and
every ending above goes through it.

**Cancellation** - `draft` → `pending` → `active`, and the branch points are
whether the procedure has cancellation complaints (`pending` waits out a
complaint period) and whether it cancels the tender or one lot. A cancellation
needs a reason and a signed `cancellationReport` document before it may leave
draft. A satisfied complaint sends it to `unsuccessful` instead, and the tender
keeps running.

**Questions** - `questionOf` may be `tender`, `lot` or `item`. Worth covering:
answered inside the enquiry period; asked outside it and refused; and the one
that matters end to end - **an unanswered question blocks the end of
tendering**.

**Claims and complaints** - the same collection, told apart by `type`. A claim
is pre-trial and addressed to the tender owner: `draft` → `claim` → `answered`
→ `resolved`. A complaint is escalated to the reviewers and carries a fee:
`draft` → `pending` → `accepted` → `satisfied` | `declined` | `stopped`. Which
of the two exists is per procedure: belowThreshold and requestForProposal have
claims only. They attach at four levels - tender, award, qualification and
cancellation - and a pending complaint blocks the step it is attached to.

Two things vary independently here, so the suites are named for both: **who
decides** (a claim goes to the owner, a complaint to the reviewers) and **what
is objected to** (the tender, an award, a qualification, a cancellation).
`tender_complaints`, `award_claims` and `award_complaints` are the three that
exist. There is deliberately no `tender_claims`: at tender level the claim
route is registered for PATCH only, so a claim there cannot be created at all -
no bundled data folder creates one either, while 112 files create award claims.
the procedure's own `negative/` holds that refusal instead. Qualification and
cancellation complaints are not covered yet. Where two suites would otherwise
walk the same path, they take different
endings on purpose - a claim declined in one and resolved in the other, a
complaint satisfied in one and declined in the other - so the second suite
earns its runtime.

A claim or a complaint about an award has to be raised **inside the complaint
period the award opened when it went active**. That is why those suites qualify
the award with `Кваліфікувати Переможця` rather than `Кваліфікувати Всіх
Переможців`: the latter
waits the period out, which closes the very window they need.

**Awards** - `pending` → `active` | `unsuccessful`, and `active` → `cancelled`.
With an awarding order the next award is created the moment the previous one
goes unsuccessful or cancelled, which is the branch behind "second bidder
wins". Without one, every award is created at once. An award cancelled after
the tender reached `active.awarded` pulls it back to `active.qualification`.

**Bids** - `draft` → `pending`, and everything else happens to them: a draft bid
is dropped at the end of tendering, any owner edit during tendering invalidates
the pending bids, a bid with no lot left is `unsuccessful`.

## Choosing what to cover

The axes multiply: procedure type, lot count, the config options above,
cancellation, questions, claims, complaints and the unsuccessful branches.
Their product is thousands of runs, so coverage is chosen, not enumerated.

- **Procedure is the main axis.** One minimal flow per procedure type. This is
  the regression base.
- **A branch is exercised once, in the cheapest procedure that has it.**
  Cancellation belongs on reporting, which finishes in seconds and has no
  complaint period, not on an above threshold tender with an auction. Claims
  belong on belowThreshold, which has claims and no complaints. Complaints
  belong wherever the reviewer tokens are available.
- **Expensive things run rarely and assert a lot.** The auction is the only
  genuinely slow part; one scenario should get everything it can out of it.

The goal is that every branch is executed somewhere, not that every combination
is.

## Tags

Tags are what make a large set usable; four axes cover the ways anyone selects.

| Axis | Examples |
|---|---|
| procedure | `procedure:aboveThreshold`, `procedure:reporting` |
| phase | `phase:tendering`, `phase:contracting` |
| feature | `feature:auction`, `feature:complaints`, `feature:econtract` |
| role | `smoke`, `slow`, `negative`, `config` |

They combine: `--include procedure:reportingANDsmoke`, `--exclude slow`.
`slow` means "waits on a chronograph or an auction" and is the tag that decides
whether a run takes minutes or an hour.

Tags stay in English even though the suites are Ukrainian: CI selects on them,
`procedure:<name>` has to match the procedure directory it sits in, and the
config directories are named after the option their tag carries. They are
identifiers, not prose.

## What to assert

Status transitions are the floor, not the ceiling. A phase should also check
the things that would still be wrong if every request returned 200:

- **Invariants** - one contract per lot, the winner is the bidder that offered
  less, the award value matches the winning bid.
- **Values and dates** - `dateSigned` inside the contract period, amounts
  carried through unchanged, periods that do not overlap.
- **Absence** - with `hasAuction` off there is no `auctionPeriod`; with
  complaints off the endpoint refuses.
- **Refusals** - a forbidden transition returns the expected code and message,
  not merely "not 200".

## Negative tests

A failing action raises inside the keyword and fails that test, which is what
makes refusals testable. Prefer them in the procedure's `negative/`, against
one procedure brought to the state under test and then poked repeatedly, rather
than one procedure per refusal.

Assert the error text, not only the status. A 422 that changed its reason is a
behaviour change worth catching.

## Language

The suites are Ukrainian, written in Robot Framework's own Ukrainian
localization: `language: uk` on line one, then the Ukrainian section and
setting names exactly as `robot.conf.languages.Uk` defines them
(`*** Налаштування ***`, `*** Тест-кейси ***`, `*** Ключових слова ***`,
`Документація`, `Налаштування Suite`, `Розбірка Suite`, `Тестові теги`,
`[Документація]`, `[Теги]`, `[Аргументи]`). Some of those readings are
awkward; they are Robot's, not ours, and changing them would stop the file
parsing.

The vocabulary of the keywords is taken from the Ukrainian source of the API
documentation (`docs/source/**/*.rst` in openprocurement.api), so that a suite
reads the way the procedure is written about there:

| API | Ukrainian | where the docs say it |
|---|---|---|
| tender | закупівля | «Створення закупівлі», «Активація закупівлі» |
| bid | (тендерна) пропозиція | «Реєстрація пропозиції» |
| award | визначення переможця, переможець | «визначенням переможця `award`» |
| claim | вимога | «Скарги та Вимоги на умови закупівлі» |
| complaint | скарга | same |
| question | звернення | «Хто подає звернення», «Відповідь на звернення» |
| procuringEntity | замовник | «Звернення до замовника `procuringEntity`» |
| buyers | покупці | «вказати себе в списку покупців `buyers`» |
| kind=central | центральна закупівельна організація (ЦЗО) | «здійснює закупівлі в інтересах замовників (ЦЗО)» |
| tenderer | учасник | «`tenderer` - учасник закупівлі» |
| supplier | постачальник | «санкції щодо постачальника» |
| contract | договір | «звітування про укладений договір» |
| items | предмет закупівлі | «Предмет закупівлі в пропозиції» |
| guarantee | забезпечення тендерної пропозиції | «Забезпечення тендерних пропозицій» |
| minimalStep | мінімальний крок аукціону | «Мінімальний крок аукціону у відсотках» |
| value | очікувана вартість | «очікувана вартість вказується без ПДВ» |
| tenderPeriod | період подання пропозицій | «Період подання пропозицій» |
| enquiryPeriod | період уточнень | «Період уточнень `enquiryPeriod`» |
| awardCriteria | критерій визначення переможця | «Критерій визначення переможця» |
| features | нецінові критерії | «Оголошення закупівлі з неціновими критеріями» |
| eligible | відповідність критеріям прийнятності | «Підтверджує відповідність критеріям прийнятності» |
| selection criteria | кваліфікаційні критерії | «опис предмету закупівлі… і кваліфікаційних критеріїв» |
| prequalification | прекваліфікація | «Провести прекваліфікацію» |
| cancellation report | протокол | «Протокол рішення… про скасування» |
| aboveThresholdReviewers | орган оскарження | АМКУ, the body a complaint goes to |
| framework | фреймворк | «Створення фреймворку з обмеженим доступом» |

`milestones` the docs leave untranslated; the suites call one **етап**, since
what they carry are `financing` and `delivery` stages - «етапи оплати й
поставки» in the prose.

What stays in English is what is a name in the system rather than prose:
variables (`${tender}`, `${data}`), keyword arguments (`index=0`, `lots=3`),
tags (`smoke`, `negative`, `procedure:aboveThreshold`), Robot's own BuiltIn
keywords, and the API error text a refusal is matched against. Robot does not
localize its keywords and the API answers in English, so translating either
would be a lie.

Three unit tests hold this in place: every suite starts with `language: uk`,
documents itself with `Документація`, and closes the session it opens.

## Naming

- Suite: the scenario, as a sentence fragment - `Понад поріг з двома лотами`.
- Test: the phase, in the language of the procedure - `Зібрати Пропозиції`, not
  `Створити Пропозиції І Перевести Їх У Pending`.
- Phase keyword: an action on the procedure - `Опублікувати Критерії`,
  `Кваліфікувати Всіх Переможців`.
- Data keyword: the thing it builds, starting with `Дані` - `Дані Закупівлі`,
  `Дані Підписанта`.

If a test name repeats the keyword it calls, the test is too small.

## Running

| When | Selection | Budget |
|---|---|---|
| Every change | `--include smoke --exclude slow` | minutes |
| Nightly | everything, parallel by scenario | as long as it takes |
| While developing | one file, or `--include feature:econtract` | seconds to minutes |

Scenarios are independent across files, so the nightly run parallelises by
file. Phases within a file are not independent and must stay in one process.

## Environment and repeatability

- The suites talk to a real CDB and create real procedures. A failure can mean
  the environment, not the code; the console log shows which request was in
  flight when it stopped.
- `ACCELERATION` decides how much of a procedure is waiting. It shortens
  periods; it does not remove the auction.
- `SEED` makes the generated data repeatable, which matters when reproducing a
  failure.
- Anything that waits on a chronograph or an auction carries `slow`.

## Data builders

The suites build payloads in memory rather than reading fixtures, and that only
stays workable under a few conventions:

- A builder composes smaller builders and accepts each of them as an argument,
  so a test replaces one piece without restating the rest.
- Defaults are valid on their own: `Дані Закупівлі` with no arguments creates a
  tender.
- Anything derived from the API is read back from the API. Criteria ids come
  from the posted criteria, contract items from the created contract. Nothing
  that the server generates is written down twice.
- A payload keyword returns what the action sends, wrapper included; a piece
  keyword returns the piece.

## Adding a test

1. Decide whether it is a scenario, a config option or a refusal, and put it in
   the matching directory. A procedure that is new starts with `complete.robot`
   and nothing else; its branches come after it, one file each.
2. Reuse the phases. If a phase almost fits, give it an argument rather than
   copying it.
3. Add the tags: procedure, phase, feature, role.
4. Name the assertions. If there are none beyond status transitions, ask again
   whether this belongs in a data folder.
5. Check it with `--dryrun`, then once live.

## Where to look things up

| Question | Where |
|---|---|
| What may this procedure put in its config? | `standards/data_model/schema/TenderConfig/<pmt>.json`, snapshotted in `libraries/data/config_schemas.py` |
| What statuses can this tender reach, and what moves it? | `openprocurement.api`, `tender/core/procedure/state/tender_details.py` (owner PATCH) and `state/chronograph.py` (time driven) |
| What can happen to an award, a bid, a cancellation? | `tender/core/procedure/state/{award,bid,cancellation}.py` |
| Which procedures have claims, which have complaints? | the `hasTenderComplaints` / `hasAwardComplaints` config per procedure |
| What scenarios exist at all? | the API's own tests: `docs/tests/test_tender_*.py` (end to end, closest to these suites) and `src/openprocurement/tender/<pkg>/tests/*_blanks.py` (one function per scenario) |
| Which actions can a keyword wrap? | `procedure_tools/actions/` |

`docs/tests/test_tender_config.py` in the API walks the config flags one by one
and is the most direct answer to "what does this option change".

## Where the gaps are now

In rough order of value per hour spent:

1. **Qualification and cancellation complaints are uncovered**, and so is what
   a pending complaint blocks: a satisfied award complaint should unseat the
   winner, and none of the suites check that it does.
2. **Config: four of the 49 open pairs are covered.** The two procedures where
   config actually varies - `competitiveOrdering` with 14 keys and
   `requestForProposal` with 11 - have no data builders yet, so neither has a
   single config test. `Tender Config Data <procedure>` already produces valid
   defaults for any procedure from its schema, so the missing part is the
   procedure payload, not the config.
3. **Only aboveThreshold and reporting have scenarios.** belowThreshold,
   negotiation, esco, the frameworks and the second-stage procedures have none.
4. **Award branches are uncovered**: the first award going unsuccessful so the
   second bidder wins, an award cancelled after `active.awarded`, the 24h and
   ALP milestones.
5. The invariants checked are the obvious ones: one contract per lot, the
   cheaper bidder wins. Dates and carried-through values are still unchecked.
