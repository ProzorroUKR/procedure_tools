*** Settings ***
Documentation     Reporting procedure: a purchase that was already made and is only
...               being reported.
...
...               There is no tendering and no auction, so the procuring entity names
...               the supplier itself by creating the award, and the contract follows
...               straight from it.

Resource          ../resources/procedure.resource

Suite Setup       Open Procedure Session
Suite Teardown    Close Procedure Session
Test Setup        Reset Procedure State

Force Tags        reporting


*** Variables ***
${TENDER_AMOUNT}     ${500000}
${AWARD_AMOUNT}      ${475000}


*** Test Cases ***
Reporting With A Contract Change
    [Documentation]    Report a purchase, award it to the chosen supplier, sign the
    ...                contract, change its price and close it.
    [Tags]    smoke

    ${tender}=    Publish Reporting Tender

    Award The Chosen Supplier

    ${contract}=    Sign Contract    index=0    with_signer_info=${False}
    ${new_amount}=  Evaluate    round(${contract}[value][amount] + 0.45, 2)
    Patch Contract    ${{ {'data': {'value': {'amount': $new_amount, 'amountNet': $new_amount, 'valueAddedTaxIncluded': False}}} }}

    Amend Contract    index=0    rationale_type=itemPriceChange

    ${paid}=    Evaluate    round(${new_amount} * 0.9, 2)
    Terminate Contract    ${paid}
    Wait Tender Status    complete

Reporting Without A Plan
    [Documentation]    A reporting tender can also be created on its own, without a
    ...                plan behind it.
    [Tags]    no-plan

    ${settings}=    Run Settings
    ${data}=        Reporting Tender Data    amount=${TENDER_AMOUNT}
    ...                                      acceleration=${settings}[acceleration]
    ${tender}=      Create Tender    ${data}
    Should Be Equal    ${tender}[procurementMethodType]    reporting
    Should Be Equal    ${tender}[status]                   draft

    Activate Tender
    Award The Chosen Supplier
    Sign Contract    index=0    with_signer_info=${False}
    Terminate Contract    ${AWARD_AMOUNT}
    Wait Tender Status    complete


*** Keywords ***
Publish Reporting Tender
    [Documentation]    Plan the purchase, report it as a tender and publish it with its
    ...                documents.
    ${settings}=    Run Settings
    ${plan}=        Reporting Plan Data    acceleration=${settings}[acceleration]
    Create Plan     ${plan}
    Patch Plan      ${{ {'data': {'status': 'scheduled'}} }}

    ${data}=      Reporting Tender Data    amount=${TENDER_AMOUNT}
    ...                                    acceleration=${settings}[acceleration]
    ${tender}=    Create Tender    ${data}
    Should Be Equal    ${tender}[procurementMethodType]    reporting

    ${document}=    Document Data    title=tender_report.txt
    Attach Tender Document    ${document}
    ${proforma}=    Contract Proforma Document Data
    Attach Tender Document    ${proforma}

    ${tender}=    Activate Tender
    RETURN    ${tender}

Award The Chosen Supplier
    [Documentation]    Create the award for the supplier the purchase was made from,
    ...                qualify it and activate it.
    ${data}=    Award Data    amount=${AWARD_AMOUNT}
    Create Award    ${data}
    Wait Tender Status    active    fail_status=unsuccessful
    Wait Awards Edr Documents
    ${award}=    Qualify Award    index=0    eligible=${None}
    RETURN    ${award}
