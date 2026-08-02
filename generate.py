from pathlib import Path
from xml.sax.saxutils import escape
from lxml import etree

SVG_FILES = [
    "dark_mode.svg",
]

PROFILE = {
    "name": "Pandu Putra",
    "subtitle": "Software Engineer • AI • Data",

    "focus1": "Web Development",
    "focus2": "Artificial Intelligence",
    "focus3": "Machine Learning",
    "focus4": "Data Engineering",

    "spec1": "Full Stack Development",
    "spec2": "Backend Engineering",
    "spec3": "ETL Pipelines",
    "spec4": "Automation",

    "current1": "Building scalable web applications",
    "current2": "Learning AI Engineering",

    "portfolio": "panduputra.vercel.app",
    "github": "github.com/Panduputran",
    "linkedin": "linkedin.com/in/panduputran",
}


def replace(root, element_id, value):
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        element.text = value


# ==========================
# Read ASCII
# ==========================

ascii_lines = Path("ascii-art.txt").read_text(
    encoding="utf-8"
).splitlines()

# ==========================
# Generate SVG
# ==========================

for svg_file in SVG_FILES:

    tree = etree.parse(svg_file)
    root = tree.getroot()

    ascii_node = root.find(".//*[@id='ascii']")

    if ascii_node is not None:

        ascii_node.clear()

        for i, line in enumerate(ascii_lines):

            tspan = etree.SubElement(
                ascii_node,
                "tspan"
            )

            tspan.set("x", "25")

            if i == 0:
                tspan.set("dy", "0")
            else:
                tspan.set("dy", "1.15em")

            tspan.text = escape(line)

    for key, value in PROFILE.items():
        replace(root, key, value)

    tree.write(
        svg_file,
        encoding="utf-8",
        xml_declaration=True
    )

print("Done.")