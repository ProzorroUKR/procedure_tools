"""
Data keywords.

Every keyword here builds a payload in memory and returns it; none of them
reads a fixture file. They are modular on purpose: a keyword composes the
smaller ones, and a test that wants something else passes its own piece in.

    ${lots}=       Lots Data      2
    ${items}=      Items Data     count=2    lots=${lots}
    ${tender}=     Tender Data    lots=${lots}    items=${items}    value.amount=5000
    ${created}=    Create Tender  ${tender}

Any keyword also takes dotted overrides, applied last::

    ${bid}=    Bid Data    ${tender}    lotValues.0.value.amount=1999
"""

from __future__ import annotations

import os
import sys
from typing import Any

from robot.api.deco import keyword, library

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data import award as award_module
from data import bid as bid_module
from data import common, contract, criteria, document, plan, tender
from data.utils import apply_overrides, deep_merge


@library(scope="GLOBAL", version="1.0")
class ProcedureData:
    """Builds the payloads the action keywords send to the API."""

    # --- building blocks

    @keyword("Address Data")
    def address_data(self, **overrides: Any) -> dict[str, Any]:
        """A Kyiv postal address."""
        return common.address_data(**overrides)

    @keyword("Identifier Data")
    def identifier_data(self, identifier_id: str = "21725150", **overrides: Any) -> dict[str, Any]:
        """An EDR identifier of a Ukrainian legal entity."""
        return common.identifier_data(identifier_id, **overrides)

    @keyword("Contact Point Data")
    def contact_point_data(self, with_email: bool = True, **overrides: Any) -> dict[str, Any]:
        """A contact person, with an email or a web page."""
        return common.contact_point_data(with_email=with_email, **overrides)

    @keyword("Organization Data")
    def organization_data(self, kind: str = "general", **overrides: Any) -> dict[str, Any]:
        """An organization: address, contact point, identifier and name."""
        return common.organization_data(kind=kind, **overrides)

    @keyword("Procuring Entity Data")
    def procuring_entity_data(self, kind: str = "special", **overrides: Any) -> dict[str, Any]:
        """The organization that runs the procedure."""
        return common.procuring_entity_data(kind=kind, **overrides)

    @keyword("Tenderer Data")
    def tenderer_data(self, identifier_id: str = "00137256", **overrides: Any) -> dict[str, Any]:
        """The organization that submits a bid."""
        return common.tenderer_data(identifier_id=identifier_id, **overrides)

    @keyword("Supplier Data")
    def supplier_data(self, identifier_id: str = "13313462", **overrides: Any) -> dict[str, Any]:
        """The organization an award is granted to."""
        return common.supplier_data(identifier_id=identifier_id, **overrides)

    @keyword("Classification Data")
    def classification_data(self, **overrides: Any) -> dict[str, Any]:
        """A ДК021 classification."""
        return common.classification_data(**overrides)

    @keyword("Unit Data")
    def unit_data(self, **overrides: Any) -> dict[str, Any]:
        """A unit of measure."""
        return common.unit_data(**overrides)

    @keyword("Value Data")
    def value_data(self, amount: float = 1000, **overrides: Any) -> dict[str, Any]:
        """An amount with its currency and VAT flag."""
        return common.value_data(amount=amount, **overrides)

    @keyword("Item Data")
    def item_data(self, quantity: float = 1, related_lot: str | None = None, **overrides: Any) -> dict[str, Any]:
        """One item of a tender, optionally bound to a lot."""
        return common.item_data(quantity=quantity, related_lot=related_lot, **overrides)

    @keyword("Lot Data")
    def lot_data(self, title: str | None = None, amount: float = 2500, **overrides: Any) -> dict[str, Any]:
        """One lot, with the id needed to bind items and criteria to it."""
        return common.lot_data(title=title, amount=amount, **overrides)

    @keyword("Milestone Data")
    def milestone_data(self, code: str = "prepayment", **overrides: Any) -> dict[str, Any]:
        """One payment or delivery milestone."""
        return common.milestone_data(code=code, **overrides)

    @keyword("Signer Info Data")
    def signer_info_data(self, **overrides: Any) -> dict[str, Any]:
        """The signatory of a contract party, as the signer info request sends it."""
        return contract.contract_signer_info_data(**overrides)

    # --- documents

    @keyword("Document Data")
    def document_data(
        self,
        title: str = "document.txt",
        document_type: str | None = None,
        content: str | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """A document to attach, together with the file content uploaded for it."""
        return document.document_data(title=title, document_type=document_type, content=content, **overrides)

    @keyword("Signature Document Data")
    def signature_document_data(self, title: str = "sign.p7s", **overrides: Any) -> dict[str, Any]:
        """A notice signature document."""
        return document.signature_document_data(title=title, **overrides)

    @keyword("Contract Proforma Document Data")
    def contract_proforma_document_data(self, title: str = "contract_proforma.txt", **overrides: Any) -> dict[str, Any]:
        """The draft contract published with the tender."""
        return document.contract_proforma_document_data(title=title, **overrides)

    @keyword("Proposal Document Data")
    def proposal_document_data(self, title: str = "bid_proposal.p7s", **overrides: Any) -> dict[str, Any]:
        """The signed proposal a bid must carry to be submitted."""
        return document.proposal_document_data(title=title, **overrides)

    # --- plan

    @keyword("Plan Data")
    def plan_data(
        self,
        procurement_method_type: str = "aboveThreshold",
        acceleration: float | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """A draft plan for the given procedure type."""
        return plan.plan_data(
            procurement_method_type=procurement_method_type,
            acceleration=acceleration,
            **overrides,
        )

    @keyword("Reporting Plan Data")
    def reporting_plan_data(self, acceleration: float | None = None, **overrides: Any) -> dict[str, Any]:
        """A draft plan for a reporting procedure."""
        return plan.reporting_plan_data(acceleration=acceleration, **overrides)

    @keyword("Plan Patch Data")
    def plan_patch_data(self, status: str = "scheduled", **overrides: Any) -> dict[str, Any]:
        """A patch that moves the plan to a status."""
        return plan.plan_patch_data(status=status, **overrides)

    # --- tender

    @keyword("Lots Data")
    def lots_data(self, count: int = 1, amount: float = 2500, **overrides: Any) -> list[dict[str, Any]]:
        """``count`` numbered lots."""
        return tender.lots_data(count=int(count), amount=amount, **overrides)

    @keyword("Items Data")
    def items_data(
        self,
        count: int = 1,
        lots: list[dict[str, Any]] | None = None,
        quantity: float = 1,
        **overrides: Any,
    ) -> list[dict[str, Any]]:
        """``count`` items per lot, or ``count`` items when there are no lots."""
        return tender.items_data(count=int(count), lots=lots, quantity=quantity, **overrides)

    @keyword("Milestones Data")
    def milestones_data(self, lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        """Payment and delivery milestones, per lot when there are lots."""
        return tender.milestones_data(lots)

    @keyword("Tender Data")
    def tender_data(
        self,
        procurement_method_type: str = "aboveThreshold",
        lots: list[dict[str, Any]] | None = None,
        items: list[dict[str, Any]] | None = None,
        config: dict[str, Any] | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """An open tender ready to be created."""
        return tender.tender_data(
            procurement_method_type=procurement_method_type,
            lots=lots,
            items=items,
            config=config,
            **overrides,
        )

    @keyword("Reporting Tender Data")
    def reporting_tender_data(self, amount: float = 500000, **overrides: Any) -> dict[str, Any]:
        """A reporting tender: limited procedure, no bids, no auction."""
        return tender.reporting_tender_data(amount=amount, **overrides)

    @keyword("Tender Patch Data")
    def tender_patch_data(self, status: str, **overrides: Any) -> dict[str, Any]:
        """A patch that moves the tender to a status."""
        return tender.tender_patch_data(status, **overrides)

    # --- criteria

    @keyword("Criteria Data")
    def criteria_data(
        self,
        lots: list[dict[str, Any]] | None = None,
        include: list[str] | None = None,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        The criteria of a tender, with fresh requirement ids.

        Lot related criteria (the guarantees) are repeated for every lot.
        """
        return criteria.criteria_data(lots=lots, include=include, exclude=exclude)

    @keyword("Exclusion Criteria Data")
    def exclusion_criteria_data(self, lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        """Grounds for refusing a bidder."""
        return criteria.exclusion_criteria(lots)

    @keyword("Selection Criteria Data")
    def selection_criteria_data(self, lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        """Qualification criteria: equipment, staff, experience, finances."""
        return criteria.selection_criteria(lots)

    @keyword("Other Criteria Data")
    def other_criteria_data(self, lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        """Language, guarantees and bid validity period."""
        return criteria.other_criteria(lots)

    @keyword("Criterion Data")
    def criterion_data(
        self, classification_id: str, related_item: str | None = None, **overrides: Any
    ) -> dict[str, Any]:
        """One criterion by its classification id."""
        return criteria.criterion(classification_id, related_item=related_item, **overrides)

    @keyword("Requirement Responses Data")
    def requirement_responses_data(
        self,
        tender_criteria: list[dict[str, Any]] | dict[str, Any],
        document_title: str | None = None,
    ) -> dict[str, Any]:
        """
        Bid answers to the criteria the tender actually has.

        Pass the criteria the API returned; the answers then carry requirement
        ids that exist in the tender. With ``document_title`` the answers also
        point at a document of the bid as evidence.
        """
        return criteria.requirement_responses_data(tender_criteria, document_title=document_title)

    # --- bid

    @keyword("Bid Data")
    def bid_data(
        self,
        tender_data: dict[str, Any],
        amount: float | None = None,
        amounts: list[float] | None = None,
        documents: list[dict[str, Any]] | None = None,
        eligibility_documents: list[dict[str, Any]] | None = None,
        financial_documents: list[dict[str, Any]] | None = None,
        qualification_documents: list[dict[str, Any]] | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """A draft bid for the tender, offering every lot it has."""
        return bid_module.bid_data(
            tender_data,
            amount=amount,
            amounts=amounts,
            documents=documents,
            eligibility_documents=eligibility_documents,
            financial_documents=financial_documents,
            qualification_documents=qualification_documents,
            **overrides,
        )

    @keyword("Bid Patch Data")
    def bid_patch_data(self, status: str = "pending", **overrides: Any) -> dict[str, Any]:
        """A patch that moves the bid to a status."""
        return bid_module.bid_patch_data(status=status, **overrides)

    # --- award

    @keyword("Award Data")
    def award_data(self, amount: float = 475000, **overrides: Any) -> dict[str, Any]:
        """An award created by the procuring entity in a limited procedure."""
        return award_module.award_data(amount=amount, **overrides)

    @keyword("Award Qualification Data")
    def award_qualification_data(self, qualified: bool = True, **overrides: Any) -> dict[str, Any]:
        """The decision that the bidder meets the criteria."""
        return award_module.award_qualification_data(qualified=qualified, **overrides)

    @keyword("Award Patch Data")
    def award_patch_data(self, status: str, **overrides: Any) -> dict[str, Any]:
        """A patch that moves the award to a status."""
        return award_module.award_patch_data(status, **overrides)

    # --- contract

    @keyword("Contract Active Data")
    def contract_active_data(
        self,
        contract_data: dict[str, Any],
        amount: float | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """The signed contract: number, period, value and item prices."""
        return contract.contract_active_data(contract_data, amount=amount, **overrides)

    @keyword("Contract Value Data")
    def contract_value_data(self, amount: float, **overrides: Any) -> dict[str, Any]:
        """A change of the agreed value of an active contract."""
        return contract.contract_value_data(amount, **overrides)

    @keyword("Contract Change Data")
    def contract_change_data(self, rationale_type: str = "itemPriceChange", **overrides: Any) -> dict[str, Any]:
        """An amendment to an active contract."""
        return contract.contract_change_data(rationale_type=rationale_type, **overrides)

    @keyword("Contract Change Active Data")
    def contract_change_active_data(self, contract_data: dict[str, Any], **overrides: Any) -> dict[str, Any]:
        """The signature that makes an amendment take effect."""
        return contract.contract_change_active_data(contract_data, **overrides)

    @keyword("Contract Terminated Data")
    def contract_terminated_data(self, amount: float, **overrides: Any) -> dict[str, Any]:
        """Closing the contract, stating how much of it was paid."""
        return contract.contract_terminated_data(amount, **overrides)

    # --- composition

    @keyword("Merge Data")
    def merge_data(self, base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
        """``patch`` merged into ``base``, dictionary by dictionary."""
        return deep_merge(base, patch)

    @keyword("Patch Data")
    def patch_data(self, base: dict[str, Any], **overrides: Any) -> dict[str, Any]:
        """``base`` with dotted overrides applied, e.g. ``value.amount=100``."""
        return apply_overrides(base, overrides)
