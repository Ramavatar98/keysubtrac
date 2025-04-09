import subprocess

def run_keysubtracter(pubkey, outputfile, b_value):
    subprocess.run(["./keysubtracter", "-p", pubkey, "-n", "1500", "-x", "-b", str(b_value)], stdout=open(outputfile, "w"))

def run_keymath(pubkey, op, val):
    result = subprocess.check_output(["./keymath", pubkey, op, str(val)])
    return result.decode().strip()

def compare_multiple(*files):
    sets = []
    for file in files:
        with open(file) as f:
            sets.append(set(f.read().splitlines()))
    
    # Check for matches in any 2 or all 3 sets
    common_matches = (sets[0] & sets[1]) | (sets[1] & sets[2]) | (sets[0] & sets[2])
    return common_matches

def main():
    pubkey = "03d02b29ecbaaab809da4e34a6740aaa4b2d1242d928c23a8e1782a8d3db47b117"
    checked = set()
    minus_count = 0
    round_num = 0

    while True:
        round_num += 1
        print(f"\n[Round {round_num}] PubKey: {pubkey}")

        # Step 1: First subtracter run with -b 12
        run_keysubtracter(pubkey, "result1.txt", b_value=135)

        # Step 2: pubkey / 2
        half1 = run_keymath(pubkey, "/", 2)

        # Step 3: Second subtracter run with -b 11
        run_keysubtracter(half1, "result2.txt", b_value=134)

        # Step 4: half1 / 2
        half2 = run_keymath(half1, "/", 2)

        # Step 5: Third subtracter run with -b 10
        run_keysubtracter(half2, "result3.txt", b_value=133)

        # Step 6: Compare all 3 result files
        match = compare_multiple("result1.txt", "result2.txt", "result3.txt")
        if match:
            print(f"[✓] Match Found after {minus_count} x '-1' operations!")
            with open("match_found.txt", "w") as matchfile:
                matchfile.write(f"Match found after {minus_count} x '-1'\n")
                matchfile.write(f"Main pubkey: {pubkey}\n")
                matchfile.write(f"Half1: {half1}\nHalf2: {half2}\n")
                matchfile.write("Matched lines:\n")
                matchfile.write("\n".join(match))
            break

        # Step 7: Try next pubkey -1
        new_pubkey = run_keymath(pubkey, "-", 1)

        if new_pubkey in checked:
            print("[x] Already tried. Ending loop.")
            break

        checked.add(pubkey)
        pubkey = new_pubkey
        minus_count += 1

if __name__ == "__main__":
    main()

      
