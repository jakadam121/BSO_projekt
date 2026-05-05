import subprocess
import os
from datetime import datetime

def run_scan(cfg):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(cfg["results_dir"], f"scan_{timestamp}.xml")

    cmd = ["nmap"]
    cmd.extend(cfg["scan_flags"].split())

    if cfg["nse_scripts"] and "--script" not in cfg["scan_flags"]:
        cmd.extend(["--script", cfg["nse_scripts"]])

    if cfg["nmap_extra"]:
        cmd.extend(cfg["nmap_extra"].split())

    cmd.extend(["-oX", output_file])
    cmd.append(cfg["subnet"])

    print(f"Uruchamiam: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR Nmap: {result.stderr}")
        return None

    print(f"Skan zakonczony, wyniki w: {output_file}")
    return output_file