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
        table {
        table-layout: fixed;
        max-height: 3px;
        overflow-y: auto;
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
    <div style="overflow-y: scroll;">
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
    </div>
    <h3>Report from resfinder</h3>                                                         
    <div style="overflow-y: scroll;">                                                     
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
</div>
{% for qua in data["qc"] %}                                                 
<table>                                                                     
    <tr><th scope="row">Software</th>                                       
        <td> {{ qua["software"] }} </td></tr>                               
    <tr><th scope="row">Version</th>                                        
        <td> {{ qua["version"] }} </td></tr>                                
    <tr><th scope="row">Assembly GC</th>                                    
        <td> {{ qua["result"]["assembly_gc"] }} </td></tr>                  
    <tr><th scope="row">Duplication ratio</th>                              
        <td> {{ qua["result"]["duplication_ratio"] }} </td></tr>                 
</table>                                                                    
{% endfor %}                                                                                                                                                                  
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

with open("tabletestreport.html", "w") as outfile:
    outfile.write(html)