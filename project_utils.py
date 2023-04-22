

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
    #<img src="data:image/png;base64,{encode_base64_from_bytes(convert_chart_fig_to_bytes(chart_fig, width, height))}" alt="Red dot" />
    
def download_pdf(uploaded_image, bounding_image,cell_disease_table, bar_chart, doughnut_chart,width,height):
    return generate_pdf(encode_PIL_Image_to_base64(uploaded_image), encode_PIL_Image_to_base64(bounding_image),cell_disease_table, encode_base64_from_bytes(convert_chart_fig_to_bytes(bar_chart, width, height)), encode_base64_from_bytes(convert_chart_fig_to_bytes(doughnut_chart, width, height)))

def generate_pdf(uploaded_image, bounding_image,cell_disease_table, bar_chart, doughnut_chart):
  tablestr='<table style="text-align: center !important; padding: 1px !important; border: 2px solid black !important; border-collapse: collapse !important; font-size: large !important;"><tr>'
  for i in list(cell_disease_table.columns):
    tablestr+=f'<th style="text-align: center !important; padding: 1px !important; border: 2px solid black !important; border-collapse: collapse !important; font-size: large !important;">{i}</th>'
  
  tablestr+='</tr>'

  for index, row in cell_disease_table.iterrows():
    tablestr+=f'<tr><td style="text-align: center !important; padding: 1px !important; border: 2px solid black !important; border-collapse: collapse !important; font-size: large !important;">{str(index+1)}</td>'
    tablestr+=f'<td style="text-align: center !important; padding: 1px !important; border: 2px solid black !important; border-collapse: collapse !important; font-size: large !important;">{row["Classes"]}</td>'
    tablestr+=f'<td style="text-align: center !important; padding: 1px !important; border: 2px solid black !important; border-collapse: collapse !important; font-size: large !important;">{row["Count"]}</td>'
    tablestr+=f'<td style="text-align: center !important; padding: 1px !important; border: 2px solid black !important; border-collapse: collapse !important; font-size: large !important;">{row["Percentage"]}</td></tr>'

  tablestr+='</table>'

  HTML_TEMPLATE=f"""<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>
<div style="width:816px; height:1054px; padding:0px; margin:0px ;text-align:center; border: 10px solid red">
<div style="content: ""; display: table; clear: both;">
  <div style="float: left; width: 50%;">
  <span style="font-size:20px; font-weight:bold">Uploaded Image</span>
       <br>
              <br>
  <img src="data:image/png;base64,{uploaded_image}" alt=""  width="300" height="300" />
  </div>
  <div style="float: left; width: 50%;">
  <span style="font-size:20px; font-weight:bold">Predicted Image</span>
       <br>     
       <br>
  <img src="data:image/png;base64,{bounding_image}" alt=""  width="300" height="300" />
  </div>
</div>
<div style="content: ""; display: table; clear: both;">
  <div style="float: left; width: 50%;">
  <span style="font-size:20px; font-weight:bold">Detected Cells in table</span>
       <br>
              <br>
  {tablestr}
             
    </div>
    <div style="float: left; width: 50%;">
  <span style="font-size:20px; font-weight:bold">Bar Chart</span>
       <br>
              <br>
              <img src="data:image/png;base64,{bar_chart}" alt="" />
  </div>               
</div>   
<div style="content: ""; display: table; clear: both;">
  <div style="width: 100%;">
  <span style="font-size:20px; font-weight:bold">doughnut chart</span>
       <br>
              <br>
               <img src="data:image/png;base64,{doughnut_chart}" alt="" />
          </div>        
    </div>
</div>
</body>
</html>"""
  return HTML(string=HTML_TEMPLATE).write_pdf(optimize_size=())
