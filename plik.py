from flask import Flask, redirect, url_for, render_template
import glob
import markdown

app = Flask(__name__)		# Setting up the application

# Sets the route for each subpage.
# Converts an markdown file to the html file.
@app.route('/opening/<file_name>')
def convert_to_html(file_name):
    path = f"markdown/{file_name}"

    # Opens file and saves it markdown version
    # to html and returns it.
    with open(path, "r") as f:
        text = f.read()
        html = markdown.markdown(text)

    # Create a home link.
    html += f'<p><a href="/"> Go to Main page </a></p>'

    return html

# Sets the route for the main page.
@app.route('/')		
def home():

    # Takes all .md files from markdown folder
    # glob returns pathes to those files.
    all_md = glob.glob("markdown/*.md")

    # Includes interface for the main page.
    html = render_template('main_page.html')

    # For each .md file create link. 
    for md in all_md:
        md = md.replace("markdown/", "")
        html += f'<p><a href="/opening/{md}"> {md} </a></p>' 
    
    return html	

app.run()