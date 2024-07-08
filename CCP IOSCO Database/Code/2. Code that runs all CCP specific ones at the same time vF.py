import subprocess
import os


scripts = [
    r"C:\{Your Path}\CCP IOSCO Database\Code\Compiling Code for each CCP\BME Compiling Code vF.py",
    r"C:\{Your Path}\CCP IOSCO Database\Code\Compiling Code for each CCP\CBOE_Compiling_Code vF.py",
    r"C:\{Your Path}\CCP IOSCO Database\Code\Compiling Code for each CCP\CCPA Compiling Code vF.py",
    r"C:\{Your Path}\CCP IOSCO Database\Code\Compiling Code for each CCP\Eurex AG Compiling Code vF.py",
    r"C:\{Your Path}\CCP IOSCO Database\Code\Compiling Code for each CCP\Euronext Compiling Code vF.py",
    r"C:\{Your Path}\CCP IOSCO Database\Code\Compiling Code for each CCP\European Commodity Clearing Compiling Code vF.py",
    r"C:\{Your Path}\CCP IOSCO Database\Code\Compiling Code for each CCP\ICE Clear Compiling Code vF.py",
    r"C:\{Your Path}\CCP IOSCO Database\Code\Compiling Code for each CCP\KDPW Compiling Code vF.py",
    r"C:\{Your Path}\CCP IOSCO Database\Code\Compiling Code for each CCP\LCH Compiling Code vF.py",
    r"C:\{Your Path}\CCP IOSCO Database\Code\Compiling Code for each CCP\OMI Clearing Compiling Code vF.py",
    r"C:\{Your Path}\CCP IOSCO Database\Code\Compiling Code for each CCP\SKDD Compiling Code vF.py"
    
    
]


def run_script(script_name):
    try:
        result = subprocess.run(["python", script_name], check=True, capture_output=True, text=True)
        print(f"Script {script_name} executed successfully.")
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script {script_name}: {e}")
        print("Output:", e.output)


def main():
    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()