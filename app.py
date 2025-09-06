from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roadmap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modello Database
class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    detailed_description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Milestone {self.title}>'

class ProjectSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), default='Il Mio Progetto')
    current_milestone_id = db.Column(db.Integer, default=1)
    
# Route principale - Vista cliente
@app.route('/')
def index():
    settings = ProjectSettings.query.first()
    if not settings:
        settings = ProjectSettings()
        db.session.add(settings)
        db.session.commit()
    
    milestones = Milestone.query.order_by(Milestone.order).all()
    return render_template('index.html', 
                         milestones=milestones, 
                         current_milestone=settings.current_milestone_id,
                         project_name=settings.project_name)

# Route admin
@app.route('/admin')
def admin():
    milestones = Milestone.query.order_by(Milestone.order).all()
    settings = ProjectSettings.query.first()
    return render_template('admin.html', 
                         milestones=milestones,
                         settings=settings)

# API per gestire milestone
@app.route('/api/milestone/<int:id>')
def get_milestone(id):
    milestone = Milestone.query.get_or_404(id)
    return jsonify({
        'id': milestone.id,
        'title': milestone.title,
        'description': milestone.description,
        'detailed_description': milestone.detailed_description,
        'status': milestone.status,
        'order': milestone.order
    })

@app.route('/api/milestone', methods=['POST'])
def create_milestone():
    data = request.json
    milestone = Milestone(
        title=data['title'],
        description=data.get('description', ''),
        detailed_description=data.get('detailed_description', ''),
        order=data['order'],
        status=data.get('status', 'pending')
    )
    db.session.add(milestone)
    db.session.commit()
    return jsonify({'success': True, 'id': milestone.id})

@app.route('/api/milestone/<int:id>', methods=['PUT'])
def update_milestone(id):
    milestone = Milestone.query.get_or_404(id)
    data = request.json
    
    milestone.title = data.get('title', milestone.title)
    milestone.description = data.get('description', milestone.description)
    milestone.detailed_description = data.get('detailed_description', milestone.detailed_description)
    milestone.status = data.get('status', milestone.status)
    milestone.order = data.get('order', milestone.order)
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/milestone/<int:id>', methods=['DELETE'])
def delete_milestone(id):
    milestone = Milestone.query.get_or_404(id)
    db.session.delete(milestone)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/settings', methods=['POST'])
def update_settings():
    settings = ProjectSettings.query.first()
    if not settings:
        settings = ProjectSettings()
        db.session.add(settings)
    
    data = request.json
    settings.project_name = data.get('project_name', settings.project_name)
    settings.current_milestone_id = data.get('current_milestone_id', settings.current_milestone_id)
    
    db.session.commit()
    return jsonify({'success': True})

# Inizializzazione database con dati di esempio
def init_db():
    with app.app_context():
        db.create_all()
        
        # Verifica se ci sono già milestone
        if Milestone.query.count() == 0:
            sample_milestones = [
                {
                    'title': 'Avvio e Analisi',
                    'description': 'Kickoff e definizione requisiti',
                    'detailed_description': 'Kickoff meeting con cliente per allineamento obiettivi. Raccolta dettagli su contenuti e branding. Definizione requisiti tecnici e setup repository.',
                    'order': 1,
                    'status': 'completed'
                },
                {
                    'title': 'Infrastruttura Backend',
                    'description': 'Setup server e database',
                    'detailed_description': 'Configurazione server di sviluppo e database. Progettazione schema DB per utenti, dispositivi e proxy. Setup API base con autenticazione.',
                    'order': 2,
                    'status': 'completed'
                },
                {
                    'title': 'Frontend Pubblico',
                    'description': 'Sito vetrina e registrazioni',
                    'detailed_description': 'Sviluppo sito vetrina responsive. Implementazione registrazione utenti e integrazione gateway pagamenti.',
                    'order': 3,
                    'status': 'in_progress'
                },
                {
                    'title': 'Pannello Utente',
                    'description': 'Dashboard e controlli utente',
                    'detailed_description': 'Implementazione dashboard utente con stato proxy, credenziali, log utilizzo e funzioni di controllo.',
                    'order': 4,
                    'status': 'pending'
                },
                {
                    'title': 'Backend Admin',
                    'description': 'Pannello amministrazione',
                    'detailed_description': 'Modulo gestione utenti, dispositivi e proxy. Controlli remoti e logs di sistema.',
                    'order': 5,
                    'status': 'pending'
                },
                {
                    'title': 'Sicurezza',
                    'description': 'Hardening e test sicurezza',
                    'detailed_description': 'Implementazione sistemi di alert, rate limiting, test sicurezza e dockerizzazione.',
                    'order': 6,
                    'status': 'pending'
                },
                {
                    'title': 'Collaudo',
                    'description': 'Test e correzioni',
                    'detailed_description': 'Deploy ambiente test, sessioni di test con casi reali, correzione bug.',
                    'order': 7,
                    'status': 'pending'
                },
                {
                    'title': 'Consegna',
                    'description': 'Documentazione e deploy',
                    'detailed_description': 'Consegna codice sorgente, manuale utente e pacchetto Docker.',
                    'order': 8,
                    'status': 'pending'
                },
                {
                    'title': 'Supporto',
                    'description': 'Garanzia 3 mesi',
                    'detailed_description': 'Correzione bug, supporto tecnico e possibili evoluzioni future.',
                    'order': 9,
                    'status': 'pending'
                }
            ]
            
            for ms_data in sample_milestones:
                milestone = Milestone(**ms_data)
                db.session.add(milestone)
            
            # Crea settings iniziali
            settings = ProjectSettings(
                project_name='Piattaforma Proxy 4G/5G',
                current_milestone_id=3
            )
            db.session.add(settings)
            
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
