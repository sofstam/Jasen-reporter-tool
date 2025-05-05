from jinja2 import Template
import json

#template = Template('Hello {{ name }}!')
#print
#template.render(name='John Doe')

with open("jasenresult.example.json", "r") as jsonfile:
    jsondata = json.load(jsonfile)

tmpl = Template(u'''\
<!DOCTYPE html>
<html>
  <head>
    <title>{{ data["sample_id"] }}</title>
    <style>
        body {
            font-family: sans-serif;
        }
    </style>
  </head>
  <body>
    <h1>{{ data["sample_id"] }}</h1>
    <h4>Databases</h4>
    <table>
        <tr>
            <th>Name</th>
        </tr>
        <tr>
    {% for db in data["run_metadata"]["databases"] %} 
        <tr>
            <td> {{db["name"]}} </td>
        </tr>
    {% endfor %}
    </table>
  </body>
</html>
''')

#{ % -
#for item in item_list %}
#{{item}}
#{ % if not loop.last %}, { % endif %}
#{ % - endfor %}

html = tmpl.render(
    data=jsondata,
#    variable='Value with <unsafe> data',
#    item_list=[1, 2, 3, 4, 5, 6]
)

with open("report.html", "w") as outfile:
    outfile.write(html)