import random
import subprocess

# Fixed public key
public_key = "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16"

# Generate random 40-digit number
random_n = ''.join([str(random.randint(0, 9)) for _ in range(40)])

# Prepare the command
command = [
    "timeout", "60",  # सिर्फ 60 सेकंड के लिए चले
    "./keysubtracter",
    "-p", public_key,
    "-n", random_n,
    "-b", "136",
    "-d",
    "-x",             # Hex mode enable करें
    "-f", "address"   # address नाम की फ़ाइल से एड्रेस लें
]

print(f"▶️ Running command (1 min) with -n: {random_n}")

# Run the command and save output to 1.txt
with open("1.txt", "w") as outfile:
    subprocess.run(command, stdout=outfile)

print("⏱️ 1 minute over or command finished. Output saved to 1.txt")
