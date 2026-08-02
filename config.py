from lxml import etree

ASCII_FILE = "ascii-art.txt"

SVG_FILES = [
    "dark_mode.svg",
    "light_mode.svg"
]


# ===============================
# CONFIG
# ===============================

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
    "linkedin": "linkedin.com/in/panduputran"
}


# ===============================
# ASCII
# ===============================

with open(ASCII_FILE, encoding="utf-8") as f:
    ascii_art = f.read()


# ===============================
# XML Helper
# ===============================

def replace(root, element_id, value):

    element = root.find(f".//*[@id='{element_id}']")

    if element is not None:
        element.text = value


# ===============================
# MAIN
# ===============================

for svg in SVG_FILES:

    tree = etree.parse(svg)

    root = tree.getroot()

    replace(root, "ascii", ascii_art)

    for key, value in PROFILE.items():
        replace(root, key, value)

    tree.write(
        svg,
        encoding="utf-8",
        xml_declaration=True
    )

print("SVG generated successfully.")