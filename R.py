import subprocess
import threading
import time

public_key = "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16"
random_n = ''.join([str(i) for i in __import__('random').choices(range(10), k=40)])

command = [
    "./keysubtracter",
    "-p", public_key,
    "-n", random_n,
    "-b", "135",
    "-R",
    "-f", "address"
]

print(f"▶️ Command run with -n: {random_n}")

# Shared buffer to hold output temporarily
buffer = []

def reader(proc):
    for line in proc.stdout:
        decoded = line.decode()
        buffer.append(decoded)

# Start the process
proc = subprocess.Popen(command, stdout=subprocess.PIPE)

# Start thread to read output
t = threading.Thread(target=reader, args=(proc,))
t.start()

# Wait for first minute, save to 1.txt
time.sleep(60)
with open("1.txt", "w") as f1:
    f1.writelines(buffer)

print("✅ First minute done → 1.txt saved.")

# Wait another minute (second minute)
time.sleep(60)
with open("2.txt", "w") as f2:
    f2.writelines(buffer[len(buffer)//2:])  # Approximate split

print("✅ Second minute done → 2.txt saved.")

# End the process if still running
proc.terminate()
