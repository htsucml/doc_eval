"""Confidence bucket summaries."""

from __future__ import annotations

from typing import Iterable


def calibration_buckets(confidences: Iterable[float | None], correctness: Iterable[float], bins: int = 5) -> list[dict]:
    valid = [
        (float(conf), float(correct))
        for conf, correct in zip(confidences, correctness)
        if conf is not None
    ]
    if not valid:
        return []

    bucketed = []
    for bucket_index in range(bins):
        low = bucket_index / bins
        high = (bucket_index + 1) / bins
        if bucket_index == bins - 1:
            members = [(c, a) for c, a in valid if low <= c <= high]
        else:
            members = [(c, a) for c, a in valid if low <= c < high]
        if not members:
            continue
        avg_conf = sum(c for c, _ in members) / len(members)
        avg_acc = sum(a for _, a in members) / len(members)
        bucketed.append(
            {
                "bucket": f"{low:.1f}-{high:.1f}",
                "count": len(members),
                "avg_confidence": round(avg_conf, 4),
                "avg_accuracy": round(avg_acc, 4),
                "gap": round(abs(avg_conf - avg_acc), 4),
            }
        )
    return bucketed

