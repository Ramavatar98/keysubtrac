import subprocess

def run_keysubtracter(pubkey, outputfile, b_value):
    subprocess.run(["./keysubtracter", "-p", pubkey, "-n", "70", "-x", "-b", str(b_value)], stdout=open(outputfile, "w"))

def run_keymath(pubkey, op, val):
    result = subprocess.check_output(["./keymath", pubkey, op, str(val)])
    return result.decode().strip()

def compare_files(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        set1 = set(f1.read().splitlines())
        set2 = set(f2.read().splitlines())
    return set1 & set2

def main():
    pubkey = "03d04b3f0f5c305ff4d13ecd74db285a96bd773af7de8766b4438a2a51a324de8c"
    checked = set()
    minus_count = 0
    round_num = 0

    while True:
        round_num += 1
        print(f"\n[Round {round_num}] Using PubKey: {pubkey}")

        # Step 1: keysubtracter with -b 12
        run_keysubtracter(pubkey, "result1.txt", b_value=12)

        # Step 2: keymath /2
        half_pubkey = run_keymath(pubkey, "/", 2)

        # Step 3: keysubtracter on half_pubkey with -b 11
        run_keysubtracter(half_pubkey, "result2.txt", b_value=11)

        # Step 4: Compare both result files
        match = compare_files("result1.txt", "result2.txt")
        if match:
            print(f"[✓] Match Found after {minus_count} x '-1' operations!")
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

if __name__ == "__main__":
    main()
