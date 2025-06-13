from flask import Flask, render_template, request, redirect, url_for
import json
import os
import uuid

app = Flask(__name__)

# File to store blog posts
BLOG_FILE = 'blog_posts.json'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load blog posts from file
def load_blog_posts():
    if os.path.exists(BLOG_FILE):
        with open(BLOG_FILE, 'r') as f:
            return json.load(f)
    return []

# Save blog posts to file
def save_blog_posts(posts):
    with open(BLOG_FILE, 'w') as f:
        json.dump(posts, f)

# Initialize blog posts
blog_posts = load_blog_posts()

@app.route('/')
def index():
    return redirect(url_for('write'))

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        font_family = request.form.get('font_family', 'Arial')
        background_color = request.form.get('background_color', '#ffffff')
        blog_posts.append({
            'title': title,
            'content': content,
            'font_family': font_family,
            'background_color': background_color
        })
        save_blog_posts(blog_posts)
        return redirect(url_for('read'))
    return render_template('write.html', fonts=get_google_fonts())

@app.route('/read')
def read():
    return render_template('read.html', blog_posts=blog_posts)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    global blog_posts
    if 0 <= post_id < len(blog_posts):
        del blog_posts[post_id]
        save_blog_posts(blog_posts)
    return redirect(url_for('read'))

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if not (0 <= post_id < len(blog_posts)):
        return redirect(url_for('read'))
    if request.method == 'POST':
        blog_posts[post_id]['title'] = request.form.get('title', '')
        blog_posts[post_id]['content'] = request.form.get('content', '')
        blog_posts[post_id]['font_family'] = request.form.get('font_family', 'Arial')
        blog_posts[post_id]['background_color'] = request.form.get('background_color', '#222831')
        save_blog_posts(blog_posts)
        return redirect(url_for('read'))
    return render_template('edit.html', post=blog_posts[post_id], post_id=post_id, fonts=get_google_fonts())

@app.route('/view/<int:post_id>')
def view_post(post_id):
    if 0 <= post_id < len(blog_posts):
        post = blog_posts[post_id]
        return render_template('view.html', post=post)
    return redirect(url_for('read'))

def get_google_fonts():
    return [
        "Arial", "Helvetica", "Times New Roman", "Georgia", "Roboto",
        "Open Sans", "Lato", "Montserrat", "Oswald", "Slabo 27px",
        "Poppins", "Raleway", "Ubuntu", "Merriweather", "Playfair Display",
        "Fira Sans", "Nunito", "Quicksand", "Rubik", "Bebas Neue",
        "Dancing Script", "Pacifico", "Bitter", "Source Sans Pro", "Muli",
        "Work Sans", "Cabin", "Josefin Sans", "PT Sans", "Varela Round"
    ]

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image = request.files['image']
        if image:
            image_filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            try:
                image.save(image_path)
                return {'location': url_for('static', filename='uploads/' + image_filename)}
            except Exception as e:
                return {'error': str(e)}
    return {'error': 'No image found'}

if __name__ == '__main__':
    app.run(debug=True)
