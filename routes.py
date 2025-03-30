from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import Project, Certificate, Message, BlogPost, Work
import logging
import os
from werkzeug.utils import secure_filename
from datetime import datetime

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
    
    # Initialize blog posts if none exist
    if BlogPost.query.count() == 0:
        blog_posts = [
            BlogPost(
                title="My Journey into Computer Science Engineering",
                content="""<p>Ever since I was young, I've been fascinated by how computers work. This curiosity led me to pursue a degree in Computer Science Engineering, and what a journey it has been!</p>
                <p>Throughout my academic career, I've had the opportunity to work on various projects, from building simple applications to more complex systems. Each project has taught me something new and has helped me grow as a developer.</p>
                <h2>What I've Learned</h2>
                <p>The field of computer science is constantly evolving, and there's always something new to learn. Here are some key takeaways from my journey so far:</p>
                <ul>
                    <li>The importance of problem-solving skills</li>
                    <li>How to work effectively in a team</li>
                    <li>The value of continuous learning</li>
                    <li>The power of persistence when facing challenges</li>
                </ul>
                <p>I'm excited to continue this journey and see where it takes me next!</p>""",
                summary="Reflecting on my academic journey and the valuable lessons I've learned while pursuing Computer Science Engineering.",
                image_url="https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
                slug="my-journey-into-computer-science-engineering-20250330"
            ),
            BlogPost(
                title="Exploring Machine Learning: A Beginner's Guide",
                content="""<p>Machine Learning (ML) has become one of the most exciting fields in technology today. As a beginner, I was both excited and intimidated by the vast amount of information available.</p>
                <p>In this post, I want to share my experience starting with ML and provide some tips for fellow beginners.</p>
                <h2>Getting Started with Machine Learning</h2>
                <p>If you're new to ML, here are some resources and steps that helped me:</p>
                <ol>
                    <li>Start with the basics: Learn about different types of ML algorithms</li>
                    <li>Practice with simple datasets: Use platforms like Kaggle to practice</li>
                    <li>Join communities: Connect with others learning ML</li>
                    <li>Build small projects: Apply what you've learned to real problems</li>
                </ol>
                <h2>My First ML Project</h2>
                <p>Recently, I completed a simple image classification project using a convolutional neural network. Despite the challenges, it was incredibly rewarding to see the model accurately identify different objects!</p>
                <p>I'm looking forward to diving deeper into this fascinating field and sharing more of my learning journey with you.</p>""",
                summary="My initial experiences with machine learning, resources that helped me get started, and tips for beginners.",
                image_url="https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
                slug="exploring-machine-learning-a-beginners-guide-20250330"
            )
        ]
        
        for post in blog_posts:
            db.session.add(post)
        
        db.session.commit()
    
    # Initialize works if none exist
    if Work.query.count() == 0:
        works = [
            Work(
                title="Data Structures and Algorithms Notes",
                description="Comprehensive notes on various data structures and algorithms, including arrays, linked lists, trees, sorting algorithms, and more.",
                file_url="/static/uploads/works/sample_dsa_notes.pdf",
                file_type="pdf"
            ),
            Work(
                title="Web Development Reference Guide",
                description="A quick reference guide for HTML, CSS, JavaScript, and popular web frameworks.",
                file_url="/static/uploads/works/sample_web_dev_guide.pdf",
                file_type="pdf"
            )
        ]
        
        for work in works:
            db.session.add(work)
        
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
        
        flash('Your message has been saved successfully!', 'success')
        return redirect(url_for('index', _anchor='contact'))
    
    except Exception as e:
        logging.error(f"Error in contact form submission: {e}")
        flash('An error occurred while saving your message. Please try again.', 'error')
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

# Setup upload folders
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
BLOG_IMAGES_FOLDER = os.path.join(UPLOAD_FOLDER, 'blog')
WORKS_FILES_FOLDER = os.path.join(UPLOAD_FOLDER, 'works')

# Create folders if they don't exist
os.makedirs(BLOG_IMAGES_FOLDER, exist_ok=True)
os.makedirs(WORKS_FILES_FOLDER, exist_ok=True)

# Configure app settings for uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Function to check if file extension is allowed
def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_work_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'doc', 'txt', 'ppt', 'pptx', 'xlsx', 'xls', 'zip', 'rar'}

# Blog Routes
@app.route('/blog')
def blog():
    """Display all blog posts"""
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/new', methods=['GET', 'POST'])
def new_blog_post():
    """Create a new blog post"""
    if request.method == 'POST':
        # Get data from form
        title = request.form.get('title')
        content = request.form.get('content')
        summary = request.form.get('summary')
        
        # Create new post
        post = BlogPost(
            title=title,
            content=content,
            summary=summary
        )
        
        # Handle image upload
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and allowed_image_file(image_file.filename):
                # Generate secure filename and save
                filename = secure_filename(image_file.filename)
                # Add timestamp to avoid name conflicts
                file_ext = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{post.title.lower().replace(' ', '_')}_{int(datetime.utcnow().timestamp())}.{file_ext}"
                file_path = os.path.join(BLOG_IMAGES_FOLDER, unique_filename)
                image_file.save(file_path)
                
                # Save relative URL to database
                post.image_url = f"/static/uploads/blog/{unique_filename}"
        
        # Generate slug and save post
        post.save()
        
        flash('Your blog post has been created!', 'success')
        return redirect(url_for('blog'))
    
    return render_template('new_blog_post.html')

@app.route('/blog/post/<slug>')
def blog_post(slug):
    """Display a single blog post"""
    post = BlogPost.query.filter_by(slug=slug).first_or_404()
    return render_template('blog_post.html', post=post)

@app.route('/blog/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_blog_post(post_id):
    """Edit an existing blog post"""
    post = BlogPost.query.get_or_404(post_id)
    
    if request.method == 'POST':
        # Update post data
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.summary = request.form.get('summary')
        
        # Handle image upload if provided
        if 'image' in request.files and request.files['image'].filename:
            image_file = request.files['image']
            if allowed_image_file(image_file.filename):
                # Generate secure filename and save
                filename = secure_filename(image_file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{post.title.lower().replace(' ', '_')}_{int(datetime.utcnow().timestamp())}.{file_ext}"
                file_path = os.path.join(BLOG_IMAGES_FOLDER, unique_filename)
                image_file.save(file_path)
                
                # Update image URL
                post.image_url = f"/static/uploads/blog/{unique_filename}"
        
        # Generate new slug and save
        post.generate_slug()
        db.session.commit()
        
        flash('Your blog post has been updated!', 'success')
        return redirect(url_for('blog_post', slug=post.slug))
    
    return render_template('edit_blog_post.html', post=post)

@app.route('/blog/delete/<int:post_id>', methods=['POST'])
def delete_blog_post(post_id):
    """Delete a blog post"""
    post = BlogPost.query.get_or_404(post_id)
    
    # Delete the post
    db.session.delete(post)
    db.session.commit()
    
    flash('Your blog post has been deleted!', 'success')
    return redirect(url_for('blog'))

@app.route('/api/blog_posts', methods=['GET'])
def get_blog_posts():
    """API endpoint for blog posts"""
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return jsonify([post.serialize for post in posts])

# Works Routes
@app.route('/works')
def works():
    """Display all works"""
    work_items = Work.query.order_by(Work.created_at.desc()).all()
    return render_template('works.html', work_items=work_items)

@app.route('/works/new', methods=['GET', 'POST'])
def new_work():
    """Create a new work item"""
    if request.method == 'POST':
        # Get data from form
        title = request.form.get('title')
        description = request.form.get('description')
        
        # Create new work
        work = Work(
            title=title,
            description=description
        )
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_work_file(file.filename):
                # Generate secure filename and save
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{work.title.lower().replace(' ', '_')}_{int(datetime.utcnow().timestamp())}.{file_ext}"
                file_path = os.path.join(WORKS_FILES_FOLDER, unique_filename)
                file.save(file_path)
                
                # Save relative URL and file type to database
                work.file_url = f"/static/uploads/works/{unique_filename}"
                work.file_type = file_ext
        
        # Save work
        db.session.add(work)
        db.session.commit()
        
        flash('Your work has been uploaded!', 'success')
        return redirect(url_for('works'))
    
    return render_template('new_work.html')

@app.route('/works/edit/<int:work_id>', methods=['GET', 'POST'])
def edit_work(work_id):
    """Edit an existing work item"""
    work = Work.query.get_or_404(work_id)
    
    if request.method == 'POST':
        # Update work data
        work.title = request.form.get('title')
        work.description = request.form.get('description')
        
        # Handle file upload if provided
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            if allowed_work_file(file.filename):
                # Generate secure filename and save
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{work.title.lower().replace(' ', '_')}_{int(datetime.utcnow().timestamp())}.{file_ext}"
                file_path = os.path.join(WORKS_FILES_FOLDER, unique_filename)
                file.save(file_path)
                
                # Update file URL and type
                work.file_url = f"/static/uploads/works/{unique_filename}"
                work.file_type = file_ext
        
        # Save changes
        db.session.commit()
        
        flash('Your work has been updated!', 'success')
        return redirect(url_for('works'))
    
    return render_template('edit_work.html', work=work)

@app.route('/works/delete/<int:work_id>', methods=['POST'])
def delete_work(work_id):
    """Delete a work item"""
    work = Work.query.get_or_404(work_id)
    
    # Delete the work
    db.session.delete(work)
    db.session.commit()
    
    flash('Your work has been deleted!', 'success')
    return redirect(url_for('works'))

@app.route('/api/works', methods=['GET'])
def get_works():
    """API endpoint for works"""
    work_items = Work.query.order_by(Work.created_at.desc()).all()
    return jsonify([work.serialize for work in work_items])
