import subprocess
import time
import re

command = ["./keysubtracter", "-p", "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16", "-n", "87112285931760246646623899502532662132736", "-b", "136", "-R"]

def load_targets(filename="pub.txt"):
    try:
        with open(filename, "r") as file:
            return set(re.escape(line.strip()) for line in file if line.strip())
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return set()

targets = load_targets()
target_pattern = re.compile("|".join(targets)) if targets else None

process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)

print("🚀 Command is running... Searching for target public key...\n")

try:
    while True:
        line = process.stdout.readline().strip()
        if line:
            print(f"🔍 Checking: {line}")

        # टारगेट चेक करें
        if target_pattern and target_pattern.search(line):
            print(f"\n🎯 TARGET FOUND: {line} 🎯\n")
            with open("found_keys.txt", "a") as f:
                f.write(line + "\n")  # Save the target key
                f.flush()  # Ensure data is written immediately
            process.terminate()
            print("✅ Command stopped!")
            break

except KeyboardInterrupt:
    print("\n❌ Script stopped by user.")

finally:
    process.kill()
    
