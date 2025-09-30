import pathlib, sys, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag.reporting import (
    generate_daily_report, generate_social_post,
    render_social_card_svg, schedule_post, load_queue
)  # noqa: E402


def test_report_and_social_post_happy_path(tmp_path):
    md = generate_daily_report({"visitors": 123, "signups": 5}, ["Launched demo"], date_str="2025-01-01")
    assert "Daily Report" in md and "| visitors | 123 |" in md
    post = generate_social_post(md)
    assert isinstance(post, str) and len(post) <= 280 and "Daily update" in post


def test_svg_and_scheduler(tmp_path):
    svg_path = tmp_path / "card.svg"
    p = render_social_card_svg("Daily Report", "visitors: 123", str(svg_path))
    assert svg_path.exists()
    assert svg_path.read_text(encoding="utf-8").lstrip().startswith("<svg")
    qpath = tmp_path / "queue.json"
    entry = schedule_post("Hello world", "2025-01-01T09:00:00Z", assets=[str(svg_path)], queue_path=str(qpath))
    assert qpath.exists() and "Hello world" in json.dumps(entry)
    q = load_queue(str(qpath))
    assert isinstance(q, list) and len(q) == 1 and q[0]["assets"]
