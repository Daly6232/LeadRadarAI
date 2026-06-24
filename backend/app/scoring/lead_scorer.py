"""
Rule-based lead scoring engine.
Score 0–100 based on digital presence gaps.
High score = more opportunity for agency services.
"""
from typing import Dict, Tuple


def score_lead(data: Dict) -> Tuple[float, str, str, str]:
    """
    Returns (score, priority, explanation, outreach_strategy)
    """
    score = 0.0
    reasons = []
    opportunities = []

    # --- Website (30 points) ---
    if data.get("has_website"):
        score += 10
        reasons.append("✓ Has a website")
        if data.get("https_enabled"):
            score += 5
            reasons.append("✓ HTTPS enabled")
        else:
            opportunities.append("No HTTPS — security upgrade needed")
        if data.get("has_contact_page"):
            score += 5
            reasons.append("✓ Has contact page")
        else:
            opportunities.append("Missing contact page")
        if data.get("has_about_page"):
            score += 5
            reasons.append("✓ Has about page")
        else:
            opportunities.append("Missing about page")
        if data.get("has_services_page"):
            score += 5
            reasons.append("✓ Has services page")
        else:
            opportunities.append("Missing services page")
    else:
        score += 30  # No website = huge opportunity
        opportunities.append("No website — major opportunity for web design")
        reasons.append("✗ No website detected")

    # --- Contact info (20 points) ---
    if data.get("email"):
        score += 10
        reasons.append("✓ Email found")
    else:
        opportunities.append("No email found online")

    if data.get("phone"):
        score += 10
        reasons.append("✓ Phone found")
    else:
        opportunities.append("No phone number found online")

    # --- Social media (30 points) ---
    social_platforms = ["facebook", "instagram", "linkedin", "twitter", "tiktok", "youtube"]
    social_present = [p for p in social_platforms if data.get(p)]
    social_missing = [p for p in social_platforms if not data.get(p)]

    social_score = min(len(social_present) * 5, 20)
    score += social_score

    if social_present:
        reasons.append(f"✓ Present on: {', '.join(social_present)}")
    if social_missing:
        missing_key = [p for p in ["facebook", "instagram", "linkedin"] if p in social_missing]
        if missing_key:
            score += len(missing_key) * 3
            opportunities.append(f"Missing social media: {', '.join(missing_key)}")

    # --- Meta quality (10 points) ---
    if data.get("meta_title"):
        score += 5
        reasons.append("✓ Has meta title (SEO)")
    else:
        opportunities.append("No meta title — SEO gap")

    if data.get("meta_description"):
        score += 5
        reasons.append("✓ Has meta description (SEO)")
    else:
        opportunities.append("No meta description — SEO gap")

    # Cap score
    score = min(round(score, 1), 100.0)

    # Priority
    if score >= 70:
        priority = "High"
    elif score >= 40:
        priority = "Medium"
    else:
        priority = "Low"

    # Explanation
    explanation_parts = ["📊 Score Analysis:"]
    explanation_parts.extend(reasons)
    if opportunities:
        explanation_parts.append("\n🎯 Opportunities:")
        explanation_parts.extend([f"  • {o}" for o in opportunities])
    explanation = "\n".join(explanation_parts)

    # Outreach strategy
    strategy = _build_strategy(data, opportunities, priority)

    return score, priority, explanation, strategy


def _build_strategy(data: Dict, opportunities: list, priority: str) -> str:
    lines = [f"📬 Recommended Outreach ({priority} Priority):"]

    if not data.get("has_website"):
        lines.append("1. Lead with web design offer — they have zero online presence")
        lines.append("2. Show competitor examples with websites in their city")
        lines.append("3. Offer a free mockup to reduce friction")
    elif opportunities:
        lines.append("1. Audit their current website and highlight the gaps")
        missing_social = [o for o in opportunities if "social" in o.lower()]
        if missing_social:
            lines.append("2. Propose social media management package")
        seo_gaps = [o for o in opportunities if "seo" in o.lower() or "meta" in o.lower()]
        if seo_gaps:
            lines.append("3. Offer SEO optimization — they have no meta tags")
    else:
        lines.append("1. Strong digital presence — pitch premium services")
        lines.append("2. Focus on performance marketing / paid ads")
        lines.append("3. Offer content creation or rebranding")

    if data.get("email"):
        lines.append(f"\n📧 Contact via email: {data.get('email')}")
    if data.get("phone"):
        lines.append(f"📞 Call/WhatsApp: {data.get('phone')}")

    return "\n".join(lines)
