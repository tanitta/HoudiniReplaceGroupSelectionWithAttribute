import sys
import hou

def replace():
    parms = kwargs["parms"]
    parm = parms[0]
    pattern = parm.eval()
    node = parms[0].node()
    geo = node.geometry()


    attrName = "name"
    Dialog = hou.ui.readInput(message ="Set Attribute Name To Search\n",title = "Set Attribute Name To Search",severity=hou.severityType.Warning,buttons=["Accept","Cancel"], initial_contents='name')
    if Dialog[0]==0:
        attrName = Dialog[1]
    else:
        return

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
