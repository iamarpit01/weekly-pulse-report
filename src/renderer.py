from typing import List, Dict, Any

def render_doc_payload(summaries: List[Dict[str, Any]], iso_week: str) -> str:
    """
    Renders a structured Markdown payload suitable for the Google Doc report.
    Adds a stable anchor for idempotency checks in the MCP Delivery phase.
    """
    lines = []
    
    # Stable anchor for idempotency checks
    lines.append(f"# [Week {iso_week}] Groww Pulse Report")
    lines.append("")
    lines.append("This report contains the automated clustering and summarization of recent Google Play Store reviews for Groww.")
    lines.append("---")
    lines.append("")
    
    if not summaries:
        lines.append("No significant themes were found for this period.")
        return "\n".join(lines)
        
    for idx, summary in enumerate(summaries, 1):
        theme_name = summary.get('theme_name', 'Unknown Theme')
        review_count = summary.get('review_count', 0)
        
        lines.append(f"## {idx}. {theme_name} ({review_count} related reviews)")
        lines.append("")
        
        # Actionable Ideas
        ideas = summary.get('actionable_ideas', [])
        if ideas:
            lines.append("### Actionable Recommendations")
            for idea in ideas:
                lines.append(f"- {idea}")
            lines.append("")
            
        # Verbatim Quotes (Already validated against hallucinations)
        quotes = summary.get('verbatim_quotes', [])
        if quotes:
            lines.append("### Verbatim Quotes from Users")
            for quote in quotes:
                lines.append(f"> \"{quote}\"")
            lines.append("")
            
        lines.append("---")
        lines.append("")
        
    return "\n".join(lines)

def render_email_payload(summaries: List[Dict[str, Any]], iso_week: str, doc_link: str = "{{DOC_LINK}}") -> str:
    """
    Renders a concise HTML email payload highlighting the top themes.
    Includes a placeholder for the Google Doc link which is populated after the Doc is updated.
    """
    html = [
        f"<h2>Groww Play Store Review Pulse - Week {iso_week}</h2>",
        "<p>Here are the top themes emerging from this week's Play Store reviews:</p>",
        "<ul>"
    ]
    
    if not summaries:
        html.append("<li>No significant themes detected this week.</li>")
    else:
        # Just show the top 5 themes so the email isn't overwhelming
        top_summaries = summaries[:5]
        for summary in top_summaries:
            theme = summary.get('theme_name', 'Unknown')
            count = summary.get('review_count', 0)
            html.append(f"<li><b>{theme}</b> ({count} reviews)</li>")
            
        if len(summaries) > 5:
            html.append(f"<li><i>...and {len(summaries) - 5} more smaller themes.</i></li>")
            
    html.extend([
        "</ul>",
        "<br/>",
        f"<p><a href='{doc_link}'>Click here to read the full report</a> including actionable recommendations and verbatim user quotes.</p>",
        "<p><i>This is an automated report.</i></p>"
    ])
    
    return "\n".join(html)
