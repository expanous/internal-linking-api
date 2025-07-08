import xml.etree.ElementTree as ET
import yaml

sitemap_file = 'sitemap-en-int-0.xml'
yaml_output = 'urls.yaml'

urls = []

# Use iterparse for memory efficiency
for event, elem in ET.iterparse(sitemap_file, events=("end",)):
    if elem.tag.endswith('url'):
        loc = elem.find('{*}loc')
        if loc is not None and loc.text:
            urls.append(loc.text.strip())
        # Clear the element to free memory
        elem.clear()

with open(yaml_output, 'w') as f:
    yaml.dump(urls, f, default_flow_style=False, allow_unicode=True)

print(f"Extracted {len(urls)} URLs to {yaml_output}") 