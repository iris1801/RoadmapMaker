# 🗺️ Roadmap WebApp

Una webapp Flask moderna e responsive per visualizzare e gestire roadmap di progetto. Perfetta per tenere aggiornati clienti e stakeholder sul progresso del tuo lavoro.

![Roadmap Preview](https://img.shields.io/badge/Status-Ready%20to%20Use-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightblue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Caratteristiche

### 🎯 Vista Cliente
- **Timeline interattiva** orizzontale/verticale responsive
- **Indicatore di progresso** generale automatico
- **Modal dettagliati** per ogni milestone (click per aprire)
- **Design moderno** con animazioni fluide
- **Stati colorati** (Completato ✅ / In Corso 🔄 / In Attesa ⏳)

### 🔧 Pannello Admin
- **Autenticazione con password** semplice e sicura
- **Gestione completa milestone** (Aggiungi/Modifica/Elimina)
- **Cambio stati** in tempo reale
- **Riordinamento** milestone
- **Impostazioni progetto** (nome, milestone corrente)
- **Interfaccia intuitiva** con sidebar

### 📱 Caratteristiche Tecniche
- **Database SQLite** integrato (zero configurazione)
- **API REST** complete per tutte le operazioni
- **Responsive design** (perfetto su mobile/desktop)
- **Sessioni sicure** per l'autenticazione admin

## 🚀 Quick Start

### 1. Clone del Repository
```bash
git clone https://github.com/tuousername/roadmap-webapp.git
cd roadmap-webapp
```

### 2. Setup Ambiente Virtuale
```bash
# Crea ambiente virtuale
python -m venv venv

# Attiva l'ambiente virtuale
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Installa Dipendenze
```bash
pip install -r requirements.txt
```

### 4. Avvia l'Applicazione
```bash
python app.py
```

### 5. Accedi alla WebApp
- **Vista Cliente**: http://localhost:5000
- **Pannello Admin**: http://localhost:5000/admin
- **Password Admin**: `admin123` (⚠️ Cambiarla in produzione!)

## 📁 Struttura del Progetto

```
roadmap-webapp/
│
├── app.py                 # Applicazione Flask principale
├── requirements.txt       # Dipendenze Python
├── README.md             # Documentazione
├── templates/            # Template HTML
│   ├── index.html        # Vista cliente
│   ├── admin.html        # Pannello amministrazione
│   └── admin_login.html  # Login admin
└── roadmap.db           # Database SQLite (auto-generato)
```

## 🎨 Screenshots

### Vista Cliente
Una timeline moderna e pulita che mostra il progresso del progetto:

### Pannello Admin
Interfaccia intuitiva per gestire tutte le milestone:

## ⚙️ Configurazione

### Cambiare la Password Admin
Modifica questa riga in `app.py`:
```python
ADMIN_PASSWORD = 'la-tua-password-sicura'
```

### Configurare Database Esterno
Per progetti più grandi, puoi usare PostgreSQL o MySQL:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
```

### Personalizzare i Colori
Modifica le variabili CSS nei template per adattare i colori al tuo brand.

## 🌐 Deploy in Produzione

### Opzione 1: Server Tradizionale
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Opzione 2: Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

### Opzione 3: Servizi Cloud
- **Heroku**: Compatibile out-of-the-box
- **Railway**: Deploy automatico da GitHub
- **PythonAnywhere**: Hosting Flask dedicato

## 🔐 Sicurezza

### ⚠️ Per l'Uso in Produzione:
1. **Cambia la SECRET_KEY** in `app.py`
2. **Imposta password admin sicura**
3. **Usa HTTPS** sempre
4. **Configura firewall** appropriato
5. **Considera autenticazione** più robusta per admin

### 🛡️ Sicurezza Implementata:
- ✅ Sessioni Flask sicure
- ✅ API protette da autenticazione
- ✅ Validazione input utente
- ✅ Protezione CSRF (sessioni)

## 🎯 Casi d'Uso Ideali

- 📋 **Progetti Cliente**: Mostra progress a clienti/stakeholder
- 🏢 **Team Internal**: Roadmap interne di sviluppo
- 🚀 **Startup**: Timeline di prodotto per investitori
- 📚 **Progetti Educational**: Tracciamento milestone accademiche
- 🔧 **Consulenza**: Progress report per contratti

## 🛠️ Personalizzazioni Possibili

### Funzionalità Aggiuntive
- 📧 **Notifiche Email** al completamento milestone
- 📊 **Analytics** e metriche di progresso
- 👥 **Multi-utente** con ruoli diversi
- 🔗 **Integrazione Slack/Teams**
- 📱 **App mobile** con React Native
- 📈 **Grafici avanzati** con Chart.js
- 🗓️ **Date e scadenze** per le milestone

### Esempi di Estensione
```python
# Aggiungi campo data alle milestone
class Milestone(db.Model):
    # ... existing fields
    due_date = db.Column(db.Date, nullable=True)
    
# API per notifiche
@app.route('/api/notify/<int:milestone_id>')
def send_notification(milestone_id):
    # Logica per invio email/Slack
    pass
```

## 🤝 Contribuire

Le contribuzioni sono benvenute! Per contribuire:

1. **Fork** il repository
2. **Crea** un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. **Apri** una Pull Request

## 📜 Changelog

### v1.0.0 (2024-12-XX)
- ✨ Release iniziale
- 🎯 Vista cliente con timeline interattiva
- 🔧 Pannello admin completo
- 🔐 Sistema autenticazione
- 📱 Design responsive
- 🎨 Interfaccia moderna

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT - vedi il file [LICENSE](LICENSE) per dettagli.

## ❤️ Supporto

Se questo progetto ti è stato utile, considera:
- ⭐ **Stella** il repository
- 🐛 **Segnala bug** tramite Issues
- 💡 **Suggerisci nuove feature**
- 🤝 **Contribuisci** al codice

## 📞 Contatti

- **GitHub**: [@tuousername](https://github.com/tuousername)
- **Email**: tua-email@example.com

---

**Fatto con ❤️ e Flask**