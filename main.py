from jinja2 import Template
import json

#template = Template('Hello {{ name }}!')
#print
#template.render(name='John Doe')
#alternative file: jasenresult.example.json    "SRR12146775_result.json"

with open("jasenresult.example.json", "r") as jsonfile:
    jsondata = json.load(jsonfile)

tmpl = Template(u'''\
<!DOCTYPE html>
<html>
<head>
    <title>Sample: {{ data["sample_id"] }}</title>
<style>
body {
    font-family: arial, helvetica, sans-serif;
	max-width: 1024px;
	background: #fff;
	padding: 1em;
}

h2 {
    border-bottom: 1px solid #000;
}

address {
    display: block;
    font-style: normal;
}

.table-adress {
    text-align: left;
    font-size: 10pt;
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

a.button,
a.button:link,
a.button:visited,
a.button:active {
	text-decoration: none;
	display: inline-block;
	padding: .4em;
	margin: 1em 0;
	background: #ccc;
	color: black;
	font-size: .8em;
}

a.button:hover {
	background: #aaa;
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
<h1>Jasen report for sample: {{ data["sample_id"] }}</h1>
<div class="table-adress">
<table>
    <tr>
        <th><h2 style="font-weight:normal; border-bottom: none;">Contact</h2></th>
        <th><h2 style="font-weight:normal; border-bottom: none;">Customer</h2></th>
    </tr>
    <tr>
        <td>
            <address>
                <strong>Clinical Genomics</strong><br>
                Science for Life Laboratory<br>
                Tomtebodavägen 23<br>
                171 65 Solna<br>
                <abbr title="Telefonnummer">T:</abbr> (08) 524 81 500
            </address>
        </td>
        <td>
            <address>
                <h3 style="font-weight:normal">testing</h4><br>
            </address>
            <address>
                <strong>JASEN-team</strong><br>
                <abbr title="Förslagslåda">E:</abbr><a href="mailto:jasen-suggestions@scilifelab.se?subject=Förbättringsförslag">
                jasen-suggestions@scilifelab.se
                </a>
            </address>
        </td>
    </tr>
</table>
</div>
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

<h2>Typing</h2>
{% for typ in data["typing_result"] %}
<a class="button" onClick="toggleExpandTable(document.getElementById('typing{{loop.index}}')); toggleLabel(this);">EXPAND TABLE</a>
<div class="wrapper closed" id="typing{{loop.index}}">
<table>
    <tr>
        <th scope="row">Software</th>
        <td> {{typ["software"]}} </td>
    </tr>
    <tr>
        <th scope="row">Type</th>
        <td>{{ typ["type"] }} </td>
    </tr>
    <tr>
        <th scope="row">Scheme</th>
        <td>{{ typ["result"]["scheme"] | default('N/A') }}</td>
    </tr>
    <tr>
        <th scope="row">Sequence type</th>
        <td>{{ typ["result"]["sequence_type"] | default('N/A') }}</td>
    </tr>
    <tr>
        <th scope="row">Number of missing</th>
        <td>{{ typ["result"]["n_novel"] | default('N/A') }}</td>  
    </tr>
    <tr>
        <th scope="row">Number of novel</th>
        <td>{{ typ["result"]["n_missing"] | default('N/A') }}</td>
    </tr>
    {% for label, allele in typ["result"]["alleles"].items() %}
        {% if allele != 'LNF' %}  
    <tr>
        <th scope="row">{{ label }}</th>
        <td>{{ allele }}</td>
    </tr>
        {% endif %}
    {% endfor %}
</table>
</div>
{% endfor %}

<h2>Other predictions</h2>
<h3>Report from resfinder</h3>
<a class="button" onClick="toggleExpandTable(document.getElementById('resprediction')); toggleLabel(this);">EXPAND TABLE</a>
<div class="wrapper closed" id="resprediction">                                                     
<table>                                                                               
    <tr>                                                                              
        <th>Resistant</th>                                                            
        <th>Susceptible</th>                                                          
    </tr>                                                                                                                                             
    {% for phe in data["element_type_result"] %}
    {% if phe["software"] == "resfinder" %}                                                 
    <tr>                                                                                      
        <td style="vertical-align: top;">
        <table>
        {% for row in phe["result"]["phenotypes"]["resistant"] %}
            <tr><td>{{ row }}</td></tr>
        {% endfor %}
        </table>
        </td>                     
        <td style="vertical-align: top;"> 
        <table>
        {% for row in phe["result"]["phenotypes"]["susceptible"] %}
            <tr><td>{{ row }}</td></tr>
        {% endfor %}
        </table>
        </td>                               
    </tr>
    {% endif %}                                                                                     
    {% endfor %}                                                                                                                                                                                                                                
</table>                                                                              
</div>

<h3>Report from amrfinder</h3>
<a class="button" onClick="toggleExpandTable(document.getElementById('amrfinder')); toggleLabel(this);">EXPAND TABLE</a>
<div class="wrapper closed" id="amrfinder">                                                     
<table>
    {% for gen in data["element_type_result"] %} 
    {% if gen["software"] == "amrfinder" and gen["type"] == "AMR" %}                                                                               
        <tr>
            <th>Number</th>
            <th>Gene</th>
            <th>Group</th>
            <th>Reference</th>
            <th>Identity %</th>
        </tr>  
        {% for row in gen["result"]["genes"] %}
        <tr>
            <td>test</td>
            <td>{{ row["gene_symbol"] }}</td>
            <td>{{ row["res_class"] }}</td>
            <td>{{ row["ref_id"] }}</td>
            <td>{{ row["identity"] }}</td>
        </tr>
        {% endfor %}
    {% endif %}
    {% endfor %}
</table>
</div>

<h2>Quality Control (QC)</h2>
{% for qua in data["qc"] %}
<a class="button" onClick="toggleExpandTable(document.getElementById('qc{{loop.index}}')); toggleLabel(this);">EXPAND TABLE</a>
<div class="wrapper closed" id="qc{{loop.index}}">
    <table>
        <tr><th scope="row">Software</th>                             
            <td>{{ qua["software"] }}</td></tr>
        <tr><th scope="row">Version</th>      
            <td>{{ qua["version"] }}</td></tr>
        {% for label, res in qua["result"].items() %}
{# This really does not want to work
            {% if res == "pct_above_x" %}
                {% for lab, pct in res.items() %} 
                <tr><th scope="row">{{ lab }}</th>
                <td>{{ pct }}</td></tr>
            {% elif res %}
                <tr><th scope="row">{{ label.replace("_", " ").capitalize() }}</th>                      
                <td>{{ res }}</td></tr>
            {% endif %}
        {% endfor %}
#}
            {% if res %}
                <tr><th scope="row">{{ label.replace("_", " ").capitalize() }}</th>                      
                <td>{{ res }}</td></tr>
            {% endif %}
        {% endfor %}         
    </table>
</div>
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

with open("report.html", "w") as outfile:
    outfile.write(html)