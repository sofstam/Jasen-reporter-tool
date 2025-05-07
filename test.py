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
                table-layout: fixed;
                padding-top: 15px;
                border-collapse: collapse;
                width: 98%;
                max-height: 10px;
                overflow-y: auto;
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
        <h3></h3>
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
        <h3></h3>
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
        <h2>Quality Control (QC)</h2>    
        <h3></h3>
        {% for qua in data["qc"] %} 
        <table>
            <tr><th scope="row">Software</th>                             
                <td> {{ qua["software"] }} </td></tr>
            <tr><th scope="row">Version</th>      
                <td> {{ qua["version"] }} </td></tr>
            <tr><th scope="row">Total length</th>                      
                <td> {{ qua["result"]["total_length"] }} </td></tr>    
            <tr><th scope="row">Reference length</th>                      
                <td> {{ qua["result"]["reference_length"] }} </td></tr>    
            <tr><th scope="row">Largest contig</th>                      
                <td> {{ qua["result"]["largest_contig"] }} </td></tr>    
            <tr><th scope="row">Number of contigs</th>               
                <td> {{ qua["result"]["n_contigs"] }} </td></tr>     
            <tr><th scope="row">N50</th>                       
                <td> {{ qua["result"]["n50"] }} </td></tr>                                                  
            <tr><th scope="row">Assembly GC</th>      
                <td> {{ qua["result"]["assembly_gc"] }} </td></tr> 
            <tr><th scope="row">Reference GC</th>                      
                <td> {{ qua["result"]["reference_gc"] }} </td></tr>                                
            <tr><th scope="row">Duplication ratio</th>      
                <td> {{ qua["result"]["duplication_ratio"] }} </td></tr>
        </table>            
        {% endfor %}
        {% for qua in data["qc"] %}       
        <table>
            <tr><th scope="row">Software</th>       
                <td> {{ qua["software"] }} </td></tr
            <tr><th scope="row">Version</th>        
                <td> {{ qua["version"] }} </td></tr>                                   
            <tr><th scope="row">Insert size</th>    
                <td> {{ qua["result"]["ins_size"] }} </td></tr>                                         
            <tr><th scope="row">Insert size deviation</th>    
                <td> {{ qua["result"]["ins_size_dev"] }} </td></tr>
            <tr><th scope="row">Mean coverage</th>                 
                <td> {{ qua["result"]["mean_cov"] }} </td></tr>
            <tr><th scope="row">Mapped reads</th>                      
                <td> {{ qua["result"]["mapped_reads"] }} </td></tr>
            <tr><th scope="row">Total reads</th>                    
                <td> {{ qua["result"]["tot_reads"] }} </td></tr>                                                     
            <tr><th scope="row">IQR Median</th>    
                <td> {{ qua["result"]["iqr_median"] }} </td></tr>           
        </table>
        {% endfor %}                                                                                                                                                                                  
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