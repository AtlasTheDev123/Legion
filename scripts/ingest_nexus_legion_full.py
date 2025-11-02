"""Ingest script: scans `schemas/` and `registry/` and optionally inserts into MongoDB.
Usage: set MONGO_URI env var to enable DB writes; otherwise script prints what it would insert.
"""
import os
import json
from pathlib import Path

SCHEMAS_DIR = Path('schemas')
REGISTRY = Path('registry/tool_registry.json')

def load_all_schemas():
    out = []
    for p in SCHEMAS_DIR.glob('functions_chunk_*.json'):
        try:
            out += json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            continue
    return out


def load_registry():
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text(encoding='utf-8'))
    return []


def main():
    schemas = load_all_schemas()
    registry = load_registry()
    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        print('MONGO_URI not set — dry run')
        print(f'Would ingest {len(schemas)} functions and {len(registry)} registry entries')
        return
    try:
        from pymongo import MongoClient
    except Exception as e:
        print('pymongo not installed; aborting DB ingest:', e)
        return
    client = MongoClient(mongo_uri)
    db = client.get_database()
    db.functions.delete_many({})
    if schemas:
        db.functions.insert_many(schemas)
    db.tool_registry.delete_many({})
    if registry:
        db.tool_registry.insert_many(registry)
    print('Ingest completed')

if __name__ == '__main__':
    main()
