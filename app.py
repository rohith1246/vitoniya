import os
import logging
import psycopg2
from psycopg2 import pool
from flask import Flask, send_from_directory, jsonify, request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
STATIC_DIR = PUBLIC_DIR if os.path.exists(PUBLIC_DIR) else BASE_DIR

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='')

DATABASE_URL = os.environ.get('DATABASE_URL')
db_pool = None

def get_db_pool():
    global db_pool
    if db_pool is None and DATABASE_URL:
        try:
            db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)
            logger.info("Database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Error creating connection pool: {e}")
            db_pool = None
    return db_pool

if DATABASE_URL:
    try:
        pool_inst = get_db_pool()
        if pool_inst:
            conn = pool_inst.getconn()
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                    CREATE TABLE IF NOT EXISTS contact_submissions (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        company VARCHAR(255),
                        project_type VARCHAR(100),
                        budget_range VARCHAR(100),
                        message TEXT NOT NULL,
                        submitted_at TIMESTAMP DEFAULT NOW()
                    );
                    """)
                conn.commit()
                logger.info("contact_submissions table verified/created successfully.")
            except Exception as e:
                logger.error(f"Error creating table: {e}")
                conn.rollback()
            finally:
                pool_inst.putconn(conn)
    except Exception as e:
        logger.error(f"Error connecting to database on startup: {e}")
else:
    logger.warning("DATABASE_URL environment variable is not set. Database features will be unavailable.")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/demos/clinic')
@app.route('/demos/clinic/')
def demo_clinic():
    clinic_dir = os.path.join(app.static_folder, 'demos', 'clinic')
    return send_from_directory(clinic_dir, 'index.html')

@app.route('/demos/realty')
@app.route('/demos/realty/')
def demo_realty():
    realty_dir = os.path.join(app.static_folder, 'demos', 'realty')
    return send_from_directory(realty_dir, 'index.html')

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.svg', mimetype='image/svg+xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(app.static_folder, 'manifest.json')

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.hostinger.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))
SMTP_USER = os.environ.get('SMTP_USER', 'info@vitoniya.com')
SMTP_PASS = os.environ.get('SMTP_PASS', 'Tinku0587@')

def send_lead_email_alert(name, email, company, project_type, budget_range, message):
    try:
        subject = f"🔥 New Client Inquiry: {name} ({project_type or 'General'})"
        body = f"""New prospective client inquiry received on vitoniya.com:

Name: {name}
Email: {email}
Company / Clinic: {company or 'Not specified'}
Project Area: {project_type or 'Not specified'}
Budget: {budget_range or 'Not specified'}

Client Message:
----------------------------------------
{message}
----------------------------------------
"""
        msg = MIMEMultipart()
        msg['From'] = f"VITONIYA Inquiries <{SMTP_USER}>"
        msg['To'] = SMTP_USER
        msg['Reply-To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        logger.info(f"Instant lead alert dispatched to {SMTP_USER}")
    except Exception as e:
        logger.error(f"Failed to dispatch email alert: {e}")

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    company = data.get('company', '').strip()
    project_type = data.get('project_type', '').strip()
    budget_range = data.get('budget_range', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({"success": False, "message": "Name, email, and message are required"}), 400

    if '@' not in email:
        return jsonify({"success": False, "message": "Invalid email format"}), 400

    # 1. Dispatch real-time SMTP alert to info@vitoniya.com
    send_lead_email_alert(name, email, company, project_type, budget_range, message)

    # 2. Persist to PostgreSQL if available
    pool_inst = get_db_pool()
    if pool_inst:
        conn = None
        try:
            conn = pool_inst.getconn()
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO contact_submissions (name, email, company, project_type, budget_range, message)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (name, email, company, project_type, budget_range, message)
                )
            conn.commit()
            logger.info("Inquiry persisted to contact_submissions database table.")
        except Exception as e:
            logger.error(f"Database error during insert: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                pool_inst.putconn(conn)
    else:
        logger.info("Database pool not active; inquiry received and dispatched via SMTP.")

    return jsonify({
        "success": True, 
        "message": "Thank you! Your message has been received. Our team will contact you within 24 hours."
    })

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
