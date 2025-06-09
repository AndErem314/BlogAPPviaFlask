import json
import os
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Path to the JSON file
        file_path = os.path.join(app.root_path, 'data', 'blog_posts.json')

        # Load existing posts
        with open(file_path, 'r') as f:
            blog_posts = json.load(f)

        # Generate a unique ID: find the max current ID and add 1
        if blog_posts:
            new_id = max(post['id'] for post in blog_posts) + 1
        else:
            new_id = 1

        # Create new post dictionary
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Append the new post and save back to JSON file
        blog_posts.append(new_post)
        with open(file_path, 'w') as f:
            json.dump(blog_posts, f, indent=4)

        # Redirect to the index page
        return redirect(url_for('index'))

    # GET request renders the form
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    file_path = os.path.join(app.root_path, 'data', 'blog_posts.json')

    # Load current posts
    with open(file_path, 'r') as f:
        blog_posts = json.load(f)

    # Filter out the post with the given ID
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated list
    with open(file_path, 'w') as f:
        json.dump(blog_posts, f, indent=4)

    return redirect(url_for('index'))


@app.route('/')
def index():
    # Construct the path to the JSON file in the 'data' folder
    file_path = os.path.join(app.root_path, 'data', 'blog_posts.json')

    with open(file_path, 'r') as fileobj:
        blog_posts = json.load(fileobj)

    return render_template('index.html', posts=blog_posts)