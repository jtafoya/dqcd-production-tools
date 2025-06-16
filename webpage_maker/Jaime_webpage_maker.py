from json2html import json2html
import glob
import json

status = {"samples": []}
for filename in glob.glob("*.json"): 
    with open(filename) as f:
        d = json.load(f)
    assert len(d) <= 1
    if len(d) == 0:
        continue
    results = {"step": filename.split("_")[0], "name": list(d.keys())[0]}
    results.update(list(d.values())[0])
    
    if results["done"] == 0 and results["dataset files"] == 1:
        # assuming the "1" in dataset files comes from the output of wc -l giving an error, as the dataset doesn't exist
        results["dataset files"] = 0

    elif results["done"] < results["dataset files"]:
        results["done"] =  '[LEFT]font color=[QUOTE]red[QUOTE][RIGHT] ' + str(results["done"]) + '[LEFT]/font[RIGHT]'
        results["dataset files"] =  '[LEFT]font color=[QUOTE]red[QUOTE][RIGHT] ' + str(results["dataset files"]) + '[LEFT]/font[RIGHT]'

    if not "resubmitted" in results:
        results["resubmitted"] = False
    status["samples"].append(results)

html = json2html.convert(status).replace("[LEFT]", "<").replace("[RIGHT]", ">").replace("[QUOTE]", '"')
html = f"""
<!DOCTYPE html>
<html>
<body>
{html}    
</body>
</html>
"""

with open("index.html", "w+") as f:
    f.write(html)
