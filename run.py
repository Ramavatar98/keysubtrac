import subprocess
import sys
import re

# Define the command
command = ["./keysubtracter", "-p", "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16", "-n", "87112285931760246646623899502532662132736", "-b", "136", "-R"]

# Load target public keys from pub.txt
def load_targets(filename="pub.txt"):
    try:
        with open(filename, "r") as file:
            return set(re.escape(line.strip()) for line in file if line.strip())  # Escape for regex safety
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return set()

# Load targets
targets = load_targets()

# Create a regex pattern to match targets inside any text
target_pattern = re.compile("|".join(targets)) if targets else None

# Run the command
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)

print("🚀 Command is running... Searching for target public key...\n")

try:
    with open("found_keys.txt", "a") as f:
        for line in iter(process.stdout.readline, ""):
            line = line.strip()
            if line:
                print(f"🔍 Checking: {line}")

            # Check if any target exists in the line
            if target_pattern and target_pattern.search(line):                                                                                                         print(f"\n🎯 TARGET FOUND: {line} 🎯\n")
                f.write(line + "\n")  # Save the target key
                f.flush()  # Ensure data is written immediately
                process.terminate()  # Stop the command
                print("✅ Command stopped!")
                sys.exit(0)

except KeyboardInterrupt:
    print("\n❌ Script stopped by user.")

finally:
    process.kill()  # Ensure process is terminated
