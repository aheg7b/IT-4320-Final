IT 4320 Final
bus-reservation-system/
│
├── app/
│   ├── __init__.py             # Flask app factory and extensions init
│   ├── models.py               # SQLAlchemy ORM models (Reservation, Admin)
│   ├── routes.py               # Flask route handlers (main menu, reservation, admin)
│   ├── forms.py                # WTForms or form classes for Reservation, Admin login
│   ├── utils.py                # Utility functions (e.g., cost matrix, reservation code)
│   ├── templates/
│   │   ├── base.html           # Base template with navbar, footer, etc.
│   │   ├── main_menu.html      # Main menu page
│   │   ├── reserve_seat.html  # Seat reservation form
│   │   ├── admin_login.html   # Admin login form
│   │   ├── admin_dashboard.html # Admin seating chart, reservations, total sales
│   │   └── confirmation.html  # Reservation confirmation page
│   └── static/
│       ├── css/
│       │   └── style.css       # Custom styles
│       ├── js/
│       │   └── scripts.js      # Custom JavaScript (if needed)
│       └── images/             # Any static images, icons
│
├── migrations/                 # Database migration files (if using Flask-Migrate)
│
├── tests/
│   ├── test_models.py          # Unit tests for models
│   ├── test_routes.py          # Unit tests for routes/views
│   └── test_utils.py           # Tests for utility functions
│
├── .gitignore                  # Ignore __pycache__, env, etc.
├── config.py                   # Configuration variables (DB URI, secret keys)
├── requirements.txt            # Python dependencies
├── run.py                      # Entry point to run Flask app
├── README.md                   # Project overview, setup instructions
└── reservations.db             # SQLite database (if you choose to commit DB)


Explanation of key files/folders:

app/ — core application code, templates, and static assets
models.py — define your Reservation and Admin models using SQLAlchemy
routes.py — contains all your route handlers and views for reservation, admin, main menu, etc.
forms.py — optional, for defining form classes if using WTForms or similar
utils.py — cost matrix generation, reservation code generation, sales calculation functions
templates/ — Jinja2 HTML templates for each page
static/ — CSS, JS, images for frontend styling and interactivity
migrations/ — optional folder if you use database migrations
tests/ — automated tests for your app
run.py — launches the Flask app
config.py — config parameters for dev, testing, production
requirements.txt — pinned Python package dependencies
README.md — instructions and project info

*Revised with assistance of Chat GPT to aid in cleaning and making the file clear as to what was expected
