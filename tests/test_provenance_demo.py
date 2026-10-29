import unittest

from examples.provenance_demo import build_manifest


class ProvenanceContract(unittest.TestCase):
    def test_unicode_offsets_recover_exact_source_passages(self):
        source = "Синтетический источник.\r\n\r\nRetry limit: 3.\n"
        first = build_manifest(source)
        self.assertEqual(first, build_manifest(source))
        for chunk in first["chunks"]:
            self.assertEqual(source[chunk["start"]:chunk["end"]], chunk["text"])
        self.assertEqual(len(first["chunks"]), 2)

    def test_source_revision_changes_provenance_identity(self):
        a, b = build_manifest("Retry limit: 3."), build_manifest("Retry limit: 4.")
        self.assertNotEqual(a["source_sha256"], b["source_sha256"])
        self.assertNotEqual(a["chunks"][0]["id"], b["chunks"][0]["id"])

    def test_empty_source_is_not_publishable_evidence(self):
        with self.assertRaises(ValueError):
            build_manifest("\n\r\n")
