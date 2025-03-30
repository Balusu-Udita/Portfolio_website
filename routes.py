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
                title="Food Delivery Website",
                description="A food delivery platform with a unique feature for food donation to help reduce food waste and support those in need.",
                features="Online food ordering, Food donation option, User authentication, Restaurant listings",
                technologies="HTML, CSS, JavaScript, Python",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg",
                project_url="#"
            ),
            Project(
                title="Student Project Guidance Website",
                description="A platform designed to help undergraduate students find guidance and resources for their academic projects.",
                features="Project database, Mentor matching, Resource library, Discussion forums",
                technologies="HTML, CSS, JavaScript, Python",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg",
                project_url="#"
            ),
            Project(
                title="Python Chatbot",
                description="An intelligent chatbot built using Python that can answer questions and provide assistance to users.",
                features="Natural language processing, Contextual responses, Knowledge base integration",
                technologies="Python, NLP, Machine Learning",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
                project_url="#"
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
                certificate_url="#"
            ),
            Certificate(
                title="Android Developer Virtual Internship",
                issuer="AICTE",
                date="Sep 2024",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/android/android-original.svg",
                certificate_url="#"
            ),
            Certificate(
                title="Tihan - Basics of Autonomous Drones",
                issuer="TSSC",
                date="Sep 2024",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original.svg",
                certificate_url="#"
            ),
            Certificate(
                title="Automation Explorer",
                issuer="UiPath",
                date="Jul 2024",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg",
                certificate_url="#"
            ),
            Certificate(
                title="Introduction to Generative AI",
                issuer="Google Cloud Skills Boost",
                date="May 2024",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg",
                certificate_url="#"
            ),
            Certificate(
                title="NPTEL - C Programming",
                issuer="IIT Kharagpur",
                date="May 2024",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/c/c-original.svg",
                certificate_url="#"
            ),
            Certificate(
                title="Cisco Networking Academy",
                issuer="Cisco",
                date="Aug 2023",
                image_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
                certificate_url="#"
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
