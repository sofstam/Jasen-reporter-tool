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
        <title>{{ data["species_prediction"]["scientific_name"] }}</title>
        <style>
            body {
                font-family: sans-serif;
            }
            table {
                padding-top: 15px;
                border-collapse: collapse;
                width: 98%;
                margin-bottom: 1em;
            }
            td, th {
                border: 2px solid grey;
                text-align: left;
                padding:8px;
            }
            h2 {
                border-bottom: 1px solid #000;
                margin: 2em 0 0 0;
                padding: 0 0 .3em 0;
            }
        </style>
      </head>
      <body>
        <h1>Jasen reporter tool</h1>
        <h2>Species prediction</h2>
        <table>
            <tr>
                <th>Scientific name</th>
                <th>Taxonomy ID</th>
                <th>Taxonomy level</th>
                <th>Fraction of total reads</th>
                <th>Kraken assigned reads</th>
                <th>Added reads</th>
            </tr>
        {% for sp in data["species_prediction"] %} 
            <tr>
                <td> {{sp["scientific_name"]}} </td>
                <td> {{sp["taxonomy_id"]}} </td>
                <td> {{sp["taxonomy_lvl"]}} </td>
                <td> {{sp["fraction_total_reads"]}} </td>
                <td> {{sp["kraken_assigned_reads"]}} </td>
                <td> {{sp["added_reads"]}} </td>
            </tr>
        {% endfor %}
        </table>
        <h2>Typing</h2>
        {% for typ in data["typing_result"] %}
        <table>
            <tr>
                <th scope="row" width="150">Software</th>
                <td> {{typ["software"]}} </td>
            </tr>
            <tr>
                <th scope="row">Type</th>
                <td> {{typ["type"]}} </td>
            </tr>
            <tr>
                <th scope="row">Scheme</th>
                <td> {{typ["result"]["scheme"] | default('N/A')}} </td>
            </tr>
            <tr>
                <th scope="row">Sequence type</th>
                <td> {{typ["result"]["sequence_type"] | default('N/A')}} </td>
            </tr>
            <tr>
                <th scope="row">Number of missing</th>
                <td> {{typ["result"]["n_novel"]}} </td>  
            </tr>
            <tr>
                <th scope="row">Number of novel</th>
                <td> {{typ["result"]["n_missing"]}} </td>
            </tr>
        </table>
        {% endfor %}
        <h2>Other predictions</h2>
        <h3>Report from resfinder</h3>
        <table>
            <tr>
                <th>Resistant</th>
                <th>Susceptible</th>
            </tr>
        {% for phe in data["element_type_result"] %} 
            <tr>
                <td> {{phe["result"]["phenotypes"]["susceptible"]}} </td>
                <td> {{phe["result"]["phenotypes"]["resistant"]}} </td>
            </tr>
        {% endfor %}
        </table>
      </body>
    </html>
    ''')

    # { % -
    # for item in item_list %}
    # {{item}}
    # { % if not loop.last %}, { % endif %}
    # { % - endfor %}

    html = tmpl.render(
        data=jsondata,
        #    variable='Value with <unsafe> data',
        #    item_list=[1, 2, 3, 4, 5, 6]
    )

    with open("testreport.html", "w") as outfile:
        outfile.write(html)