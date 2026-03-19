{
    "name": "Sales Team Gamification: Targets & Rewards",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "summary": "Boost sales with monthly targets and progress bars.",
    "description": """
        Adds monthly sales targets for individuals.
        Includes real-time progress bars and secures target modifications to Managers only.
    """,
    "author": "Digimonk Technologies",
    "website": "https://digimonk.in/",
    "depends": ["sale_management", "sales_team"],
    "data": [
        "security/security.xml",
        "views/res_users_views.xml",
        "views/sale_order_views.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
