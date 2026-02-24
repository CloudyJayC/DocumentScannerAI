"""
html_helpers.py — HTML Rendering Utilities

Provides functions to format analysis results as styled HTML for display
in the Qt results text edit widget.
"""


def render_section_header(title: str, color: str, icon: str = "") -> str:
    """
    Render a section header with icon, title, and horizontal rule.
    
    Args:
        title: Section title text
        color: CSS color for the title
        icon: Optional emoji/icon to display before title
    
    Returns:
        HTML string for the section header
    """
    return (
        f'<div style="margin-top:28px; margin-bottom:10px;">'
        f'<span style="color:{color}; font-size:9px; font-weight:700; '
        f'letter-spacing:2.5px; font-family:Segoe UI,sans-serif;">'
        f'{icon}&nbsp;&nbsp;{title.upper()}'
        f'</span>'
        f'<hr style="border:none; border-top:1px solid #1a2236; margin-top:6px; margin-bottom:0;">'
        f'</div>'
    )


def render_ok_line(text: str) -> str:
    """
    Render a success/ok message line in green.
    
    Args:
        text: Message text to display
    
    Returns:
        HTML string for success message
    """
    return f'<p style="color:#6ee7b7; font-size:11px; margin:4px 0 0 2px;">{text}</p>'


def render_warn_line(text: str) -> str:
    """
    Render a warning message line in yellow/amber.
    
    Args:
        text: Warning message text
    
    Returns:
        HTML string for warning message
    """
    return f'<p style="color:#fbbf24; font-size:11px; margin:3px 0 0 2px;">{text}</p>'


def render_error_line(text: str) -> str:
    """
    Render an error message line in red with bold text.
    
    Args:
        text: Error message text
    
    Returns:
        HTML string for error message
    """
    return f'<p style="color:#f87171; font-size:11px; font-weight:600; margin:3px 0 0 2px;">{text}</p>'


def render_ai_analysis(analysis: dict) -> str:
    """
    Render structured AI analysis results as formatted HTML.
    
    Displays:
    - Overall impression (summary paragraph)
    - Strengths (bulleted list)
    - Areas to improve/Weaknesses (bulleted list)
    - Key skills detected (bulleted list)
    - Recommendations (bulleted list)
    
    Args:
        analysis: Dictionary with keys: overall_impression, strengths,
                 weaknesses, key_skills, recommendations
    
    Returns:
        Complete HTML string for the AI analysis section
    """
    html = ""

    # Overall impression
    impression = analysis.get("overall_impression", "")
    if impression:
        html += (
            f'<p style="color:#e2e8f0; font-size:12px; line-height:1.7; '
            f'margin:0 0 16px 2px;">{impression}</p>'
        )

    def _subsection(title: str, color: str, items: list) -> str:
        """Render a subsection with title and bulleted items."""
        if not items:
            return ""
        out = (
            f'<p style="color:{color}; font-size:9px; font-weight:700; '
            f'letter-spacing:2px; margin:14px 0 6px 2px;">{title}</p>'
        )
        for item in items:
            out += (
                f'<p style="color:#94a3b8; font-size:11.5px; line-height:1.6; '
                f'margin:3px 0 3px 10px;">▸ &nbsp;{item}</p>'
            )
        return out

    html += _subsection(
        "STRENGTHS",
        "#6ee7b7",
        analysis.get("strengths", [])
    )
    html += _subsection(
        "AREAS TO IMPROVE",
        "#f87171",
        analysis.get("weaknesses", [])
    )
    html += _subsection(
        "KEY SKILLS DETECTED",
        "#7dd3fc",
        analysis.get("key_skills", [])
    )
    html += _subsection(
        "RECOMMENDATIONS",
        "#fbbf24",
        analysis.get("recommendations", [])
    )

    return html


def render_text_block(text: str) -> str:
    """
    Render plain text as formatted HTML with syntax highlighting for headers.
    
    Applies special formatting to:
    - All-caps short lines (rendered as headers in blue)
    - Regular text lines (rendered in monospace font)
    - Empty lines (preserved as breaks)
    
    Args:
        text: Plain text to render
    
    Returns:
        HTML string with formatted text
    """
    # Escape HTML special characters
    escaped = (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    
    lines_html = []
    for line in escaped.split("\n"):
        stripped = line.strip()
        if not stripped:
            lines_html.append("<br>")
        elif stripped.isupper() and len(stripped) < 40:
            # Format short all-caps lines as headers
            lines_html.append(
                f'<span style="color:#7dd3fc; font-weight:700; font-size:11px;">{line}</span><br>'
            )
        else:
            lines_html.append(f"{line}<br>")
    
    return (
        '<p style="font-family:Cascadia Code,Fira Code,Consolas,monospace; '
        'font-size:11.5px; color:#94a3b8; line-height:1.75; margin:6px 0 0 2px;">'
        + "".join(lines_html)
        + "</p>"
    )
