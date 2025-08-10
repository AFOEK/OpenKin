import re
from pathlib import Path
from typing import Optional, Iterable
import opencc
from sqlalchemy import text

CH_SURNAME_START = re.compile(r'^[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]')
LATIN_START = re.compile(r'[A-Za-z]')

_cc_t2s = opencc.OpenCC('t2s.json')

_COMPOUND: set[str] = set()
def load_compound_surnames(path: str | Path) -> None:
    global _COMPOUND
    p = Path(path)
    if p.exists():
        _COMPOUND = {line.strip() for line in p.read_text(encoding='utf-8').splitlines() if line.strip()}
    else:
        _COMPOUND = set()

load_compound_surnames(Path(__file__).resolve().parents[2] / 'data' / 'compound_surname.txt')

def normalize_chinese(text: str) -> str:
    return _cc_t2s.convert(text)

def is_chinese_name(name: Optional[str]) -> bool:
    if not name:
        return False
    return bool(CH_SURNAME_START.match(name.strip()))

def detect_type(name: Optional[str]) -> str:
    if not name:
        return 'other'
    
    n = name.strip()
    if CH_SURNAME_START.match(n): return 'zh'
    if LATIN_START.match(n): return 'en'
    return 'other'

def extract_surname_chinese(name: str) -> Optional[str]:
    n = name.strip()
    n = normalize_chinese(n)
    if len(n) >= 2 and n[:2] in _COMPOUND:
        return n[:2]
    
    return n[0] if n else None

def get_parents(db, person_id: str) -> Iterable[dict]:
    sql = text("""
        SELECT p.*
        FROM "CoreDB".relationships r
        JOIN "CoreDB".persons p ON p.id = r.from_person_id
        WHERE r.relationships_type = 'parent'
        AND r.to_person_id = :child_id
    """)
    res = db.session.execute(sql, {"child_id": person_id}).mappings().all()
    return res

def pick_father_mother(parents: Iterable[dict]) -> tuple[Optional[dict], Optional[dict]]:
    father = mother = None

    for p in parents:
        if p.get('gender') == 0 and father is None:
            father = p
        elif p.get('gender') == 1 and mother is None:
            mother = p

    return father, mother

def clan_surname_for_person(db, person_row: dict) -> Optional[str]:
    cn = (person_row.get('chinese_name') or '').strip()
    if is_chinese_name(cn):
        return extract_surname_chinese(cn)
    
    person_id = str(person_row.get('id'))
    parents = list(get_parents(db, person_id))
    father, mother = pick_father_mother(parents)

    if father:
        fcn = (father.get('chinese_name') or '').strip()
        if is_chinese_name(fcn):
            return extract_surname_chinese(fcn)
        
    if mother:
        mcn = (mother.get('chinese_name') or '').strip()
        if is_chinese_name(mcn):
            return extract_surname_chinese(mcn)
        
    return None

def same_clan(db, a_row: dict, b_row: dict) -> bool:
    a = clan_surname_for_person(db, a_row)
    b = clan_surname_for_person(db, b_row)
    return bool(a and b and a == b)