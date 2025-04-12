# Function to handle extraction of all vertecies, even those with metadata.
# Written for extensibility, not efficiency.

meta_objects = [element for element in $XML.findall("diagram/mxGraphModel/root/UserObject")]
standard_objects = [element for element in $XML.findall("diagram/mxGraphModel/root/mxCell")]
meta_object_dict = dict()
standard_object_dict = dict()
is_meta_dict = dict()
connectable_dict = dict()
cell_ids = set()
vertex_ids = set()
edge_ids = set()

for mo in meta_objects:
  cell = mo.find("mxCell")
  cell_id = cell.get("id",default=mo.get("id"))
  meta_object_dict[cell_id] = mo
  standard_object_dict[cell_id] = cell
  is_meta_dict[cell_id] = True
  if cell.get("vertex",default=0):
    vertex_ids.add(cell_id)
  if cell.get("edge",default=0):  
    edge_ids.add(cell_id) 
  cell_ids.add(cell_id)

for so in standard_objects:
  cell = so
  cell_id = cell.get("id")
  is_meta_dict[cell_id] = False
  standard_object_dict[cell_id] = so
  if cell.get("vertex",default=0):
    vertex_ids.add(cell_id)
  if cell.get("edge",default=0):  
    edge_ids.add(cell_id) 
  cell_ids.add(cell_id)
  
def label_cleaner(label):
  label = label.replace("\n","_")
  label = label.replace("<b>","")
  label = label.replace("</b>","")
  label = label.replace("<div>","")
  label = label.replace("</div>","")
  label = label.replace("<i>","")
  label = label.replace("</i>","")
  label = label.replace("&lt;","<")
  label = label.replace("&gt;",">")
  label = label.replace("","")
  return label
  
txt = []

for id in vertex_ids:
  label = "?"
  cell = standard_object_dict[id]
  not_connectable = ((cell.get("connectable") == "0") or ("connectable=0" in cell.get("style")))
  
  if is_meta_dict[id]:
    label = meta_object_dict[id].get("label",default="No Label In Meta")
  else:
    label = cell.get("value",default="No value in cell")
    
  label = label_cleaner(label)
  txt.append(f"id:{id} label:{label} not_con: {not_connectable}")

return "\n".join(txt)