import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv(Path(__file__).with_name('.env.local'))


def connect_db():
    if not os.getenv('PGDATABASE') or not os.getenv('PGUSER'):
        raise RuntimeError('Set PGDATABASE and PGUSER in .env.local')
    return psycopg.connect(connect_timeout=5, row_factory=dict_row)
