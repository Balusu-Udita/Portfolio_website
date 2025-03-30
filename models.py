from app import db
from datetime import datetime
import re

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

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(200), unique=True)
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'image_url': self.image_url,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'slug': self.slug
        }
    
    def generate_slug(self):
        # Convert the title to lowercase and replace spaces with hyphens
        slug = self.title.lower()
        # Remove any characters that aren't alphanumeric, hyphens, or spaces
        slug = re.sub(r'[^\w\s-]', '', slug)
        # Replace spaces with hyphens
        slug = re.sub(r'\s+', '-', slug)
        # Add timestamp to make slug unique
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f"{slug}-{timestamp}"
    
    def save(self):
        if not self.slug:
            self.slug = self.generate_slug()
        db.session.add(self)
        db.session.commit()

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_url = db.Column(db.String(200))
    file_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Work {self.title}>'
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'file_url': self.file_url,
            'file_type': self.file_type,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }
