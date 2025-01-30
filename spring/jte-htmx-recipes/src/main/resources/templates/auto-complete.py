from flask import Flask, request, render_template_string

app = Flask(__name__)

# Sample data for the search
SEARCH_RESULTS = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    suggestions = [item for item in SEARCH_RESULTS if query in item.lower()]

    # Return HTML template for suggestions
    return render_template_string(
        '''
        {% for suggestion in suggestions %}
        <div
            class="px-4 py-2 cursor-pointer hover:bg-gray-100"
            hx-get="/select/{{ suggestion }}"
            hx-target="#search-box"
            hx-swap="outerHTML"
        >
            {{ suggestion }}
        </div>
        {% endfor %}
        ''',
        suggestions=suggestions
    )

@app.route('/select/<item>')
def select_item(item):
    # Return the selected suggestion to replace the input field value
    return f'<input type="text" value="{item}" class="block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-300 focus:outline-none">'

if __name__ == '__main__':
    app.run(debug=True)