from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db, mail
from models import Project, Certificate, Message
from flask_mail import Message as MailMessage
import logging

# Initialize default data
def initialize_data():
    if Project.query.count() == 0:
        projects = [
            Project(
                title="Bill Management System",
                description="A comprehensive Python-based billing system designed to efficiently manage invoices, track payments, and generate detailed financial reports for businesses of all sizes.",
                features="Invoice generation, Payment tracking, Financial reporting, Client management, PDF export",
                technologies="Python, SQLite, Tkinter, ReportLab, PyPDF2",
                image_url="https://images.unsplash.com/photo-1554224155-6726b3ff858f?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
                project_url="https://github.com/"
            ),
            Project(
                title="Student Project Guidance Website",
                description="A platform designed to help undergraduate students find guidance and resources for their academic projects.",
                features="Project database, Mentor matching, Resource library, Discussion forums",
                technologies="HTML, CSS, JavaScript, Python",
                image_url="https://images.unsplash.com/photo-1523240795612-9a054b0db644?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
                project_url="https://github.com/"
            ),
            Project(
                title="Python Chatbot",
                description="An intelligent chatbot built using Python that can answer questions and provide assistance to users.",
                features="Natural language processing, Contextual responses, Knowledge base integration",
                technologies="Python, NLP, Machine Learning",
                image_url="https://images.unsplash.com/photo-1531482615713-2afd69097998?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
                project_url="https://github.com/"
            )
        ]
        
        for project in projects:
            db.session.add(project)
        
        db.session.commit()
    
    if Certificate.query.count() == 0:
        certificates = [
            Certificate(
                title="Java Programming Fundamentals",
                issuer="Infosys",
                date="Nov 2024",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg",
                certificate_url="https://www.linkedin.com/in/balusu-udita-230a44283/"
            ),
            Certificate(
                title="Android Developer Virtual Internship",
                issuer="AICTE",
                date="Sep 2024",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/android/android-original.svg",
                certificate_url="https://www.linkedin.com/in/balusu-udita-230a44283/"
            ),
            Certificate(
                title="Tihan - Basics of Autonomous Drones",
                issuer="TSSC",
                date="Sep 2024",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original.svg",
                certificate_url="https://www.linkedin.com/in/balusu-udita-230a44283/"
            ),
            Certificate(
                title="Automation Explorer",
                issuer="UiPath",
                date="Jul 2024",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg",
                certificate_url="https://www.linkedin.com/in/balusu-udita-230a44283/"
            ),
            Certificate(
                title="Introduction to Generative AI",
                issuer="Google Cloud Skills Boost",
                date="May 2024",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg",
                certificate_url="https://www.linkedin.com/in/balusu-udita-230a44283/"
            ),
            Certificate(
                title="NPTEL - C Programming",
                issuer="IIT Kharagpur",
                date="May 2024",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/c/c-original.svg",
                certificate_url="https://www.linkedin.com/in/balusu-udita-230a44283/"
            ),
            Certificate(
                title="Cisco Networking Academy",
                issuer="Cisco",
                date="Aug 2023",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
                certificate_url="https://www.linkedin.com/in/balusu-udita-230a44283/"
            )
        ]
        
        for certificate in certificates:
            db.session.add(certificate)
        
        db.session.commit()

# Routes
@app.route('/')
def index():
    # Initialize data if database is empty
    initialize_data()
    
    # Fetch data from the database
    projects = Project.query.all()
    certificates = Certificate.query.all()
    
    return render_template('index.html', projects=projects, certificates=certificates)

@app.route('/contact', methods=['POST'])
def contact():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_content = request.form.get('message')
        
        # Validate form data
        if not all([name, email, subject, message_content]):
            flash('Please fill out all fields', 'error')
            return redirect(url_for('index', _anchor='contact'))
        
        # Save message to database
        new_message = Message(
            name=name,
            email=email,
            subject=subject,
            message=message_content
        )
        db.session.add(new_message)
        db.session.commit()
        
        # Send email
        try:
            msg = MailMessage(
                subject=f"Portfolio Contact: {subject}",
                recipients=[app.config['MAIL_USERNAME']],
                body=f"From: {name} <{email}>\n\n{message_content}",
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            mail.send(msg)
            logging.debug(f"Email sent successfully from {email}")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            # Continue execution - the message is still saved to database
        
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('index', _anchor='contact'))
    
    except Exception as e:
        logging.error(f"Error in contact form submission: {e}")
        flash('An error occurred while sending your message. Please try again.', 'error')
        return redirect(url_for('index', _anchor='contact'))

# API routes for dynamic content
@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.serialize for project in projects])

@app.route('/api/certificates', methods=['GET'])
def get_certificates():
    certificates = Certificate.query.all()
    return jsonify([cert.serialize for cert in certificates])
