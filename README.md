# VITONIYA

> **Vitoniya Global Technologies** | *Intelligent Solutions For A Better Tomorrow*  
> Official Domain: [vitoniya.com](https://vitoniya.com) | Contact: [info@vitoniya.com](mailto:info@vitoniya.com)

Official responsive, high-performance web service for **Vitoniya Global Technologies**, powered by **Python Flask & Gunicorn**.

---

## 📁 Repository Structure

```
vitoniya/
├── app.py                # Flask application & HTTP server routing
├── requirements.txt      # Python dependencies (Flask, gunicorn)
├── Procfile              # Render process definition (web: gunicorn app:app)
├── .gitignore            # Python & system gitignore
├── README.md             # Complete Render Web Service & DNS guide
└── public/               # Production frontend assets
    ├── index.html        # Landing page with SEO, Open Graph
    ├── styles.css        # Premium editorial stylesheet & responsive layout
    ├── script.js         # Interactive scroll animations, mobile menu, email copy
    └── favicon.svg       # Vector geometric 'V' monogram favicon
```

---

## 🚀 Deployment Guide: Render Web Service

Deploying on [Render](https://render.com) as a **Web Service**:

1. Log in to [Render](https://render.com).
2. Click **New +** → select **Web Service** *(not Static Site)*.
3. Connect your GitHub repository: `rohith1246/vitoniya`.
4. Configure the Web Service settings:
   - **Name**: `vitoniya`
   - **Language / Runtime**: `Python 3`
   - **Branch**: `main`
   - **Region**: Closest to your target audience (e.g. Frankfurt, Singapore, or Oregon)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or Starter)
5. *(Optional)* In **Advanced Settings**, set **Health Check Path** to `/health`.
6. Click **Create Web Service**.
7. Render will build the environment, install Flask and Gunicorn, and start your web service at:  
   `https://vitoniya.onrender.com`

---

## 🌐 Connecting `vitoniya.com` (Hostinger DNS Setup)

### 1. Add Custom Domain on Render
- In your Render Web Service dashboard, go to **Settings** → **Custom Domains**.
- Add:
  - `vitoniya.com`
  - `www.vitoniya.com`
- Set `vitoniya.com` as the **Primary Domain** (Render will automatically redirect `www` to root).
- Render will display the DNS records needed for Hostinger.

### 2. Configure Hostinger DNS
In your **Hostinger Control Panel** → **Domains** → **vitoniya.com** → **DNS / Nameservers**:

| Type | Name / Host | Points to / Value | TTL | Purpose |
|---|---|---|---|---|
| **A** | `@` | `216.24.57.1` *(or IP provided by Render)* | 3600 | Directs apex domain to Render Web Service |
| **CNAME** | `www` | `vitoniya.onrender.com` | 3600 | Directs `www` to Render |

> ⚠️ **CRITICAL: Preserve Email (MX Records)**  
> **Do NOT delete or edit your existing MX, SPF, or DKIM records** in Hostinger.  
> Your email (`info@vitoniya.com`) routes through Hostinger's mail servers, while website traffic routes to your Render Web Service.

---

## 🔒 Automatic SSL / HTTPS
Render automatically provisions and renews a free Let's Encrypt SSL certificate once DNS records are verified.

---

## 💻 Local Testing

To run the web service locally on your machine:
```bash
pip install -r requirements.txt
python app.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

---

© 2026 Vitoniya Global Technologies. All rights reserved.
