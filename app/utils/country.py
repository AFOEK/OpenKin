def iso2_to_flag(code: str) -> str:
    if not code or len(code) != 2:
        return ''
    base = 127397
    return ''.join(chr(base + ord(c.upper())) for c in code)