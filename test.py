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
            address {
                display: block;
                font-style: normal;
            }
            adress-table {
            }
            .table-container {
                border: 2.5px solid grey;
                background-color: #E8E8E8;
                width: 98%;
            }
            table {
                table-layout: fixed;
                padding-top: 15px;
                padding-right: 0;
                border-collapse: collapse;
                width: 98%;
                max-height: 10px;
                overflow-y: auto;
                margin-bottom: 1em;
            }
            th {
                border-top: none;
                border-bottom: 2px solid grey;
                border-right: 2px solid grey; 
                text-align: left;
                padding:8px;
            }
            td {
                border-right: 2px solid grey;
                border-top: none;
                border-bottom: none;
                text-align: left;
                padding:8px;
            }
            h2 {
                border-bottom: 1px solid #000;
                margin: 2em 0 0 0;
                padding: 0 0 .3em 0;
            }
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
      <h1>Jasen reporter tool</h1>
      <div class="row">
        <div class="col">
            <h2 style="font-weight:normal">Contact</h2>
            <adress>
                <strong>Clinical Genomics</strong><br>
                Science for Life Laboratory<br>
                Tomtebodavägen 23<br>
                171 65 Solna<br>
                <abbr title="Telefonnummer">T:</abbr> (08) 524 81 500
            </adress>
        </div>
        <div class="col">
            <h2 style="font-weight:normal">Customer</h2>
            <address>
                Testing<br>
            </adress>
            <adress>
                <strong>JASEN-teamet</strong><br>
                <abbr title="Förslagslåda">E:</abbr><a href="mailto:jasen-suggestions@scilifelab.se?subject=Förbättringsförslag">
                jasen-suggestions@scilifelab.se
                </a>
            </address>
        </div>
      </div>
        <h2>Species prediction</h2>
        <div class="table-container">
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
        <h2>Quality Control (QC)</h2>    
        <h3></h3>
        {% for qua in data["qc"] %} 
        <table>
            <tr><th scope="row">Software</th>                             
                <td> {{ qua["software"] }} </td></tr>
            <tr><th scope="row">Version</th>      
                <td> {{ qua["version"] }} </td></tr>
            <tr><th scope="row">Total length</th>                      
                <td> {{ res["total_length"] }} </td></tr>    
            <tr><th scope="row">Reference length</th>                      
                <td> {{ res["reference_length"] }} </td></tr>    
            <tr><th scope="row">Largest contig</th>                      
                <td> {{ res["largest_contig"] }} </td></tr>    
            <tr><th scope="row">Number of contigs</th>               
                <td> {{ res["n_contigs"] }} </td></tr>     
            <tr><th scope="row">N50</th>                       
                <td> {{ res["n50"] }} </td></tr>                                                  
            <tr><th scope="row">Assembly GC</th>      
                <td> {{ res["assembly_gc"] }} </td></tr> 
            <tr><th scope="row">Reference GC</th>                      
                <td> {{ res["reference_gc"] }} </td></tr>                                
            <tr><th scope="row">Duplication ratio</th>      
                <td> {{ res["duplication_ratio"] }} </td></tr>
        </table>            
        {% endfor %}
        {% for qua in data["qc"] %}       
        <table>
            <tr><th scope="row">Software</th>       
                <td> {{ qua["software"] }} </td></tr
            <tr><th scope="row">Version</th>        
                <td> {{ qua["version"] }} </td></tr>                                   
            <tr><th scope="row">Insert size</th>    
                <td> {{ res["ins_size"] }} </td></tr>                                         
            <tr><th scope="row">Insert size deviation</th>    
                <td> {{ res["ins_size_dev"] }} </td></tr>
            <tr><th scope="row">Mean coverage</th>                 
                <td> {{ res["mean_cov"] }} </td></tr>
            <tr><th scope="row">Mapped reads</th>                      
                <td> {{ res["mapped_reads"] }} </td></tr>
            <tr><th scope="row">Total reads</th>                    
                <td> {{ res["tot_reads"] }} </td></tr>                                                     
            <tr><th scope="row">IQR Median</th>    
                <td> {{ res["iqr_median"] }} </td></tr>           
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