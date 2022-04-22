"""
1. find appropriate svg elements.
2. Add hover attribute to svg elements and event to call `show_motion_details`
"""
import xml.etree.ElementTree as ET

def read_host(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    pass

"""

{{ svg_string }}

<script>
{{ collection_json }}
</script>

<script>
function show_motion_details(channel_id) {

}
</script>
"""
