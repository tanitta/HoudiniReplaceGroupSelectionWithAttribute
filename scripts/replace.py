import sys
import hou

def replace():
    parms = kwargs["parms"]
    parm = parms[0]
    pattern = parm.eval()
    node = parms[0].node()
    referenced_input_index = 0
    componentType = sys.argv[1]
    convert = sys.argv[2]

    attrName = "name"

    if convert == "attr":
        button_idx, values = hou.ui.readMultiInput(title = "Set Parms To Search Selected", message = "", buttons = ["Accept","Cancel"], severity = hou.severityType.Message, default_choice=0, close_choice=-1, help=None, 
                                                   input_labels     = ["Referenced Input",          "Attribute Name", ], 
                                                   initial_contents = (str(referenced_input_index), attrName))
    else:
        button_idx, values = hou.ui.readMultiInput(title = "Set Parms To Search Selected", message = "", buttons = ["Accept","Cancel"], severity = hou.severityType.Message, default_choice=0, close_choice=-1, help=None, 
                                                   input_labels     = ["Referenced Input"], 
                                                   initial_contents = (str(referenced_input_index)))
    if button_idx != 0:
        return

    referenced_input_index = int(values[0])
    geo = node.inputGeometry(referenced_input_index)

    if button_idx == -1 or geo is None:
        geo = node.geometry()

    elems = []
    if componentType == "point":
        elems = geo.globPoints(pattern)
    elif componentType == "vertex":
        elems = geo.globVertices(pattern)
    elif componentType == "primitive":
        elems = geo.globPrims(pattern)
    if convert == "attr":
        attrName = values[1]
        values = set()
        for elem in elems:
            values.add(elem.attribValue(attrName))
        parm_lines = []
        for value in values:
            line = '@{}="{}"'.format(attrName, value)
            parm_lines.append(line)
        parm.set('\n'.join(parm_lines))
    else:
        parm_lines = []
        for elem in elems:
            line = "{}".format(elem.number())
            parm_lines.append(line)
        parm.set(' '.join(parm_lines))

replace()
