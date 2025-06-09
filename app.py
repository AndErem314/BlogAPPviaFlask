import json
import os
from flask import Flask, request, redirect, url_for, abort, render_template

app = Flask(__name__)


def get_blog_file_path():
    """Return the full path to the blog posts JSON file."""
    return os.path.join(app.root_path, 'data', 'blog_posts.json')


def read_posts():
    """Read blog posts from the JSON file."""
    file_path = get_blog_file_path()
    with open(file_path, 'r') as f:
        return json.load(f)


def write_posts(posts):
    """Write blog posts to the JSON file."""
    file_path = get_blog_file_path()
    with open(file_path, 'w') as f:
        json.dump(posts, f, indent=4)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Handle the addition of a new blog post"""
    if request.method == 'POST':
        blog_posts = read_posts()

        new_id = max((post['id'] for post in blog_posts), default=0) + 1
        new_post = {
            'id': new_id,
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content')
        }

        blog_posts.append(new_post)
        write_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete a blog post by ID"""
    blog_posts = read_posts()
    original_count = len(blog_posts)

    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    if len(blog_posts) == original_count:
        abort(404)

    write_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update an existing blog post by ID"""
    blog_posts = read_posts()
    post = next((p for p in blog_posts if p['id'] == post_id), None)

    if post is None:
        abort(404)

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        write_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.errorhandler(404)
def not_found(e):
    """Render the 404 error page."""
    return render_template('404.html'), 404


@app.route('/')
def index():
    """Render the index page with all blog posts."""
    blog_posts = read_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)