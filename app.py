"""
Serve new combined calendar
"""

import os
import json
from flask import Flask
from waitress import serve
from combine_calendars import ExistingCalendar, generate_combined_calendar

ROOT_PATH = "/motorsport-calendar"

app = Flask(__name__)

cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, 'config.json')) as f:
    config = json.load(f)

all_pages: list[dict] = [{}]

for page in config['pages']:
    existing_calendars = []
    page_name = page['name']
    all_pages.append({
        'name': page_name,
        'path': f"/{page['path']}"
    })

    for calendar in page['calendars']:
        existing_calendar = ExistingCalendar(calendar['name'],
                                             calendar['description'],
                                             calendar['url'])
        existing_calendars.append(existing_calendar)

    route_path = f"{ROOT_PATH}/{page['path']}"

    @app.route(route_path)
    def combine_calendar_page(existing_calendars=existing_calendars, page=page):
        """
        Return combined calendar in ics format
        """
        return generate_combined_calendar(page['name'], existing_calendars).serialize()

@app.route(ROOT_PATH)
def index():
    """
    Return index of available combined calendars
    """
    index_lines = ['<h1>Available Combined Calendars</h1>', '<ul>']
    for page in all_pages[1:]:
        index_lines.append(f'<li><a href="{ROOT_PATH}{page["path"]}">{page["name"]}</a></li>')
    index_lines.append('</ul>')
    return '\n'.join(index_lines)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)