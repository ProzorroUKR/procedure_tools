*** Settings ***
Documentation     Setup and the keywords every procedure shares.
...
...               The libraries do the work: ``ProcedureData`` builds payloads,
...               ``ProcedureTools`` sends them through the procedure_tools
...               actions. What lives here is only what more than one procedure
...               needs, in particular the run settings (acceleration and
...               submission method) that the tender dates depend on.

Library           Collections
Library           ProcedureTools
Library           ProcedureData


*** Keywords ***
Open Procedure Session
    [Documentation]    Connect to the API; use it as the suite setup.
    Start Procedure Session

Close Procedure Session
    [Documentation]    Close the connection and drop the generated files.
    End Procedure Session

Run Settings
    [Documentation]    Acceleration and submission method of this run, as a dictionary
    ...                to splat into a data keyword.
    ${acceleration}=    Get Acceleration
    ${submission}=      Get Submission
    ${settings}=        Create Dictionary    acceleration=${acceleration}    submission=${submission}
    RETURN    ${settings}

Publish Tender
    [Documentation]    Move the tender to ``active.tendering`` and check that it got there.
    ${data}=      Tender Patch Data    active.tendering
    ${tender}=    Patch Tender         ${data}
    Should Be Equal    ${tender}[status]    active.tendering
    RETURN    ${tender}

Activate Tender
    [Documentation]    Move a limited procedure tender to ``active``.
    ${data}=      Tender Patch Data    active
    ${tender}=    Patch Tender         ${data}
    Should Be Equal    ${tender}[status]    active
    RETURN    ${tender}

Qualify Award
    [Documentation]    Qualify an award, sign the decision and activate it. Limited
    ...                procedures have no eligibility check, pass ``eligible=${None}``
    ...                to leave it out.
    [Arguments]    ${index}=0    ${eligible}=${True}
    ${qualification}=    Award Qualification Data    eligible=${eligible}
    Patch Award          ${qualification}    index=${index}

    ${notice}=    Signature Document Data    title=award_notice_${index}.p7s
    Attach Award Document    ${notice}    index=${index}

    ${activate}=    Award Patch Data    active
    ${award}=       Patch Award         ${activate}    index=${index}
    Should Be Equal    ${award}[status]    active
    RETURN    ${award}

Sign Contract
    [Documentation]    Take the contract credentials, let both parties name their
    ...                signatory and activate the contract.
    [Arguments]    ${index}=0    ${amount}=${None}    ${with_signer_info}=${True}
    Take Contract Credentials    index=${index}
    IF    ${with_signer_info}
        ${buyer}=       Signer Info Data
        Put Contract Buyer Signer Info        ${buyer}       index=${index}
        ${supplier}=    Signer Info Data
        Put Contract Suppliers Signer Info    ${supplier}    index=${index}
    END
    ${contract}=    Get Contract            index=${index}
    ${data}=        Contract Active Data    ${contract}    amount=${amount}
    ${contract}=    Patch Contract          ${data}        index=${index}
    Should Be Equal    ${contract}[status]    active
    RETURN    ${contract}

Amend Contract
    [Documentation]    Create an amendment and activate it.
    [Arguments]    ${index}=0    ${rationale_type}=itemPriceChange
    ${change}=      Contract Change Data    rationale_type=${rationale_type}
    ${contract}=    Post Contract Change    ${change}    index=${index}
    ${last}=        Evaluate    len($contract["changes"]) - 1
    ${activate}=    Contract Change Active Data    ${contract}
    ${contract}=    Patch Contract Change    ${activate}    index=${index}    change_index=${last}
    Should Be Equal    ${contract}[changes][${last}][status]    active
    RETURN    ${contract}

Terminate Contract
    [Documentation]    Close the contract, stating the amount actually paid.
    [Arguments]    ${amount}    ${index}=0
    ${data}=        Contract Terminated Data    ${amount}
    ${contract}=    Patch Contract    ${data}    index=${index}
    Should Be Equal    ${contract}[status]    terminated
    RETURN    ${contract}
