#!/usr/bin/env python3
"""Generate index.html from resume.md and index.template.html."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESUME_PATH = ROOT / "resume.md"
TEMPLATE_PATH = ROOT / "index.template.html"
OUTPUT_PATH = ROOT / "index.html"

SECTION_MAP = {
    "Professional Summary": ("summary", "Professional Summary", "panel-summary", "tab-summary", True),
    "Core Competencies": ("competencies", "Core Competencies", "panel-competencies", "tab-competencies", False),
    "Work Experience": ("experience", "Work Experience", "panel-experience", "tab-experience", False),
    "Technical Skills": ("skills", "Technical Skills", "panel-skills", "tab-skills", False),
    "Domain & Industry Skills": ("domain", "Domain & Industry", "panel-domain", "tab-domain", False),
    "Domain & Industry": ("domain", "Domain & Industry", "panel-domain", "tab-domain", False),
    "Education": ("education", "Education", "panel-education", "tab-education", False),
}


def esc(text: str, *, quote: bool = True) -> str:
    return html.escape(text.strip(), quote=quote)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("\n", 1)
    if len(parts) < 2:
        return {}, text
    rest = parts[1]
    if "---" not in rest:
        return {}, text
    fm_block, body = rest.split("---", 1)
    meta: dict[str, str] = {}
    for line in fm_block.strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, body.lstrip("\n")


def split_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    chunks: list[str] = []

    for line in body.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(chunks).strip()
            current = line[3:].strip()
            chunks = []
        elif current is not None:
            chunks.append(line)

    if current is not None:
        sections[current] = "\n".join(chunks).strip()

    return sections


def strip_separators(text: str) -> str:
    lines = [ln for ln in text.splitlines() if ln.strip() not in ("---", "")]
    return "\n".join(lines).strip()


def parse_contact_line(line: str) -> dict[str, str]:
    parts = [p.strip() for p in line.split("·")]
    location = re.sub(r"^\*\*|\*\*$", "", parts[0]) if parts else ""
    phone = parts[1] if len(parts) > 1 else ""
    email = parts[2] if len(parts) > 2 else ""
    linkedin_label = "LinkedIn"
    linkedin_url = ""
    if len(parts) > 3:
        link_match = re.search(r"\[([^\]]+)\]\(([^)]+)\)", parts[3])
        if link_match:
            linkedin_label = link_match.group(1)
            linkedin_url = link_match.group(2)
    return {
        "location": location.strip("* "),
        "phone": phone,
        "email": email,
        "linkedin_label": linkedin_label,
        "linkedin_url": linkedin_url,
    }


def phone_href(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        digits = "1" + digits
    return f"+{digits}" if digits else ""


def contact_row_html(contact: dict[str, str]) -> str:
    loc = esc(contact["location"])
    phone = esc(contact["phone"])
    email = esc(contact["email"])
    tel = phone_href(contact["phone"])
    linkedin_url = esc(contact["linkedin_url"], quote=True)
    linkedin_label = esc(contact["linkedin_label"])

    pin = (
        '<svg class="contact-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>'
    )
    phone_icon = (
        '<svg class="contact-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>'
    )
    mail_icon = (
        '<svg class="contact-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>'
    )
    li_icon = (
        '<svg class="contact-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>'
    )

    rows = [
        f'<span class="contact-item">{pin} {loc}</span>',
        f'<span class="contact-item">{phone_icon} <a href="tel:{esc(tel, quote=True)}">{phone}</a></span>',
        f'<span class="contact-item">{mail_icon} <a href="mailto:{email}">{email}</a></span>',
    ]
    if linkedin_url:
        rows.append(
            f'<span class="contact-item">{li_icon} '
            f'<a href="{linkedin_url}" target="_blank" rel="noopener noreferrer">{linkedin_label}</a></span>'
        )
    return "\n            ".join(rows)


def bullet_text(raw: str) -> tuple[str, bool]:
    text = raw.strip()
    highlight = False
    m = re.match(r"^\*\*(.+)\*\*$", text)
    if m:
        highlight = True
        text = m.group(1)
    return text, highlight


def render_summary(section: str, panel_id: str, tab_id: str, active: bool) -> str:
    text = strip_separators(section)
    active_class = " active" if active else ""
    return f"""        <section class="section tab-panel{active_class}" role="tabpanel" id="{panel_id}" aria-labelledby="{tab_id}">
          <h2 class="section-title" id="{panel_id.replace('panel-', '')}-heading">Professional Summary</h2>
          <p class="section-text">
            {esc(text)}
          </p>
        </section>"""


def render_competencies(section: str, panel_id: str, tab_id: str) -> str:
    items = []
    for line in section.splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(f"            <li>{esc(line[2:])}</li>")
    return f"""        <section class="section tab-panel" role="tabpanel" id="{panel_id}" aria-labelledby="{tab_id}">
          <h2 class="section-title" id="competencies-heading">Core Competencies</h2>
          <ul class="competency-grid">
{chr(10).join(items)}
          </ul>
        </section>"""


def render_experience(section: str, panel_id: str, tab_id: str) -> str:
    jobs_html: list[str] = []
    current_company = ""
    current_role = ""
    current_dates = ""
    bullets: list[str] = []

    def flush_job() -> None:
        nonlocal bullets, current_company, current_role, current_dates
        if not current_company:
            return
        bullet_lines = []
        for b in bullets:
            text, highlight = bullet_text(b)
            cls = ' class="highlight"' if highlight else ""
            bullet_lines.append(f"              <li{cls}>{esc(text)}</li>")
        jobs_html.append(
            f"""          <article class="job">
            <div class="job-header">
              <span class="job-company">{esc(current_company)}</span>
              <span class="job-dates">{esc(current_dates)}</span>
            </div>
            <p class="job-role">{esc(current_role)}</p>
            <ul class="job-bullets">
{chr(10).join(bullet_lines)}
            </ul>
          </article>"""
        )
        bullets = []

    for line in section.splitlines():
        if line.startswith("### "):
            flush_job()
            current_company = line[4:].strip()
            current_role = ""
            current_dates = ""
        elif line.strip().startswith("**") and "·" in line:
            role_part, dates_part = line.strip().split("·", 1)
            current_role = role_part.strip().strip("*")
            current_dates = dates_part.strip()
        elif line.strip().startswith("- "):
            bullets.append(line.strip()[2:])

    flush_job()

    return f"""        <section class="section tab-panel" role="tabpanel" id="{panel_id}" aria-labelledby="{tab_id}">
          <h2 class="section-title" id="experience-heading">Work Experience</h2>

{chr(10).join(jobs_html)}
        </section>"""


def parse_skills_table(section: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 2:
            continue
        if cells[0].lower() == "category" or set(cells[0]) <= {"-", " "}:
            continue
        category = re.sub(r"^\*\*|\*\*$", "", cells[0])
        tech = re.sub(r"^\*\*|\*\*$", "", cells[1])
        rows.append((category, tech))
    return rows


def render_skills(section: str, panel_id: str, tab_id: str) -> str:
    cards = []
    for category, tech in parse_skills_table(section):
        cards.append(
            f"""            <div class="skill-category">
              <h4>{esc(category)}</h4>
              <p>{esc(tech)}</p>
            </div>"""
        )
    return f"""        <section class="section tab-panel" role="tabpanel" id="{panel_id}" aria-labelledby="{tab_id}">
          <h2 class="section-title" id="skills-heading">Technical Skills</h2>
          <div class="skills-grid">
{chr(10).join(cards)}
          </div>
        </section>"""


def render_domain(section: str, panel_id: str, tab_id: str) -> str:
    tags = []
    for line in section.splitlines():
        line = line.strip()
        if line.startswith("- "):
            tags.append(f"            <li>{esc(line[2:])}</li>")
    return f"""        <section class="section tab-panel" role="tabpanel" id="{panel_id}" aria-labelledby="{tab_id}">
          <h2 class="section-title" id="domain-heading">Domain &amp; Industry</h2>
          <ul class="tag-list">
{chr(10).join(tags)}
          </ul>
        </section>"""


def render_education(section: str, panel_id: str, tab_id: str) -> str:
    lines = [ln.strip() for ln in strip_separators(section).splitlines() if ln.strip()]
    degree = re.sub(r"^\*\*|\*\*$", "", lines[0]) if lines else ""
    school = lines[1] if len(lines) > 1 else ""
    return f"""        <section class="section tab-panel" role="tabpanel" id="{panel_id}" aria-labelledby="{tab_id}">
          <h2 class="section-title" id="education-heading">Education</h2>
          <div class="education-item">
            <h3>{esc(degree)}</h3>
            <p>{esc(school)}</p>
          </div>
        </section>"""


def render_sections(sections: dict[str, str]) -> str:
    parts: list[str] = []
    first = True
    order = [
        "Professional Summary",
        "Core Competencies",
        "Work Experience",
        "Technical Skills",
        "Domain & Industry Skills",
        "Domain & Industry",
        "Education",
    ]
    seen: set[str] = set()

    for title in order:
        if title in seen or title not in sections:
            continue
        seen.add(title)
        _, heading, panel_id, tab_id, is_first_panel = SECTION_MAP[title]
        body = sections[title]

        if title == "Professional Summary":
            parts.append(render_summary(body, panel_id, tab_id, first))
        elif title == "Core Competencies":
            parts.append(render_competencies(body, panel_id, tab_id))
        elif title == "Work Experience":
            parts.append(render_experience(body, panel_id, tab_id))
        elif title == "Technical Skills":
            parts.append(render_skills(body, panel_id, tab_id))
        elif title.startswith("Domain"):
            parts.append(render_domain(body, panel_id, tab_id))
        elif title == "Education":
            parts.append(render_education(body, panel_id, tab_id))

        if first:
            first = False

    return "\n\n".join(parts)


def parse_resume(md: str) -> dict:
    meta, body = parse_frontmatter(md)
    lines = body.splitlines()
    name = ""
    contact_line = ""
    content_start = 0

    for i, line in enumerate(lines):
        if line.startswith("# "):
            name = line[2:].strip()
            content_start = i + 1
            break

    for j in range(content_start, len(lines)):
        line = lines[j].strip()
        if not line:
            continue
        if line.startswith("## "):
            body = "\n".join(lines[j:])
            break
        if "·" in line or "@" in line:
            contact_line = line
            body = "\n".join(lines[j + 1 :])
            break

    sections = split_sections(body)
    contact = parse_contact_line(contact_line) if contact_line else {}

    tagline = meta.get("tagline", "Quality Engineering & DevSecOps Leader")
    page_title = meta.get("page_title", f"{name} | Quality Engineering & DevSecOps")
    meta_description = meta.get(
        "meta_description",
        f"{name} — Quality Engineering & DevSecOps professional specializing in test automation, SAST/DAST, and CI/CD transformation.",
    )

    return {
        "name": name,
        "tagline": tagline,
        "page_title": page_title,
        "meta_description": meta_description,
        "contact": contact,
        "sections": sections,
    }


def generate() -> None:
    if not RESUME_PATH.exists():
        sys.exit(f"Missing {RESUME_PATH}")
    if not TEMPLATE_PATH.exists():
        sys.exit(f"Missing {TEMPLATE_PATH}")

    data = parse_resume(RESUME_PATH.read_text(encoding="utf-8"))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    output = (
        template.replace("{{NAME}}", esc(data["name"]))
        .replace("{{TAGLINE}}", esc(data["tagline"]))
        .replace("{{PAGE_TITLE}}", esc(data["page_title"]))
        .replace("{{META_DESCRIPTION}}", esc(data["meta_description"]))
        .replace("{{CONTACT_ROW}}", contact_row_html(data["contact"]))
        .replace("{{CONTENT_SECTIONS}}", render_sections(data["sections"]))
    )

    OUTPUT_PATH.write_text(output, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    generate()
