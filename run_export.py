import subprocess, json, tempfile
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--template", required=True)
parser.add_argument("--output", required=True)

args = parser.parse_args()

config = {
    "sla": args.template,
    "output": args.output
}

base_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(base_dir, "scribus_inner.py")

config = {
    "sla": os.path.join(base_dir, "template.sla"),
    "output": os.path.join(base_dir, "output.pdf")
}

with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    json.dump(config, f)
    config_path = f.name

cmd = f'"C:\\Program Files\\Scribus 1.6.5\\Scribus.exe" --python-script "{script_path}" "{config_path}"'

print("Running command:")
print(cmd)

subprocess.run(cmd, shell=True, check=True)