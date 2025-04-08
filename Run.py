import os
import json
import subprocess

# State file to track -n value
STATE_FILE = "n_state.json"

# Get current -n value or default to 10
def get_n_value():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            return state.get("n", 100000)
    return 100000

# Save updated -n value
def save_n_value(n):
    with open(STATE_FILE, "w") as f:
        json.dump({"n": n}, f)

def run_keysubtracter(pubkey, n, b_value, outputfile):
    subprocess.run(["./keysubtracter", "-p", pubkey, "-n", str(n), "-x", "-b", str(b_value)], stdout=open(outputfile, "w"))

def run_keymath(pubkey, op, val):
    result = subprocess.check_output(["./keymath", pubkey, op, str(val)])
    return result.decode().strip()

def compare_files(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        set1 = set(f1.read().splitlines())
        set2 = set(f2.read().splitlines())
    return set1 & set2

def main():
    pubkey = "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16"
    checked = set()
    minus_count = 0
    round_num = 0
    n = get_n_value()

    while True:
        round_num += 1
        print(f"\n[Round {round_num}] Using PubKey: {pubkey} with -n {n}")

        # Step 1: keysubtracter with -b 12
        run_keysubtracter(pubkey, n, b_value=135, outputfile="result1.txt")

        # Step 2: keymath /2
        half_pubkey = run_keymath(pubkey, "/", 2)

        # Step 3: keysubtracter on half_pubkey with -b 11
        run_keysubtracter(half_pubkey, n, b_value=134, outputfile="result2.txt")

        # Step 4: Compare both result files
        match = compare_files("result1.txt", "result2.txt")
        if match:
            print(f"[\u2713] Match Found after {minus_count} x '-1' operations!")
            with open("match_found.txt", "w") as matchfile:
                matchfile.write(f"Match found after {minus_count} x '-1'\n")
                matchfile.write(f"Main pubkey used: {pubkey}\n")
                matchfile.write(f"Half pubkey used: {half_pubkey}\n")
                matchfile.write("Matched lines:\n")
                matchfile.write("\n".join(match))
            break

        # Step 5: keymath -1 for next round
        new_pubkey = run_keymath(pubkey, "-", 1)

        if new_pubkey in checked:
            print("[x] Already tried this pubkey. Ending loop.")
            break

        checked.add(pubkey)
        pubkey = new_pubkey
        minus_count += 1

    # Save updated -n value only if job restarted
    if os.getenv("GITHUB_RUN_ID"):
        save_n_value(n + 10)

if __name__ == "__main__":
    main()
      
