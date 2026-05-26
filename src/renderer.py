import os
from datetime import datetime, timedelta, timezone
from jinja2 import Environment, FileSystemLoader

KST = timezone(timedelta(hours=9))
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")


def render(summaries: list[dict]) -> tuple[str, str]:
    date_str = datetime.now(KST).strftime("%Y-%m-%d")
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("newsletter.html")
    html = template.render(date=date_str, summaries=summaries)
    filename = f"{date_str}.html"
    return html, filename
