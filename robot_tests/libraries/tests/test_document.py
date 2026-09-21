"""Documents and the file content that is uploaded for them."""

from data.document import (
    SIGNATURE_CONTENT,
    contract_proforma_document_data,
    document_data,
    merge_contents,
    proposal_document_data,
    signature_document_data,
)


class TestDocumentData:
    def test_the_file_travels_next_to_the_payload_under_its_name(self):
        payload = document_data(title="report.txt", content="hello")
        assert payload["data"]["title"] == "report.txt"
        assert payload["contents"] == {"report.txt": "hello"}

    def test_content_is_generated_when_none_is_given(self):
        assert document_data(title="report.txt")["contents"]["report.txt"].strip()

    def test_document_type_appears_only_when_given(self):
        assert "documentType" not in document_data()["data"]
        assert document_data(document_type="notice")["data"]["documentType"] == "notice"


class TestTypedDocuments:
    def test_a_notice_is_a_signature(self):
        payload = signature_document_data(title="notice.p7s")
        assert payload["data"]["documentType"] == "notice"
        assert payload["contents"]["notice.p7s"] == SIGNATURE_CONTENT

    def test_a_proposal_keeps_the_extension_the_api_reads_the_format_from(self):
        # the API asks for a pkcs7 signature and decides by the file name
        payload = proposal_document_data()
        assert payload["data"]["documentType"] == "proposal"
        assert payload["data"]["title"].endswith(".p7s")

    def test_a_proforma_is_the_draft_contract(self):
        assert contract_proforma_document_data()["data"]["documentType"] == "contractProforma"


def test_merge_contents_collects_the_files_of_several_documents():
    payload = {}
    merge_contents(payload, [document_data(title="a.txt"), document_data(title="b.txt")])
    assert set(payload["contents"]) == {"a.txt", "b.txt"}
