from jinja2 import Template

#template = Template('Hello {{ name }}!')
#print
#template.render(name='John Doe')

tmpl = Template(u'''\
<!DOCTYPE html>
<html>
  <head>
    <title>{{ variable|escape }}</title>
  </head>
  <body>
  {%- for item in item_list %}
    {{ item }}{% if not loop.last %},{% endif %}
  {%- endfor %}
  </body>
</html>
''')

html = tmpl.render(
    variable='Value with <unsafe> data',
    item_list=[1, 2, 3, 4, 5, 6]
)

with open("report.html", "w") as outfile:
    outfile.write(html)