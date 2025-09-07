from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roadmap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Password per l'admin (cambia questa!)
ADMIN_PASSWORD = 'admin123'

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

# Route per il login admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Password non corretta!')
            return render_template('admin_login.html', error=True)
    
    return render_template('admin_login.html')

# Route per il logout admin
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# Route admin protetta
@app.route('/admin')
def admin():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    milestones = Milestone.query.order_by(Milestone.order).all()
    settings = ProjectSettings.query.first()
    return render_template('admin.html', 
                         milestones=milestones,
                         settings=settings)

# API per gestire milestone (protette)
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
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
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
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
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
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    milestone = Milestone.query.get_or_404(id)
    db.session.delete(milestone)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/settings', methods=['POST'])
def update_settings():
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
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
            # Milestone di esempio (opzionali - rimuovi se non desiderate)
            sample_milestones = [
                {
                    'title': 'Analisi e Pianificazione',
                    'description': 'Raccolta requisiti e definizione architettura',
                    'detailed_description': 'Fase iniziale del progetto con analisi dettagliata dei requisiti, definizione dell\'architettura tecnica e pianificazione delle attività.',
                    'order': 1,
                    'status': 'completed'
                },
                {
                    'title': 'Sviluppo Backend',
                    'description': 'Implementazione API e database',
                    'detailed_description': 'Sviluppo delle API REST, configurazione database e implementazione della logica di business principale.',
                    'order': 2,
                    'status': 'in_progress'
                },
                {
                    'title': 'Frontend e UI',
                    'description': 'Interfaccia utente e dashboard',
                    'detailed_description': 'Creazione dell\'interfaccia utente, dashboard amministrativa e integrazione con le API backend.',
                    'order': 3,
                    'status': 'pending'
                },
                {
                    'title': 'Testing e Deploy',
                    'description': 'Test completi e messa in produzione',
                    'detailed_description': 'Fase di testing completo, correzione bug, ottimizzazioni performance e deploy in ambiente di produzione.',
                    'order': 4,
                    'status': 'pending'
                }
            ]
            
            for ms_data in sample_milestones:
                milestone = Milestone(**ms_data)
                db.session.add(milestone)
            
            # Crea settings iniziali
            settings = ProjectSettings(
                project_name='Roadmap Project',
                current_milestone_id=2
            )
            db.session.add(settings)
            
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)