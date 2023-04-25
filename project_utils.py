

import io
from PIL import Image
import base64
import plotly
import plotly.express as px
from weasyprint import HTML,CSS

def convert_chart_fig_to_bytes(chart_fig, width, height):
  return plotly.io.to_image(chart_fig, format=None, width=width, height=height, scale=None, validate=True, engine='kaleido')
    
#def encode_to_base64(varobj):
#    return base64.b64encode(varobj)
#  return base64.b64encode(varobj.getvalue()).decode('utf-8')

#def encode_to_base64(varobj):
#    #img = Image.fromarray(varobj, 'RGB')
#    image_bytes=''
#    with io.BytesIO() as buf:
#      varobj.save(buf, 'jpeg')
#      image_bytes = buf.getvalue()
#    #byteimg = io.BytesIO()
#    #varobj.save(byteimg,format="PNG")
#    #byteimg.seek(0)
#    #img_bytes = byteimg.read()
#    return base64.b64encode(image_bytes)

def encode_PIL_Image_to_base64(imgobj):
  im_file = io.BytesIO()
  imgobj.save(im_file, format="JPEG")
  im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
  im_b64 = base64.b64encode(im_bytes)
  return im_b64.decode('utf-8')

def encode_base64_from_bytes(bytesobj):
  return base64.b64encode(bytesobj).decode('utf-8')
    
def download_pdf(uploaded_image, bounding_image, cell_disease_table, RBC_status_table, bar_chart, doughnut_chart, width, height):
  return generate_pdf(encode_PIL_Image_to_base64(uploaded_image), encode_PIL_Image_to_base64(bounding_image), cell_disease_table, RBC_status_table, encode_base64_from_bytes(convert_chart_fig_to_bytes(bar_chart, width, height)), encode_base64_from_bytes(convert_chart_fig_to_bytes(doughnut_chart, width, height)), width, height)

def generate_pdf(uploaded_image, bounding_image,cell_disease_table, RBC_status_table, bar_chart, doughnut_chart, width, height):
  image_height=height
  image_width=width
  bar_chart_width=width
  bar_chart_height=height
  doughnut_chart_width=width
  doughnut_chart_height=height

  cell_disease_table_str='<table><tr>'
  RBC_status_table_str='<table><tr>'

  for i in list(RBC_status_table.columns):
    RBC_status_table_str+=f'<th>{i}</th>'
  
  for i in list(cell_disease_table.columns):
    cell_disease_table_str+=f'<th>{i}</th>'
  
  RBC_status_table_str+='</tr>'
  cell_disease_table_str+='</tr>'

  for index, row in RBC_status_table.iterrows():
    RBC_status_table_str+=f'<td>{row["HbA"]}</td>'
    RBC_status_table_str+=f'<td>{row["HbS"]}</td>'
    RBC_status_table_str+=f'<td>{row["HbC"]}</td>'
    RBC_status_table_str+=f'<td>{row["Status"]}</td></tr>'

  for index, row in cell_disease_table.iterrows():
    cell_disease_table_str+=f'<tr><td>{str(index+1)}</td>'
    cell_disease_table_str+=f'<td>{row["Classes"]}</td>'
    cell_disease_table_str+=f'<td>{row["Count"]}</td>'
    cell_disease_table_str+=f'<td>{row["Percentage"]}</td></tr>'

  cell_disease_table_str+='</table>'

  HTML_TEMPLATE=f"""
<!DOCTYPE html>
<html>
<head>
<title></title>
</head>
<body>
<div style='content: ""; display: table; clear: both;'>
  <div style='float: left; width: 50%;'>
  <span style="font-size:20px; font-weight:bold">Uploaded Image</span>
  <br>
  <br>
  <img class="imagesize" src="data:image/png;base64,{uploaded_image}" alt="uploaded image" />
  </div>
  <div style='float: left; width: 50%;'>
  <span style="font-size:20px; font-weight:bold">Diagnose disease cells</span>
  <br>     
  <br>
  <img class="imagesize" src="data:image/png;base64,{bounding_image}" alt="predicted image" />
  </div>
</div>
<div style='content: ""; display: table; clear: both;'> 
<span style="font-size:20px; font-weight:bold">Total diagnose detected classified cells are: {cell_disease_table['Count'].sum()}</span>
</div>
  <br>
  <br>
<div style='content: ""; display: table; clear: both;'> 
  <span style="font-size:20px; font-weight:bold">Detected cells details</span>
</div>
  <br>
  <br>  
<div style='content: ""; display: table; clear: both;'>
  <div style='float: left; width: 50%;'>
  {cell_disease_table_str}
  </div>
  <div style='float: left; width: 50%;'>
  {RBC_status_table_str}
  </div>               
</div>   
<div style='content: ""; display: table; clear: both;'>
  <span style="font-size:20px; font-weight:bold">Analysis of detected diseases cells</span>
</div>
<div style='content: ""; display: table; clear: both;'>
  <br>              
  <img class="barchartsize" src="data:image/png;base64,{bar_chart}"  alt="bar chart image"  />         
</div>   
<div style='content: ""; display: table; clear: both;'>
  <br>
  <img class="doughnutchartsize" src="data:image/png;base64,{doughnut_chart}" alt="doughnut chart image" />
</div>
</div>
</body>
</html>
"""
  css=CSS(string=f'''@page {{size: Letter; margin: 0.1in 0.1in 0in 0.1in;}}
      img {{border: 5px solid #555;}}
      body{{display: block; margin: 0px;}}
      .imagesize{{height: {image_height}px; width: {image_width}px; margin: 0 auto;}}  
      .barchartsize{{height: {bar_chart_height}px; width: {bar_chart_width}px; margin: 0 auto;}} 
      .doughnutchartsize{{height: {doughnut_chart_height}px; width: {doughnut_chart_width}px; margin: 0 auto;}} 
       table,th,td{{text-align: center !important; padding: 1px !important; border: 2px solid black !important; border-collapse: collapse !important; font-size: large !important;"}}
      .column {{float: left; width: 50%; }}
      .row {{ content: ""; display: table; clear: both; }}
      ''')

  return HTML(string=HTML_TEMPLATE).write_pdf(optimize_size=(), stylesheets=[css])
