"""Seed demo data - 2 companies, realistic contacts and signals."""
from .models import init_db, upsert_account, upsert_contact, add_signal, update_icp_score


def seed():
    init_db()

    # Company 1 - Rippling (HR/Fintech SaaS)
    a1 = upsert_account(
        domain="rippling.com",
        name="Rippling",
        industry="HR SaaS",
        size="500-5000",
    )
    upsert_contact(a1, "Parker Conrad", "CEO", "parker@rippling.com", "linkedin.com/in/parkerconrad")
    upsert_contact(a1, "Vanessa Wu", "VP Sales", "vanessa@rippling.com", "linkedin.com/in/vanessawu")
    upsert_contact(a1, "Matt MacInnis", "CRO", "matt@rippling.com", "linkedin.com/in/mattmacinnis")
    add_signal(a1, "funding", "Rippling raised $200M Series F at $13.5B valuation", "TechCrunch")
    add_signal(a1, "product_launch", "Rippling launched AI-native expense management", "Product Hunt")
    add_signal(a1, "hiring", "Rippling is hiring 50+ enterprise sales reps", "LinkedIn")
    update_icp_score(a1, 0.92)

    # Company 2 - Linear (Developer Tools SaaS)
    a2 = upsert_account(
        domain="linear.app",
        name="Linear",
        industry="Developer Tools",
        size="50-500",
    )
    upsert_contact(a2, "Karri Saarinen", "CEO", "karri@linear.app", "linkedin.com/in/karrisaarinen")
    upsert_contact(a2, "Tuomas Artman", "CTO", "tuomas@linear.app", "linkedin.com/in/tuomasartman")
    add_signal(a2, "product_launch", "Linear launched Cycles - AI-powered sprint planning", "Hacker News")
    add_signal(a2, "growth", "Linear crossed 25,000 paying teams milestone", "Twitter")
    update_icp_score(a2, 0.87)
