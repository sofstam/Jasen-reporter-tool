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
            max-height: 70px;
            overflow-y: auto;
        }
        table th {
            text-align: left;
        }
        .grey-table {
            width: 98%;
            border-collapse: collapse;
            background-color: #d3d3d3;
        }
        .grey-table th, .grey-table td {
            border-left: 1px solid #000;
            padding: 8px;
        }
        .grey-table th {
            background-color: #bbb;
        }
        .grey-table td:first-child, .grey-table th:first-child {
        border-left: none;
        }
        .info-table {
            border-collapse: collapse;
            font-weight: normal;
            text-align: left;
        }
        .info-table th {
            font-weight: normal;
            font-size: 10pt;
            padding-right: 400px;,
        }
        .info-table1 th {
            padding-right: 400px;
            font-weight: normal;
            font-size: 15pt;
        }
        .wrapper.closed {
            max-height: 120px;
            overflow: hidden!important;
            border-width: 4px;
            border-style: solid solid dotted solid;
            border-color: #ccc;
            background-image: linear-gradient(#efefef, white);
        }
        .wrapper.open {
            max-height: 120000px;
            border: 4px solid #eec;
            background: #ffffef;
        }
    </style>
    
    <script>
    function toggleExpandTable(obj) {
	    obj.classList.toggle("open");
	    obj.classList.toggle("closed");
    }
    
    function toggleLabel(obj) {
        if (obj.textContent === "EXPAND TABLE") {
            obj.textContent = "COLLAPSE TABLE";
        } else {
            obj.textContent = "EXPAND TABLE";
        }
    }
</script>

  </head>
  <body>
    <h1>Testing tables and layout</h1>
        <div class="info-table1">
        <table>
            <tr><th>Contact Clinical Genomics</th>
                <th>Customer</th></tr>
        </table>
        </div>
    <div class="info-table">
        <table>
            <tr><th style="font-weight: bold">Clinical Genomics</th></tr>
            <tr><th  scope="row">Science for Life Laboratory</th></tr>
            <tr><th  scope="row">Tomtebodavägen 23</th></tr>
            <tr><th  scope="row">171 65 Solna</th></tr>
            <tr><th  scope="row">T: (08) 524 81 500</th></tr>
        </table>
    </div>
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
    <h2>Species prediction</h2>
    <a class="button" onClick="toggleExpandTable(document.getElementById('speciesprediction')); toggleLabel(this);">EXPAND TABLE</a>
    <div class="wrapper closed" id="speciesprediction"> 
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
    <a class="button" onClick="toggleExpandTable(document.getElementById('resprediction')); toggleLabel(this);">EXPAND TABLE</a>
    <div class="wrapper closed" id="resprediction">                                                     
    <table>                                                                               
    <tr>                                                                              
        <th style="text-align: left;">Resistant</th>                                                            
        <th style="text-align: left;">Susceptible</th>                                                          
    </tr>                                                                                                                                             
    {% for phe in data["element_type_result"] %}                                                  
    <tr>                                                                                      
        <td style="vertical-align: top;">
        <table>
        {% for row in phe["result"]["phenotypes"]["resistant"] %}
            <tr><td> {{row}} </td></tr>
        {% endfor %}
        </table>
        </td>                     
        <td style="vertical-align: top;"> 
        <table>
        {% for row in phe["result"]["phenotypes"]["susceptible"] %}
            <tr><td> {{row}} </td></tr>
        {% endfor %}
        </table>
        </td>                               
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