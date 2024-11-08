# Diagnosable Code Duplication in Introductory Programming

This repository contains the baseline script and guide how to run the newly implemented detectors for the paper Diagnosable Code Duplication in Introductory Programming accepted for SIGCSE 2025.

All the code was run on Ubuntu 22.04 with Python 3.10.12.

## Baseline detector

The `baseline/duplication_scorer.py` script takes a name of the output file to store the results to and then at least one folder containing `.py` files, which it walks to compute similarity score for each of the files. The script creates a `.csv` file that contains two columns: filepath, which identifies the file relative to the folder passed as an argument, and score, which expresses how many identical/similar lines are there inside the file (the script does **not** compute duplication spread across different files). The higher the score, the more duplication is there in the file. For the purpose of the baseline detector described in the paper, we considered any file with the score at least 4 to contain duplication.

Calling `python3 baseline/duplication_scorer.py out data/` creates a file `out.csv` in the current folder, with a line for each Python file in the `data` folder. The line will contain the path to the file relative to `data` and the duplication score the file has.

## New detectors

The source code for the detectors can be found in the `new` folder. The `analyses` subfolder contains code responsible for the antiunification = building the intermediate representation for the duplicate code. The `duplication` subfolder contains code for the detectors. However, the detectors have been implemented as a part of the open-source linter [EduLint](https://github.com/GiraffeReversed/edulint). They depend on plenty of features and analyses performed by EduLint, so the best way of running the detectors is through the linter.

The detectors used in the paper correspond to those in EduLint's version 4.1.3. You can install the linter using `pip` as described in [the linter's documentation](https://edulint.readthedocs.io/en/v4.1.3/running.html#installation). Then run the detectors using the following command:

```
python3 -m edulint check -o config-file=empty -o pylint=--enable=similar-block-to-loop-range,similar-block-to-loop-collection,similar-block-to-loop-merge,similar-block-to-function,similar-block-to-call,similar-if-into-block,similar-if-to-extracted,similar-if-to-expr,similar-if-to-untwisted,similar-if-to-use,identical-if-branches,identical-if-branches-part,identical-seq-ifs <files-or-dirs-to-check>
```

<details>
   <summary>How to simplify the command</summary>
To simplify the command, you can also create a TOML file with the following contents:

```
[pylint]
enable=[
    "similar-block-to-loop-range",
    "similar-block-to-loop-collection",
    "similar-block-to-loop-merge",
    "similar-block-to-function",
    "similar-block-to-call",
    "similar-if-into-block",
    "similar-if-to-extracted",
    "similar-if-to-expr",
    "similar-if-to-untwisted",
    "similar-if-to-use",
    "identical-if-branches",
    "identical-if-branches-part",
    "identical-seq-ifs"
]
```
Then instead call the following command:

```
python3 -m edulint check -o config-file=<path-to-the-TOML-file> <files-or-dirs-to-check>
```
</details>

The detectors are still under active development. To get the most up-to-date version of the detectors, which may have improved recall or have some bugs fixed, use the latest EduLint version. The latest version may also support more detectors. For that, see the [current documentation](https://edulint.readthedocs.io/en/latest/checkers.html#custom-checkers) (section No duplicate code).

### Detector mapping

Since the tool is under development and has been for some time before we started working on the paper, the detector names differ from those used in the paper (we did not change them afterwards for backwards compatibility reasons). They map to the duplication types described in the paper as follows:

```
duplicate sequence: similar-block-to-loop-range,similar-block-to-loop-collection  # detectors differ in whether they advice to iterate over a range or a collection
duplicate loop body: similar-block-to-loop-merge
duplicate blocks: similar-block-to-function
missing call: similar-block-to-call
movable if: similar-if-into-block
extractable if: similar-if-to-extracted,similar-if-to-expr  # detector differ in whether they advice to extract the if and assign to variables, or to use the if expression
twisted ifs: similar-if-to-untwisted
directly usable condition: similar-if-to-use
identical if branches: identical-if-branches
extractable branch part: identical-if-branches-part
mergeable sequential ifs: identical-seq-ifs
```
