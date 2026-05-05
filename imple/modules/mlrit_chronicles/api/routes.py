"""
routes.py — MLRIT Chronicles Flask Blueprint
Registered in app.py under url_prefix='/api/chronicles'

Endpoints:
  GET /api/chronicles                    — paginated list, sorted by date desc
  GET /api/chronicles?q=keyword          — filtered by keyword
  GET /api/chronicles?page=1&limit=20    — pagination
  GET /api/chronicles/latest             — 5 most recent articles
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, request, jsonify, current_app

logger = logging.getLogger(__name__)

chronicles_bp = Blueprint("chronicles", __name__)

# ── Path to news.json (relative to this file) ──────────────────────────────
_DATA_PATH = Path(__file__).parent.parent / "data" / "news.json"


# ══════════════════════════════════════════════════════════════════════════
# DATA ACCESS HELPERS
# ══════════════════════════════════════════════════════════════════════════

def _parse_date(date_str: str) -> datetime:
    """Parse ISO 8601 date string; return epoch on failure."""
    try:
        return datetime.fromisoformat(str(date_str).replace("Z", "+00:00"))
    except Exception:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


def _load_articles() -> list:
    """
    Load articles from MongoDB (preferred) or news.json fallback.
    Falls back to JSON if MongoDB collection is empty or unavailable.
    Always returns a list — never raises.
    """
    db = getattr(current_app, "db", None)

    # Try MongoDB first — but only if collection has data
    if db is not None:
        try:
            docs = list(db["chronicles"].find({}, {"_id": 0}).sort("date", -1))
            if docs:  # Only use MongoDB if it actually has articles
                return docs
            # MongoDB empty — fall through to JSON
        except Exception as exc:
            logger.warning("[Chronicles API] MongoDB read failed, falling back to JSON: %s", exc)

    # JSON fallback
    try:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        articles = data.get("articles", [])
        # Sort by date descending
        articles.sort(
            key=lambda a: _parse_date(str(a.get("date") or "")),
            reverse=True,
        )
        return articles
    except FileNotFoundError:
        return []
    except Exception as exc:
        logger.error("[Chronicles API] Failed to read news.json: %s", exc)
        return []


def _filter_articles(articles: list, q: str) -> list:
    """
    Case-insensitive keyword filter across title, summary, and keywords array.
    Empty q returns all articles.
    """
    if not q or not q.strip():
        return articles
    q_lower = q.strip().lower()
    result = []
    for article in articles:
        title    = str(article.get("title",   "") or "").lower()
        summary  = str(article.get("summary", "") or "").lower()
        keywords = " ".join(article.get("keywords", []) or []).lower()
        if q_lower in title or q_lower in summary or q_lower in keywords:
            result.append(article)
    return result


def _paginate(articles: list, page: int, limit: int):
    """Return (page_slice, total, pages)."""
    total  = len(articles)
    pages  = max(1, (total + limit - 1) // limit)
    start  = (page - 1) * limit
    end    = start + limit
    return articles[start:end], total, pages


# ══════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════

@chronicles_bp.route("", methods=["GET"])
@chronicles_bp.route("/", methods=["GET"])
def list_chronicles():
    """
    GET /api/chronicles
    Query params:
      q     — keyword filter (optional)
      page  — page number, default 1
      limit — articles per page, default 20
    """
    q     = (request.args.get("q")     or "").strip()
    page  = request.args.get("page",  1)
    limit = request.args.get("limit", 20)

    # Validate pagination params
    try:
        page  = int(page)
        limit = int(limit)
        if page < 1 or limit < 1 or limit > 100:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid pagination parameters"}), 400

    articles = _load_articles()
    filtered = _filter_articles(articles, q)
    page_slice, total, pages = _paginate(filtered, page, limit)

    return jsonify({
        "articles": page_slice,
        "total":    total,
        "page":     page,
        "limit":    limit,
        "pages":    pages,
    }), 200


@chronicles_bp.route("/latest", methods=["GET"])
def latest_chronicles():
    """
    GET /api/chronicles/latest
    Returns the 5 most recent articles.
    """
    articles = _load_articles()
    return jsonify({
        "articles": articles[:5],
        "total":    min(5, len(articles)),
    }), 200
