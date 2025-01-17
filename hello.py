import anthropic
import prompts
import sys
import argparse

client = anthropic.Anthropic()


def explain_code(code: str):
    print(f"explaining:\n{code}")


def optimize_code(code: str):
    print(f"optimizing:\n{code}")


def read_files(files: list) -> str:
    code = ""
    for file in files:
        with open(file) as f:
            code += f"{f.read()}\n"

    return code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        choices=["explain", "optimize", "e", "o"],
        help="The action to perform for the code: 'explain' (or 'e'), 'optimize' (or 'o')",
    )
    parser.add_argument(
        "files", metavar="file", nargs="+", help="One or more files to process"
    )
    args = parser.parse_args()

    if args.action in ["e", "explain"]:
        code = read_files(args.files)
        explain_code(code)

    elif args.action in ["o", "optimize"]:
        code = read_files(args.files)
        optimize_code(code)


if __name__ == "__main__":
    main()
