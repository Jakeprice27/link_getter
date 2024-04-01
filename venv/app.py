from flask import Flask, render_template, request, flash
from bs4 import BeautifulSoup
import urllib.request
import ssl
from urllib.parse import urljoin

app = Flask(__name__, template_folder="templates")

app.secret_key = 'jake_price'

# Disable SSL verification
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

@app.route('/')
def index():
    flash("Please enter the URL you would like to get links from.")
    return render_template("index.html")


@app.route('/get_urls', methods=['POST'])
def get_urls():
    user_input = request.form.get('user_input')

    surfaceable_links = []  # Initialize the variable here

    try:
        page = urllib.request.urlopen(user_input, context=context)
        text = page.read()
        doc = BeautifulSoup(text, 'html.parser')

        # Get all the tags
        a_tags = doc.find_all('a')

        for tag in a_tags:
            href = tag.get('href')
            if href:
                absolute_url = urljoin(user_input, href)
                surfaceable_links.append(absolute_url)

    except Exception as e:
        error_message = f"Error fetching URL: {str(e)}"
        return render_template("error.html", error_message=error_message)

    final_links = [link for link in surfaceable_links if link.startswith("https://") or link.startswith("http://")]

    return render_template("scrape_results.html", url=user_input, links=final_links)


if __name__ == '__main__':
    app.run(debug=True)