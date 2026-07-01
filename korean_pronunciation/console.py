"""Interactive Console Mode (REPL) for the Korean Pronunciation Engine."""

import sys
from korean_pronunciation import get_pronunciations


def run_console():
    # Ensure standard output supports UTF-8 for Korean characters
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        # Fallback if stdout doesn't support reconfigure (e.g. in some IDE run window wrappers)
        pass

    print("=====================================")
    print("Korean Pronunciation Converter")
    print("Type 'exit' to quit.")
    print("=====================================")
    print()

    while True:
        try:
            print("Input:")
            try:
                text = input("> ").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                print("Goodbye.")
                sys.exit(0)

            if text.lower() == "exit":
                print("Goodbye.")
                sys.exit(0)

            if not text:
                print("-------------------------------------")
                print()
                continue

            try:
                results = get_pronunciations(text)
                print()
                print("Pronunciations")
                print()
                if not results:
                    print("No valid pronunciations found.")
                else:
                    for i, pron in enumerate(results, 1):
                        rules_str = ", ".join(pron["applied_rules"])
                        if rules_str:
                            print(f"{i}. {pron['pronunciation']} (rules: {rules_str})")
                        else:
                            print(f"{i}. {pron['pronunciation']}")
            except Exception as e:
                print(f"Error processing text: {e}", file=sys.stderr)

            print()
            print("-------------------------------------")
            print()

        except KeyboardInterrupt:
            print()
            print("Goodbye.")
            sys.exit(0)


if __name__ == "__main__":
    run_console()
