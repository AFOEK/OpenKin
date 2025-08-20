from flask import Blueprint, jsonify
import pycountry
from app.utils.country import iso2_to_flag

public_bp = Blueprint("public", __name__)

@public_bp.get("/countries")
def countries():
    items = []
    for c in pycountry.countries:
        code = getattr(c, "alpha_2", None)
        name = getattr(c, "name", None)
        if not code or not name:
            continue
        items.append({
            "code":code,
            "name":name,
            "flag":iso2_to_flag(code)
        })

    return jsonify(items)