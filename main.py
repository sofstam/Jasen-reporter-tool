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
    font-family: arial, helvetica, sans-serif;
	max-width: 1024px;
	background: #fff;
	padding: 1em;
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
<a class="button" onClick="toggleExpandTable(document.getElementById('typing')); toggleLabel(this);">EXPAND TABLE</a>
<div class="wrapper closed" id="typing">
{% for typ in data["typing_result"] %}
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
        <td>{{ typ["result"]["n_novel"] }}</td>  
    </tr>
    <tr>
        <th scope="row">Number of novel</th>
        <td>{{ typ["result"]["n_missing"] }}</td>
    </tr>
</table>
{% endfor %}
</div>

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
    {% endfor %}                                                                                                                                                                                                                                
</table>                                                                              
</div>

<h2>Quality Control (QC)</h2>
<a class="button" onClick="toggleExpandTable(document.getElementById('qualitycontrol')); toggleLabel(this);">EXPAND TABLE</a>
<div class="wrapper closed" id="qualitycontrol"> 
{% for qua in data["qc"] %} 
    <table>
        <tr><th scope="row">Software</th>                             
            <td>{{ qua["software"] }}</td></tr>
        <tr><th scope="row">Version</th>      
            <td>{{ qua["version"] }}</td></tr>
        <tr><th scope="row">Total length</th>                      
            <td>{{ qua["result"]["total_length"] }}</td></tr>    
        <tr><th scope="row">Reference length</th>                      
            <td>{{ qua["result"]["reference_length"] }}</td></tr>    
        <tr><th scope="row">Largest contig</th>                      
            <td>{{ qua["result"]["largest_contig"] }}</td></tr>    
        <tr><th scope="row">Number of contigs</th>               
            <td>{{ qua["result"]["n_contigs"] }}</td></tr>     
        <tr><th scope="row">N50</th>                       
            <td>{{ qua["result"]["n50"] }}</td></tr>                                                  
        <tr><th scope="row">Assembly GC</th>      
            <td>{{ qua["result"]["assembly_gc"] }}</td></tr> 
        <tr><th scope="row">Reference GC</th>                      
            <td>{{ qua["result"]["reference_gc"] }}</td></tr>                                
        <tr><th scope="row">Duplication ratio</th>      
            <td>{{ qua["result"]["duplication_ratio"] }}</td></tr>
        <tr><th scope="row">Software</th>       
            <td>{{ qua["software"] }}</td></tr
        <tr><th scope="row">Version</th>        
            <td>{{ qua["version"] }}</td></tr>                                   
        <tr><th scope="row">Insert size</th>    
            <td>{{ qua["result"]["ins_size"] }}</td></tr>                                         
        <tr><th scope="row">Insert size deviation</th>    
            <td>{{ qua["result"]["ins_size_dev"] }}</td></tr>
        <tr><th scope="row">Mean coverage</th>                 
            <td>{{ qua["result"]["mean_cov"] }}</td></tr>
        <tr><th scope="row">Mapped reads</th>                      
            <td>{{ qua["result"]["mapped_reads"] }}</td></tr>
        <tr><th scope="row">Total reads</th>                    
            <td>{{ qua["result"]["tot_reads"] }}</td></tr>                                                     
        <tr><th scope="row">IQR Median</th>    
            <td>{{ qua["result"]["iqr_median"]}} </td></tr>           
    </table>
{% endfor %}
</div> 
</body>
</html>
''')
#TODO: Split typing results into two tables based on software
#TODO: Split Quality control results into two tables based on software
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