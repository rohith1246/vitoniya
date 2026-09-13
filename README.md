# VITONIYA

> **Vitoniya Global Technologies** | *Building What's Next.*  
> Founded & Owned by **Rohith Vuppula**  
> Official Domain: [vitoniya.com](https://vitoniya.com) | Contact: [info@vitoniya.com](mailto:info@vitoniya.com)

Official responsive, high-performance "Launching Soon" landing page for **Vitoniya Global Technologies**.

---

## 📁 Repository Structure

```
vitoniya/
├── index.html        # Semantic HTML5 landing page with SEO & Open Graph meta
├── styles.css        # Premium dark mode stylesheet & responsive layout
├── script.js         # Interactive canvas animation, mobile menu, email copy
├── favicon.svg       # Vector geometric 'V' monogram favicon
└── README.md         # Deployment & DNS setup guide
```

---

## 🚀 Deployment Guide: Render Static Site

1. Sign in to [Render](https://render.com).
2. Click **New +** → **Static Site**.
3. Connect your GitHub repository: `rohith1246/vitoniya`.
4. Configure the service settings:
   - **Name**: `vitoniya`
   - **Branch**: `main`
   - **Build Command**: *(leave blank)*
   - **Publish Directory**: `.`
5. Click **Create Static Site**.
6. Render will build and deploy your site in seconds at a URL like:
   `https://vitoniya.onrender.com`

---

## 🌐 Connecting `vitoniya.com` (Hostinger DNS Setup)

### 1. Add Custom Domain in Render
- In your Render dashboard, navigate to your static site.
- Go to **Settings** → **Custom Domains**.
- Add both:
  - `vitoniya.com`
  - `www.vitoniya.com`
- Set `vitoniya.com` as the **Primary Domain** (Render will automatically redirect `www` to root).

### 2. Update DNS Records in Hostinger
Log in to your Hostinger Control Panel → **Domains** → **vitoniya.com** → **DNS / Nameservers**:

| Type | Name / Host | Target / Value | TTL | Purpose |
|---|---|---|---|---|
| **A** | `@` | `216.24.57.1` *(or IP provided by Render)* | 3600 | Points root domain to Render |
| **CNAME** | `www` | `vitoniya.onrender.com` | 3600 | Points www to Render |

> ⚠️ **CRITICAL: Preserve Email (MX Records)**  
> **Do NOT touch or delete existing MX, SPF, or DKIM records** in Hostinger.  
> Your email (`info@vitoniya.com`) routes through Hostinger's mail servers, while your web traffic routes to Render.

---

## 🔒 SSL / HTTPS
Render automatically provisions and renews a free Let's Encrypt SSL certificate as soon as the DNS records propagate (typically 5–30 minutes).

---

© 2026 Vitoniya Global Technologies. All rights reserved.
