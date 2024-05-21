import sys
import hou

def replace():
    parms = kwargs["parms"]
    parm = parms[0]
    pattern = parm.eval()
    node = parms[0].node()
    referenced_input_index = 0


    attrName = "name"
    button_idx, values = hou.ui.readMultiInput(title = "Set Parms To Search Selected", message = "", buttons = ["Accept","Cancel"], severity = hou.severityType.Message, default_choice=0, close_choice=-1, help=None, 
                                               input_labels     = ["Attribute Name", "Referenced Input"], 
                                               initial_contents = (attrName,         str(referenced_input_index)))
    if button_idx == 0:
        attrName = values[0]
        referenced_input_index = int(values[1])
    else:
        return
    referenced_input_node = node.inputs()[referenced_input_index]
    geo = referenced_input_node.geometry()

    if button_idx == -1 or referenced_input_node is None:
        geo = node.geometry()
    componentType = sys.argv[1]

    elems = []
    if componentType == "point":
        elems = geo.globPoints(pattern)
    elif componentType == "vertex":
        elems = geo.globVertices(pattern)
    elif componentType == "primitive":
        elems = geo.globPrims(pattern)

    # find attr
    values = set()
    for elem in elems:
        values.add(elem.attribValue(attrName))
    parmStr = ""
    for value in values:
        parmStr += "@{}={} ".format(attrName, value)
    parm.set(parmStr)

replace()
