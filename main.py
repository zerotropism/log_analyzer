import argparse
import json

from log_loader import load_data, stream_entries
from report import generate_report, generate_report_from_entries


def parse_args():
    parser = argparse.ArgumentParser(description="Analyse de sécurité des logs")
    parser.add_argument("--input", required=True, help="Chemin vers le fichier de logs")
    parser.add_argument(
        "--output", default=None, help="Fichier JSON de sortie (stdout par défaut)"
    )
    parser.add_argument(
        "--large-file", action="store_true", help="Mode streaming pour fichiers > 32 GB"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.large_file:
        report = generate_report_from_entries(stream_entries(args.input))
    else:
        df, malformed = load_data(args.input)
        report = generate_report(df, malformed_count=len(malformed))

    output = json.dumps(report, indent=2, default=str)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
