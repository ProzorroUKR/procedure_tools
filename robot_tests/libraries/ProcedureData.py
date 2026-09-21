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
from data import (
    cancellation,
    common,
    complaint,
    contract,
    criteria,
    document,
    feature,
    framework,
    plan,
    question,
    tender,
)
from data.utils import apply_overrides, deep_merge


@library(scope="GLOBAL", version="1.0")
class ProcedureData:
    """Builds the payloads the action keywords send to the API."""

    # --- building blocks

    @keyword("Дані Адреси")
    def address_data(self, **overrides: Any) -> dict[str, Any]:
        """A Kyiv postal address."""
        return common.address_data(**overrides)

    @keyword("Дані Ідентифікатора")
    def identifier_data(self, identifier_id: str = "21725150", **overrides: Any) -> dict[str, Any]:
        """An EDR identifier of a Ukrainian legal entity."""
        return common.identifier_data(identifier_id, **overrides)

    @keyword("Дані Контактної Особи")
    def contact_point_data(self, with_email: bool = True, **overrides: Any) -> dict[str, Any]:
        """A contact person, with an email or a web page."""
        return common.contact_point_data(with_email=with_email, **overrides)

    @keyword("Дані Організації")
    def organization_data(self, kind: str = "general", **overrides: Any) -> dict[str, Any]:
        """An organization: address, contact point, identifier and name."""
        return common.organization_data(kind=kind, **overrides)

    @keyword("Дані Замовника")
    def procuring_entity_data(self, kind: str = "special", **overrides: Any) -> dict[str, Any]:
        """The organization that runs the procedure."""
        return common.procuring_entity_data(kind=kind, **overrides)

    @keyword("Дані Учасника")
    def tenderer_data(self, identifier_id: str = "00137256", **overrides: Any) -> dict[str, Any]:
        """The organization that submits a bid."""
        return common.tenderer_data(identifier_id=identifier_id, **overrides)

    @keyword("Дані Постачальника")
    def supplier_data(self, identifier_id: str = "13313462", **overrides: Any) -> dict[str, Any]:
        """The organization an award is granted to."""
        return common.supplier_data(identifier_id=identifier_id, **overrides)

    @keyword("Дані Класифікатора")
    def classification_data(self, **overrides: Any) -> dict[str, Any]:
        """A ДК021 classification."""
        return common.classification_data(**overrides)

    @keyword("Дані Одиниці Виміру")
    def unit_data(self, **overrides: Any) -> dict[str, Any]:
        """A unit of measure."""
        return common.unit_data(**overrides)

    @keyword("Дані Вартості")
    def value_data(self, amount: float = 1000, **overrides: Any) -> dict[str, Any]:
        """An amount with its currency and VAT flag."""
        return common.value_data(amount=amount, **overrides)

    @keyword("Дані Предмета Закупівлі")
    def item_data(self, quantity: float = 1, related_lot: str | None = None, **overrides: Any) -> dict[str, Any]:
        """One item of a tender, optionally bound to a lot."""
        return common.item_data(quantity=quantity, related_lot=related_lot, **overrides)

    @keyword("Дані Локалізованого Предмета Закупівлі")
    def localised_item_data(self, quantity: float = 1, **overrides: Any) -> dict[str, Any]:
        """An item naming its catalogue product, which a localisation criterion needs."""
        return common.localised_item_data(quantity=quantity, **overrides)

    @keyword("Дані Лота")
    def lot_data(self, title: str | None = None, amount: float = 2500, **overrides: Any) -> dict[str, Any]:
        """One lot, with the id needed to bind items and criteria to it."""
        return common.lot_data(title=title, amount=amount, **overrides)

    @keyword("Дані Етапу")
    def milestone_data(self, code: str = "prepayment", **overrides: Any) -> dict[str, Any]:
        """One payment or delivery milestone."""
        return common.milestone_data(code=code, **overrides)

    @keyword("Дані Підписанта")
    def signer_info_data(self, **overrides: Any) -> dict[str, Any]:
        """The signatory of a contract party, as the signer info request sends it."""
        return contract.contract_signer_info_data(**overrides)

    # --- documents

    @keyword("Дані Документа")
    def document_data(
        self,
        title: str = "document.txt",
        document_type: str | None = None,
        content: str | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """A document to attach, together with the file content uploaded for it."""
        return document.document_data(title=title, document_type=document_type, content=content, **overrides)

    @keyword("Дані Файлу Підпису")
    def signature_document_data(self, title: str = "sign.p7s", **overrides: Any) -> dict[str, Any]:
        """A notice signature document."""
        return document.signature_document_data(title=title, **overrides)

    @keyword("Дані Проекту Договору")
    def contract_proforma_document_data(self, title: str = "contract_proforma.txt", **overrides: Any) -> dict[str, Any]:
        """The draft contract published with the tender."""
        return document.contract_proforma_document_data(title=title, **overrides)

    @keyword("Дані Підпису Пропозиції")
    def proposal_document_data(self, title: str = "bid_proposal.p7s", **overrides: Any) -> dict[str, Any]:
        """The signed proposal a bid must carry to be submitted."""
        return document.proposal_document_data(title=title, **overrides)

    # --- plan

    @keyword("Дані Плану")
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

    @keyword("Дані Плану Звітування")
    def reporting_plan_data(self, acceleration: float | None = None, **overrides: Any) -> dict[str, Any]:
        """A draft plan for a reporting procedure."""
        return plan.reporting_plan_data(acceleration=acceleration, **overrides)

    @keyword("Дані Зміни Плану")
    def plan_patch_data(self, status: str = "scheduled", **overrides: Any) -> dict[str, Any]:
        """A patch that moves the plan to a status."""
        return plan.plan_patch_data(status=status, **overrides)

    # --- features

    @keyword("Дані Нецінового Критерію")
    def feature_data(
        self,
        feature_of: str = "lot",
        related_item: str | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """One non-price quality the bids are compared on."""
        return feature.feature_data(feature_of=feature_of, related_item=related_item, **overrides)

    @keyword("Дані Нецінових Критеріїв")
    def features_data(self, lot_id: str, item_id: str) -> list[dict[str, Any]]:
        """A feature about a lot and one about an item, as the bundled flow declares them."""
        return feature.features_data(lot_id, item_id)

    @keyword("Дані Параметрів")
    def parameters_data(self, features: list[dict[str, Any]], best: bool = False) -> list[dict[str, Any]]:
        """A bid's answer to every feature of the tender."""
        return feature.parameters_data(features, best=best)

    # --- framework

    @keyword("Дані Конфігу Фреймворку")
    def framework_config_data(self, **overrides: Any) -> dict[str, Any]:
        """The config block of a framework, with the named options changed."""
        return framework.framework_config_data(**overrides)

    @keyword("Дані Фреймворку")
    def framework_data(
        self,
        framework_type: str = "dynamicPurchasingSystem",
        config: dict[str, Any] | None = None,
        acceleration: float | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """A framework ready to be created."""
        return framework.framework_data(
            framework_type=framework_type,
            config=config,
            acceleration=acceleration,
            **overrides,
        )

    @keyword("Дані Зміни Фреймворку")
    def framework_patch_data(self, status: str, **overrides: Any) -> dict[str, Any]:
        """A patch that moves the framework to a status."""
        return framework.framework_patch_data(status, **overrides)

    # --- tender

    @keyword("Дані Лотів")
    def lots_data(
        self,
        count: int = 1,
        amount: float = 2500,
        with_minimal_step: bool = True,
        **overrides: Any,
    ) -> list[dict[str, Any]]:
        """``count`` numbered lots; a tender with no auction takes them without a minimal step."""
        return tender.lots_data(
            count=int(count),
            amount=amount,
            with_minimal_step=with_minimal_step,
            **overrides,
        )

    @keyword("Дані Предметів Закупівлі")
    def items_data(
        self,
        count: int = 1,
        lots: list[dict[str, Any]] | None = None,
        quantity: float = 1,
        **overrides: Any,
    ) -> list[dict[str, Any]]:
        """``count`` items per lot, or ``count`` items when there are no lots."""
        return tender.items_data(count=int(count), lots=lots, quantity=quantity, **overrides)

    @keyword("Дані Етапів")
    def milestones_data(self, lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        """Payment and delivery milestones, per lot when there are lots."""
        return tender.milestones_data(lots)

    @keyword("Дані Конфігу Закупівлі")
    def tender_config_data(
        self,
        procedure: str | None = None,
        base: dict[str, Any] | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """
        The config block of a tender, with the named options changed.

        Named without a procedure it is an above threshold config; named with
        one it is that procedure's defaults, taken from its config schema.
        """
        return tender.tender_config_data(procedure, base, **overrides)

    @keyword("Дані Конфігу Звітування")
    def reporting_config_data(self, **overrides: Any) -> dict[str, Any]:
        """The config block of a reporting tender, with the named options changed."""
        return tender.tender_config_data(tender.REPORTING_CONFIG, **overrides)

    @keyword("Дані Закупівлі")
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

    @keyword("Дані Закупівлі Звітування")
    def reporting_tender_data(self, amount: float = 500000, **overrides: Any) -> dict[str, Any]:
        """A reporting tender: limited procedure, no bids, no auction."""
        return tender.reporting_tender_data(amount=amount, **overrides)

    @keyword("Дані Зміни Закупівлі")
    def tender_patch_data(self, status: str, **overrides: Any) -> dict[str, Any]:
        """A patch that moves the tender to a status."""
        return tender.tender_patch_data(status, **overrides)

    # --- criteria

    @keyword("Дані Критеріїв")
    def criteria_data(
        self,
        lots: list[dict[str, Any]] | None = None,
        include: list[str] | None = None,
        exclude: list[str] | None = None,
        folder: str = "aboveThreshold",
        related_item: str | None = None,
    ) -> dict[str, Any]:
        """
        The criteria of a tender, with fresh requirement ids.

        ``folder`` names the data folder whose set to build, since which
        criteria a procedure accepts is decided by the procedure. Lot related
        criteria are repeated for every lot.
        """
        return criteria.criteria_data(
            lots=lots,
            include=include,
            exclude=exclude,
            folder=folder,
            related_item=related_item,
        )

    @keyword("Дані Підстав Для Відмови В Участі")
    def exclusion_criteria_data(self, lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        """Grounds for refusing a bidder."""
        return criteria.exclusion_criteria(lots)

    @keyword("Дані Кваліфікаційних Критеріїв")
    def selection_criteria_data(self, lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        """Qualification criteria: equipment, staff, experience, finances."""
        return criteria.selection_criteria(lots)

    @keyword("Дані Інших Критеріїв")
    def other_criteria_data(self, lots: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        """Language, guarantees and bid validity period."""
        return criteria.other_criteria(lots)

    @keyword("Дані Критерію")
    def criterion_data(
        self, classification_id: str, related_item: str | None = None, **overrides: Any
    ) -> dict[str, Any]:
        """One criterion by its classification id."""
        return criteria.criterion(classification_id, related_item=related_item, **overrides)

    @keyword("Дані Відповідей На Вимоги")
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

    @keyword("Дані Пропозиції")
    def bid_data(
        self,
        tender_data: dict[str, Any],
        amount: float | None = None,
        amounts: list[float] | None = None,
        documents: list[dict[str, Any]] | None = None,
        eligibility_documents: list[dict[str, Any]] | None = None,
        financial_documents: list[dict[str, Any]] | None = None,
        qualification_documents: list[dict[str, Any]] | None = None,
        parameters: list[dict[str, Any]] | None = None,
        lot_ids: list[str] | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """A draft bid, offering every lot of the tender or only the ones named."""
        return bid_module.bid_data(
            tender_data,
            amount=amount,
            amounts=amounts,
            parameters=parameters,
            lot_ids=lot_ids,
            documents=documents,
            eligibility_documents=eligibility_documents,
            financial_documents=financial_documents,
            qualification_documents=qualification_documents,
            **overrides,
        )

    @keyword("Дані Зміни Пропозиції")
    def bid_patch_data(self, status: str = "pending", **overrides: Any) -> dict[str, Any]:
        """A patch that moves the bid to a status."""
        return bid_module.bid_patch_data(status=status, **overrides)

    # --- questions

    @keyword("Дані Звернення")
    def question_data(
        self,
        question_of: str = "tender",
        related_item: str | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """A supplier question about the tender, a lot or an item."""
        return question.question_data(question_of=question_of, related_item=related_item, **overrides)

    @keyword("Дані Відповіді На Звернення")
    def question_answer_data(self, answer: str | None = None, **overrides: Any) -> dict[str, Any]:
        """The tender owner's answer to a question."""
        return question.question_answer_data(answer=answer, **overrides)

    # --- claims and complaints

    @keyword("Дані Вимоги")
    def claim_data(self, **overrides: Any) -> dict[str, Any]:
        """A draft claim, addressed to the tender owner."""
        return complaint.claim_data(**overrides)

    @keyword("Дані Подання Вимоги")
    def claim_submit_data(self, **overrides: Any) -> dict[str, Any]:
        """The claimant submits the draft."""
        return complaint.claim_submit_data(**overrides)

    @keyword("Дані Відповіді На Вимогу")
    def claim_answer_data(self, resolution_type: str = "resolved", **overrides: Any) -> dict[str, Any]:
        """The tender owner's answer: invalid, resolved or declined."""
        return complaint.claim_answer_data(resolution_type=resolution_type, **overrides)

    @keyword("Дані Вирішення Вимоги")
    def claim_resolution_data(self, satisfied: bool = True, **overrides: Any) -> dict[str, Any]:
        """The claimant says whether the answer settled it."""
        return complaint.claim_resolution_data(satisfied=satisfied, **overrides)

    @keyword("Дані Скасування Вимоги")
    def claim_cancel_data(self, **overrides: Any) -> dict[str, Any]:
        """The claimant withdraws the claim."""
        return complaint.claim_cancel_data(**overrides)

    @keyword("Дані Скарги")
    def complaint_data(
        self,
        related_item: str,
        relates_to: str = "tender",
        **overrides: Any,
    ) -> dict[str, Any]:
        """A draft complaint for the reviewers, objecting to something."""
        return complaint.complaint_data(related_item, relates_to=relates_to, **overrides)

    @keyword("Дані Заперечення")
    def objection_data(self, related_item: str, relates_to: str = "tender", **overrides: Any) -> dict[str, Any]:
        """One objection: what is wrong and what remedy is asked for."""
        return complaint.objection_data(related_item, relates_to=relates_to, **overrides)

    @keyword("Дані Подання Скарги")
    def complaint_submit_data(self, **overrides: Any) -> dict[str, Any]:
        """The bot moves a paid complaint on to the reviewers."""
        return complaint.complaint_submit_data(**overrides)

    @keyword("Дані Прийняття Скарги")
    def complaint_accept_data(self, **overrides: Any) -> dict[str, Any]:
        """A reviewer takes the complaint on."""
        return complaint.complaint_accept_data(**overrides)

    @keyword("Дані Рішення По Скарзі")
    def complaint_decision_data(self, status: str = "satisfied", **overrides: Any) -> dict[str, Any]:
        """The reviewers decide: satisfied, declined or stopped."""
        return complaint.complaint_decision_data(status=status, **overrides)

    @keyword("Дані Виконання Рішення По Скарзі")
    def complaint_resolution_data(self, **overrides: Any) -> dict[str, Any]:
        """The tender owner says what they did about a satisfied complaint."""
        return complaint.complaint_resolution_data(**overrides)

    @keyword("Дані Відхилення Скарги")
    def complaint_rejection_data(self, status: str, reject_reason: str, **overrides: Any) -> dict[str, Any]:
        """The reviewers end it without deciding it: stopped or invalid, with a reason."""
        return complaint.complaint_rejection_data(status, reject_reason, **overrides)

    @keyword("Дані Помилкової Скарги")
    def complaint_mistaken_data(self, **overrides: Any) -> dict[str, Any]:
        """The complainant withdraws it as raised by mistake."""
        return complaint.complaint_mistaken_data(**overrides)

    @keyword("Дані Повідомлення У Скарзі")
    def complaint_post_data(
        self,
        related_objection: str,
        recipient: str = "complaint_owner",
        related_post: str | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """One message in the exchange around a complaint."""
        return complaint.complaint_post_data(
            related_objection,
            recipient=recipient,
            related_post=related_post,
            **overrides,
        )

    # --- cancellation

    @keyword("Дані Скасування")
    def cancellation_data(
        self,
        reason_type: str = "noDemand",
        related_lot: str | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """A draft cancellation, of the whole tender or of one lot."""
        return cancellation.cancellation_data(reason_type=reason_type, related_lot=related_lot, **overrides)

    @keyword("Дані Протоколу Скасування")
    def cancellation_report_data(self, title: str = "cancellation_report.p7s", **overrides: Any) -> dict[str, Any]:
        """The signed report a cancellation must carry before it is submitted."""
        return cancellation.cancellation_report_data(title=title, **overrides)

    @keyword("Дані Зміни Скасування")
    def cancellation_patch_data(self, status: str, **overrides: Any) -> dict[str, Any]:
        """A patch that moves the cancellation to a status."""
        return cancellation.cancellation_patch_data(status, **overrides)

    # --- award

    @keyword("Дані Переможця")
    def award_data(self, amount: float = 475000, **overrides: Any) -> dict[str, Any]:
        """An award created by the procuring entity in a limited procedure."""
        return award_module.award_data(amount=amount, **overrides)

    @keyword("Дані Кваліфікації Переможця")
    def award_qualification_data(self, qualified: bool = True, **overrides: Any) -> dict[str, Any]:
        """The decision that the bidder meets the criteria."""
        return award_module.award_qualification_data(qualified=qualified, **overrides)

    @keyword("Дані Зміни Переможця")
    def award_patch_data(self, status: str, **overrides: Any) -> dict[str, Any]:
        """A patch that moves the award to a status."""
        return award_module.award_patch_data(status, **overrides)

    # --- contract

    @keyword("Дані Активації Договору")
    def contract_active_data(
        self,
        contract_data: dict[str, Any],
        amount: float | None = None,
        **overrides: Any,
    ) -> dict[str, Any]:
        """The signed contract: number, period, value and item prices."""
        return contract.contract_active_data(contract_data, amount=amount, **overrides)

    @keyword("Дані Підпису Договору")
    def contract_signature_data(self, title: str, **overrides: Any) -> dict[str, Any]:
        """One side's signature on an electronic contract."""
        return contract.contract_signature_data(title, **overrides)

    @keyword("Дані Скасування Договору")
    def contract_cancellation_data(self, reason: str, **overrides: Any) -> dict[str, Any]:
        """Cancelling a contract or an amendment, with the reason for it."""
        return contract.contract_cancellation_data(reason, **overrides)

    @keyword("Дані Вартості Договору")
    def contract_value_data(self, amount: float, **overrides: Any) -> dict[str, Any]:
        """A change of the agreed value of an active contract."""
        return contract.contract_value_data(amount, **overrides)

    @keyword("Дані Зміни До Договору")
    def contract_change_data(self, rationale_type: str = "itemPriceChange", **overrides: Any) -> dict[str, Any]:
        """An amendment to an active contract."""
        return contract.contract_change_data(rationale_type=rationale_type, **overrides)

    @keyword("Дані Активації Зміни До Договору")
    def contract_change_active_data(self, contract_data: dict[str, Any], **overrides: Any) -> dict[str, Any]:
        """The signature that makes an amendment take effect."""
        return contract.contract_change_active_data(contract_data, **overrides)

    @keyword("Дані Завершення Договору")
    def contract_terminated_data(self, amount: float, **overrides: Any) -> dict[str, Any]:
        """Closing the contract, stating how much of it was paid."""
        return contract.contract_terminated_data(amount, **overrides)

    # --- composition

    @keyword("Обʼєднати Дані")
    def merge_data(self, base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
        """``patch`` merged into ``base``, dictionary by dictionary."""
        return deep_merge(base, patch)

    @keyword("Змінити Дані")
    def patch_data(self, base: dict[str, Any], **overrides: Any) -> dict[str, Any]:
        """``base`` with dotted overrides applied, e.g. ``value.amount=100``."""
        return apply_overrides(base, overrides)
