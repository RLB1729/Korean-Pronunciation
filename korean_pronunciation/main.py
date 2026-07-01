"""CLI interface for the Korean Pronunciation Engine."""

import sys
import json
import argparse
from korean_pronunciation import get_pronunciations


def main():
    parser = argparse.ArgumentParser(
        description="Convert Korean text into all valid standard pronunciations."
    )
    parser.add_argument(
        "text",
        type=str,
        help="Korean word or sentence to convert."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output the results in JSON format."
    )
    
    args = parser.parse_args()
    
    try:
        results = get_pronunciations(args.text)
    except Exception as e:
        print(f"Error processing text: {e}", file=sys.stderr)
        sys.exit(1)
        
    if args.json:
        # Force UTF-8 encoding output for JSON representation
        sys.stdout.reconfigure(encoding="utf-8")
        print(json.dumps(results, ensure_ascii=False, indent=4))
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        for pron in results:
            rules_str = ", ".join(pron["applied_rules"])
            if rules_str:
                print(f"{pron['pronunciation']} (rules: {rules_str})")
            else:
                print(pron["pronunciation"])


if __name__ == "__main__":
    main()
