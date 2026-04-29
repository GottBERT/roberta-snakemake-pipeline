#!/usr/bin/env python3

import re
from datetime import datetime, timedelta
from pathlib import Path

# alles über diesem Gap wird als "Pause/Queue-Wait" ignoriert
GAP_THRESHOLD_MINUTES = 300

names = {
    "32k": "/path/to/logs/train_32k.log",
    "52k": "/path/to/logs/train_52k.log",
    "96k": "/path/to/logs/train_96k.log"
}

# Nur train_inner Zeilen nehmen (aktive Trainingsschritte)
TS_PATTERN = re.compile(
    r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\|\sINFO\s\|\strain_inner\s\|'
)

def parse_timestamps(logfile):
    ts = []
    with open(logfile, "r") as f:
        for line in f:
            m = TS_PATTERN.match(line)
            if m:
                ts.append(
                    datetime.strptime(
                        m.group(1),
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
    return ts


def compute_active_time(timestamps, gap_minutes=30):
    if len(timestamps) < 2:
        return timedelta(0), []

    threshold = timedelta(minutes=gap_minutes)
    active = timedelta(0)
    segments = []

    seg_start = timestamps[0]
    seg_end = timestamps[0]

    for prev, curr in zip(timestamps[:-1], timestamps[1:]):
        delta = curr - prev

        if delta <= threshold:
            active += delta
            seg_end = curr
        else:
            # Segment abschließen, Gap ignorieren
            segments.append((seg_start, seg_end))
            seg_start = curr
            seg_end = curr

    segments.append((seg_start, seg_end))

    return active, segments


def fmt(td):
    seconds = int(td.total_seconds())
    hours = seconds / 3600
    days = hours / 24
    return seconds, hours, days


def main():
    print(f"Gap threshold: {GAP_THRESHOLD_MINUTES} min\n")

    for model, logfile in names.items():
        ts = parse_timestamps(logfile)

        active, segments = compute_active_time(
            ts,
            gap_minutes=GAP_THRESHOLD_MINUTES
        )

        sec, hrs, days = fmt(active)

        print(f"=== {model} ===")
        print(f"Active training time: {hrs:.2f} h ({days:.2f} d)")
        print(f"Segments found: {len(segments)}")

        for i, (s,e) in enumerate(segments,1):
            dur = e-s
            print(
                f"  Run {i:02d}: {s} -> {e} "
                f" ({dur.total_seconds()/3600:.2f} h)"
            )
        print()

if __name__ == "__main__":
    main()