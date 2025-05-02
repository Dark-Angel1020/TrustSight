<div align="center">
  <img src="https://github.com/user-attachments/assets/4f58b08e-0cca-414d-a982-05fab9b0d38c" alt="Project Banner" width="600"/><br><br>
  <h1>Website Monitoring System</h1>
  <p><strong>Advanced SSL Monitoring & Defacement Detection Toolkit</strong></p>
</div>
<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.8+-blueviolet.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/version-1.0.0-orange.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/status-active-brightgreen.svg"></a>
</p>

<p align="center"><em>Monitor your websites' health, detect defacements, and stay ahead of SSL issues with timely email alerts.</em></p>

---

## ✨ Features

- 🚨 **SSL Certificate Validation**  
- 🛡️ **Website Defacement Detection**  
- 🔄 **Change Tracking via HTML Hashing**  
- 📬 **Email Alerts for Admins**  

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dark-Angel1020/TrustSight.git
   cd TrustSight
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install requirements**
   ```bash
   pip install -r req.txt
   ```

4. **Set up your credentials**
   Add a `.env` file:
   ```
   SMTP_SENDER=your_email@gmail.com
   SMTP_PASSWORD=your_app_specific_password
   ```

---

## ⚙️ Configuration

- Edit `websites.csv`:
  ```
  si number,website address,email
  1,https://example.com,admin@example.com
  2,https://testsite.org,support@testsite.org
  ```

- First run to generate content hashes:
  ```bash
  python main.py
  ```

---

## 💻 Terminal UI Preview

### 🧭 Main Menu
```
████████╗██████╗ ██╗   ██╗███████╗████████╗███████╗██╗ ██████╗ ██╗  ██╗████████╗
╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔════╝██║██╔════╝ ██║  ██║╚══██╔══╝
   ██║   ██████╔╝██║   ██║███████╗   ██║   ███████╗██║██║  ███╗███████║   ██║   
   ██║   ██╔══██╗██║   ██║╚════██║   ██║   ╚════██║██║██║   ██║██╔══██║   ██║   
   ██║   ██║  ██║╚██████╔╝███████║   ██║   ███████║██║╚██████╔╝██║  ██║   ██║   
   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   

Main Menu:
1. Certificate Validation
2. Defacement Checker
3. Exit
```

### 🔐 SSL Certificate Check
```
SSL Certificate Validation Results
+--------+---------------------+--------+------------+------------+----------------+-----------------+
| SI No  | Website             | Status | From       | To         | Days Remaining | Issuer          |
+--------+---------------------+--------+------------+------------+----------------+-----------------+
| 1      | https://example.com | Valid  | 2024-01-01 | 2025-01-01 | 244            | Let's Encrypt   |
+--------+---------------------+--------+------------+------------+----------------+-----------------+
```

---

## 📧 Example Email Alerts

**Certificate Expiring:**
```
Subject: Alert: SSL Certificate Expiring Soon - https://example.com

The SSL certificate for https://example.com is expiring soon.
Expiration Date: 2023-12-31
Days Remaining: 15
```

**Defacement Detected:**
```
Subject: URGENT: Defacement Detected - https://yoursite.org

Potential website defacement has been detected on: https://yoursite.org
The content contains suspicious keywords indicating possible compromise.
```

---

## 📂 File Structure

```
📦 website-monitoring-system
├── main.py               # Main controller
├── cert.py               # SSL checker
├── checkchange.py        # Content integrity check
├── alertmailer.py        # SMTP email system
├── websites.csv          # Sites to monitor
├── site_hash.csv         # Stored SHA256 hashes
├── html_snapshots/       # HTML snapshot storage
├── req.txt               # Dependency list
└── .env                  # Email credentials
```

---

## 🤝 Contributing

1. Fork the repository  
2. Create your branch: `git checkout -b feature/my-feature`  
3. Commit your changes: `git commit -m "Add awesome feature"`  
4. Push to the branch: `git push origin feature/my-feature`  
5. Submit a pull request ✅

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
<div align="center">
  <p><i>Secure your data.</i></p>
  <p>Made with ❤️</p>
</div>

