from difflib import SequenceMatcher
import os
import tqdm
import argparse


def check_match(line1, line2, threshold=0.85):
    if line1 == line2:
        return 1
    s = SequenceMatcher(None, line1, line2)
    if s.ratio() > threshold:
        return 0.5
    return 0


def compute_duplication_score(code):
    lines = code.split("\n")
    lines = list(map(lambda s: s.replace(" ", ""), lines))
    lines = list(filter(lambda s: len(s), lines))
    score = 0
    max_duplicate_line = -1
    for i in range(len(lines) - 1):
        if i < max_duplicate_line:
            continue
        for j in range(i + 1, len(lines)):
            local_score = 0
            count = 0
            current_score = check_match(lines[i], lines[j])
            while (
                i + count + 1 < j and j + count + 1 < len(lines) and current_score > 0
            ):
                local_score += current_score
                count += 1
                current_score = check_match(lines[i + count], lines[j + count])
            if local_score > 0.5:
                score += local_score
                max_duplicate_line = i + count
                break
    return score


def main():
    parser = argparse.ArgumentParser(
        description="computes baseline duplication score for passed files"
    )
    parser.add_argument("output_filename")
    parser.add_argument("input_dirs", nargs="+")

    args = parser.parse_args()

    with open(f"{args.output_filename}.csv", mode="w") as out_f:
        out_f.write("filepath,score\n")
        for dir in tqdm.tqdm(args.input_dirs):
            for dirpath, dirnames, filenames in tqdm.tqdm(os.walk(dir), leave=False):
                for filename in filenames:
                    if not filename.lower().endswith(".py"):
                        continue
                    full_path = os.path.join(dirpath, filename)
                    with open(full_path, encoding="utf8") as in_f:
                        score = compute_duplication_score(in_f.read())
                    out_f.write(f"{full_path},{score}\n")


if __name__ == "__main__":
    main()
