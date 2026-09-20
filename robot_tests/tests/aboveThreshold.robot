*** Settings ***
Documentation     Above threshold open procedure, from the plan to the closed contract.
...
...               The payloads are built by the data keywords, never read from a
...               file, so each test states only what it cares about: how many
...               lots, how many bids and what happens after the auction.

Resource          ../resources/procedure.resource

Suite Setup       Open Procedure Session
Suite Teardown    Close Procedure Session
Test Setup        Reset Procedure State

Force Tags        aboveThreshold


*** Variables ***
${LOT_AMOUNT}     ${2500}


*** Test Cases ***
Above Threshold With Two Lots And Two Bids
    [Documentation]    The full positive flow: a planned purchase becomes a tender with
    ...                criteria, two tenderers bid on both lots, the auction ranks them,
    ...                the winners are qualified and every contract is signed, amended
    ...                and closed.
    [Tags]    smoke    auction

    ${tender}    ${criteria}=    Publish Tender With Criteria    lots=2

    Submit Bid    ${tender}    ${criteria}    index=0
    Submit Bid    ${tender}    ${criteria}    index=1
    ${bids}=    Get Bids
    Length Should Be    ${bids}    2

    Wait Tender Next Check
    Wait Tender Status    ${{ ['active.auction', 'active.qualification', 'active.awarded'] }}
    ...                   fail_status=unsuccessful
    Wait Tender Auction

    Qualify Every Award
    Complete Every Contract    amend=${True}

Above Threshold Without An Auction
    [Documentation]    One lot and one bid, with the auction switched off: the shortest
    ...                way from a published tender to a completed one.
    [Tags]    no-auction

    ${tender}    ${criteria}=    Publish Tender With Criteria
    ...                          lots=1    submission=quick(mode:no-auction)

    Submit Bid    ${tender}    ${criteria}    index=0

    Wait Tender Next Check
    Wait Tender Status    ${{ ['active.qualification', 'active.awarded'] }}
    ...                   fail_status=unsuccessful

    Qualify Every Award
    Complete Every Contract


*** Keywords ***
Publish Tender With Criteria
    [Documentation]    Plan the purchase, create the tender from the plan, publish its
    ...                criteria and documents and open it for bids. Returns the tender
    ...                and the criteria the API assigned ids to.
    [Arguments]    ${lots}=1    ${submission}=${None}

    ${settings}=    Run Settings
    ${plan}=        Plan Data    aboveThreshold    acceleration=${settings}[acceleration]
    Create Plan     ${plan}
    Patch Plan      ${{ {'data': {'status': 'scheduled'}} }}

    ${lot_list}=    Lots Data    ${lots}    amount=${LOT_AMOUNT}
    ${submission}=  Set Variable If    $submission is not None    ${submission}    ${settings}[submission]
    ${data}=        Tender Data    lots=${lot_list}
    ...                            acceleration=${settings}[acceleration]
    ...                            submission=${submission}
    ${tender}=      Create Tender    ${data}
    Should Be Equal     ${tender}[status]    draft
    Length Should Be    ${tender}[lots]      ${{ int($lots) }}

    ${proforma}=    Contract Proforma Document Data
    Attach Tender Document    ${proforma}

    ${criteria_data}=    Criteria Data           lots=${tender}[lots]
    ${criteria}=         Post Tender Criteria    ${criteria_data}

    ${notice}=    Signature Document Data    title=tender_notice.p7s
    Attach Tender Document    ${notice}

    ${tender}=    Publish Tender
    RETURN    ${tender}    ${criteria}

Submit Bid
    [Documentation]    Create a draft bid with its documents, answer the tender criteria
    ...                and submit it for consideration.
    [Arguments]    ${tender}    ${criteria}    ${index}=0    ${amounts}=${None}

    ${proposal}=       Document Data    title=bid_${index}_proposal.txt
    ${eligibility}=    Document Data    title=bid_${index}_eligibility.txt
    ${financial}=      Document Data    title=bid_${index}_financial.txt

    ${data}=    Bid Data    ${tender}
    ...                     amounts=${amounts}
    ...                     documents=${{ [$proposal] }}
    ...                     eligibility_documents=${{ [$eligibility] }}
    ...                     financial_documents=${{ [$financial] }}
    ${bid}=     Create Bid    ${data}    index=${index}
    Should Be Equal    ${bid}[status]    draft

    ${responses}=    Requirement Responses Data    ${criteria}
    ...                                            document_title=${proposal}[data][title]
    Post Bid Requirement Responses    ${responses}    index=${index}

    ${signature}=    Proposal Document Data    title=bid_${index}_proposal.p7s
    Attach Bid Document    ${signature}    index=${index}

    ${bid}=    Patch Bid    ${{ {'data': {'status': 'pending'}} }}    index=${index}
    Should Be Equal    ${bid}[status]    pending
    RETURN    ${bid}

Qualify Every Award
    [Documentation]    Qualify and activate the awards until the tender leaves
    ...                qualification, which is what tells us every lot has a winner,
    ...                then wait out the complaint periods.
    Wait Awards Edr Documents
    ${tender}=    Refresh Tender
    WHILE    "${tender}[status]" == "active.qualification"    limit=15
    ...      on_limit_message=the tender stayed in qualification
        ${awards}=    Get Awards
        ${pending}=   Evaluate
        ...    [index for index, award in enumerate($awards) if award["status"] == "pending"]
        IF    ${pending}
            FOR    ${index}    IN    @{pending}
                Qualify Award    index=${index}
            END
        ELSE
            Wait Seconds    5
        END
        ${tender}=    Refresh Tender
    END
    Wait Awards Complaint Period
    Wait Tender Status    active.awarded    fail_status=unsuccessful

Complete Every Contract
    [Documentation]    Sign every contract of the tender, optionally amend it, and close
    ...                it so that the tender itself can complete.
    [Arguments]    ${amend}=${False}
    ${contracts}=    Get Contracts
    FOR    ${index}    ${contract}    IN ENUMERATE    @{contracts}
        ${contract}=    Sign Contract    index=${index}
        IF    ${amend}
            Amend Contract    index=${index}    rationale_type=fiscalYearExtension
        END
        ${paid}=    Evaluate    round(${contract}[value][amount] * 0.9, 2)
        Terminate Contract    ${paid}    index=${index}
    END
    Wait Tender Status    complete
