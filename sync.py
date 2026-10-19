"""Add an importer shipment manifest to the green coffee inventory."""
import csv
import json
import sys
from pathlib import Path

INVENTORY = Path("inventory.csv")
REORDER_KG = 60


def load():
    if not INVENTORY.exists():
        return {}
    with INVENTORY.open() as f:
        return {row["origin"]: float(row["kg"]) for row in csv.DictReader(f)}


def save(stock):
    with INVENTORY.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["origin", "kg"])
        writer.writerows(sorted(stock.items()))


def main(manifest_path):
    manifest = json.loads(Path(manifest_path).read_text())
    stock = load()
    for line in manifest["lines"]:
        stock[line["origin"]] = stock.get(line["origin"], 0) + line["bags"] * line["kg_per_bag"]
    save(stock)
    print(f"Synced shipment from {manifest['supplier']} ({manifest['contact']})")
    for origin, kg in stock.items():
        if kg < REORDER_KG:
            print(f"  LOW: {origin} at {kg:.0f} kg")


if __name__ == "__main__":
    main(sys.argv[1])
