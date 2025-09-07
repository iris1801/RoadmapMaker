# 🗺️ Roadmap WebApp

A modern Flask webapp for visualizing and managing project roadmaps. Perfect for keeping clients updated on project progress.

## ✨ Features

- **Interactive timeline** responsive design
- **Admin panel** with password authentication
- **Modern design** with colored status indicators
- **Built-in SQLite** database

## 🚀 Quick Start

```bash
git clone https://github.com/yourusername/roadmap-webapp.git
cd roadmap-webapp
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Access**: http://localhost:5000  
**Admin**: http://localhost:5000/admin (password: `admin123`)

## 🔧 Configuration

Change admin password in `app.py`:
```python
ADMIN_PASSWORD = 'your-secure-password'
```

## 📁 Project Structure

```
roadmap-webapp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── index.html        # Client view
│   ├── admin.html        # Admin panel
│   └── admin_login.html  # Admin login
└── roadmap.db           # SQLite database (auto-generated)
```

## 🌐 Production Deploy

### Traditional Server
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

## 🔐 Security

⚠️ **For production use:**
1. Change `SECRET_KEY` in `app.py`
2. Set secure admin password
3. Use HTTPS
4. Configure proper firewall

## 🎯 Use Cases

- 📋 **Client Projects**: Show progress to clients/stakeholders
- 🏢 **Internal Teams**: Development roadmaps
- 🚀 **Startups**: Product timeline for investors
- 📚 **Education**: Academic milestone tracking
- 🔧 **Consulting**: Progress reports

## 🛠️ Customization

### Additional Features Ideas
- 📧 Email notifications
- 📊 Analytics and metrics
- 👥 Multi-user with roles
- 🔗 Slack/Teams integration
- 📱 Mobile app
- 📈 Advanced charts
- 🗓️ Milestone dates/deadlines

## 🤝 Contributing

Contributions welcome! To contribute:

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to branch (`git push origin feature/AmazingFeature`)
5. **Open** Pull Request

## 📄 License

This project is released under the MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Contact

- **GitHub**: [@iris1801](https://github.com/iris1801)
- **Email**: matteo@idrainformatica.it

---

**Made with ❤️ and Flask**