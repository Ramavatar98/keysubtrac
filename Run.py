import subprocess

def run_keysubtracter(pubkey, outputfile, b_value, n_value):
    subprocess.run(["./keysubtracter", "-p", pubkey, "-n", str(n_value), "-x", "-b", str(b_value)],
                   stdout=open(outputfile, "w"))

def run_keymath(pubkey, op, val):
    result = subprocess.check_output(["./keymath", pubkey, op, str(val)])
    return result.decode().strip()

def compare_files(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        set1 = set(f1.read().splitlines())
        set2 = set(f2.read().splitlines())
    return set1 & set2

def compare_three(file1, file2, file3):
    with open(file1) as f1, open(file2) as f2, open(file3) as f3:
        set1 = set(f1.read().splitlines())
        set2 = set(f2.read().splitlines())
        set3 = set(f3.read().splitlines())
    return (set1 & set2) | (set1 & set3) | (set2 & set3)

def main():
    original_pubkey = "03d02b29ecbaaab809da4e34a6740aaa4b2d1242d928c23a8e1782a8d3db47b117"
    pubkey = original_pubkey
    checked = set()
    minus_count = 0
    round_num = 0
    n_value = 9005020

    while True:
        round_num += 1
        print(f"\n[Round {round_num}] Using PubKey: {pubkey} | -n: {n_value}")

        run_keysubtracter(pubkey, "result1.txt", b_value=135, n_value=n_value)

        half_pubkey = run_keymath(pubkey, "/", 2)
        run_keysubtracter(half_pubkey, "result2.txt", b_value=134, n_value=n_value)

        quarter_pubkey = run_keymath(half_pubkey, "/", 2)
        run_keysubtracter(quarter_pubkey, "result3.txt", b_value=133, n_value=n_value)

        match = compare_three("result1.txt", "result2.txt", "result3.txt")
        if match:
            print(f"[✓] Match Found after {minus_count} x '-1' operations!")
            with open("match_found.txt", "w") as matchfile:
                matchfile.write(f"Match found after {minus_count} x '-1'\n")
                matchfile.write(f"Main pubkey used: {pubkey}\n")
                matchfile.write(f"Half pubkey used: {half_pubkey}\n")
                matchfile.write(f"Quarter pubkey used: {quarter_pubkey}\n")
                matchfile.write("Matched lines:\n")
                matchfile.write("\n".join(match))
            break

        new_pubkey = run_keymath(pubkey, "-", 1)
        if new_pubkey in checked:
            print("[x] Already tried this pubkey. Ending loop.")
            break

        checked.add(pubkey)
        pubkey = new_pubkey
        minus_count += 1

        if minus_count >= 5000:
            print(f"[i] 500 rounds done. Increasing -n by 10 and restarting from original pubkey.")
            n_value += 10

            # Save updated -n value
            with open("np.txt", "a") as np_file:
                np_file.write(f"{n_value}\n")

            pubkey = original_pubkey
            minus_count = 0
            checked.clear()

if __name__ == "__main__":
    main()

      
