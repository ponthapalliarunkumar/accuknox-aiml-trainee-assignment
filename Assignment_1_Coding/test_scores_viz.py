"""Problem 2: get student scores from an API, find the average, draw a bar chart."""
import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Assumption: the API returns JSON like [{"name": "Asha", "score": 78}, ...]
API_URL = "https://example.com/api/scores"  # replace with your real/mock endpoint

SAMPLE = [  # used only when the API cannot be reached
    {"name": "Asha", "score": 78}, {"name": "Ravi", "score": 85},
    {"name": "Meena", "score": 62}, {"name": "Kiran", "score": 91},
    {"name": "Sara", "score": 70}, {"name": "John", "score": "absent"},
]


def get_scores():
    try:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError):
        print("API not reachable, using sample data instead.")
        return SAMPLE


def clean(records):
    names, scores, skipped = [], [], 0
    for rec in records:
        try:
            score = float(rec["score"])
        except (KeyError, TypeError, ValueError):
            skipped += 1
            continue
        names.append(rec.get("name", "?"))
        scores.append(score)
    return names, scores, skipped


if __name__ == "__main__":
    names, scores, skipped = clean(get_scores())
    if not scores:
        raise SystemExit("No valid scores found.")
    average = sum(scores) / len(scores)
    print(f"Students: {len(scores)}  Skipped: {skipped}  Average: {average:.2f}")

    plt.figure(figsize=(8, 5))
    plt.bar(names, scores, color="steelblue")
    plt.axhline(average, color="red", linestyle="--", label=f"Average {average:.1f}")
    plt.xlabel("Student"); plt.ylabel("Score"); plt.title("Student Test Scores")
    plt.legend(); plt.tight_layout()
    plt.savefig("scores_chart.png")
    print("Chart saved as scores_chart.png")