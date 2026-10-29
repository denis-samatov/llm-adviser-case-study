"""Authored synthetic provenance contract; not the private platform or an LLM run."""

import hashlib
import json


def build_manifest(source: str) -> dict:
    source_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()
    chunks = []
    offset = 0
    for line in source.splitlines(keepends=True):
        text = line.rstrip("\r\n")
        if text.strip():
            end = offset + len(text)
            identifier = hashlib.sha256(f"{source_hash}:{offset}:{end}".encode()).hexdigest()
            chunks.append({"id": identifier, "start": offset, "end": end, "text": text})
        offset += len(line)
    if not chunks:
        raise ValueError("Source must contain a nonempty passage")
    return {"source_id": "authored-synthetic-example", "source_sha256": source_hash,
            "offset_unit": "unicode_characters", "chunks": chunks}


if __name__ == "__main__":
    print(json.dumps(build_manifest("Retry policy: up to three attempts.\nOwner: demo team.\n"), indent=2))
