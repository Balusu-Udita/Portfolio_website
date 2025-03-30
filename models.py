from app import db
from datetime import datetime

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    features = db.Column(db.Text)
    technologies = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    project_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Project {self.title}>'
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'features': self.features,
            'technologies': self.technologies,
            'image_url': self.image_url,
            'project_url': self.project_url
        }

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    issuer = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    certificate_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Certificate {self.title}>'
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'issuer': self.issuer,
            'date': self.date,
            'image_url': self.image_url,
            'certificate_url': self.certificate_url
        }

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message from {self.name}>'
