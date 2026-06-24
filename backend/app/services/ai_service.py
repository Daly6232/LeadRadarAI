from app.models.lead import Lead


def analyze_lead(lead: Lead):
    strengths = []
    weaknesses = []

    score = lead.score or 0

    # Website check
    if lead.website:
        strengths.append("Professional website available")
    else:
        weaknesses.append("No website")

    # Email check
    if lead.email:
        strengths.append("Business email available")
    else:
        weaknesses.append("No business email")

    # Phone check
    if lead.phone:
        strengths.append("Phone number available")
    else:
        weaknesses.append("No phone number")

    # AI Priority logic
    if score >= 80:
        priority = "High"
        opportunity = "Excellent prospect for SEO, ads, and automation."
        action = "Contact immediately."

    elif score >= 50:
        priority = "Medium"
        opportunity = "Good business with room to improve digital presence."
        action = "Send personalized outreach."

    else:
        priority = "Low"
        opportunity = "Weak digital presence. High opportunity for full digital upgrade."
        action = "Offer website + SEO + social media services."

    # Closing probability
    if score >= 80:
        closing_probability = "85%"
    elif score >= 50:
        closing_probability = "55%"
    else:
        closing_probability = "30%"

    summary = f"{lead.business_name} has a digital presence score of {score}/100 and is {priority} priority."

    return {
        "business": lead.business_name,
        "city": lead.city,
        "category": lead.category,
        "score": score,
        "priority": priority,
        "closing_probability": closing_probability,
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "opportunity": opportunity,
        "recommended_action": action,
    }
