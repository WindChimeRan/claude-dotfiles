"""Poll `metalstat` one-shot every second and emit compact JSONL to stdout.

Background
----------
`metalstat -a -i 1 --json` works as a streaming monitor but buffers its
JSON output under redirection, which makes it useless as a sidecar
logger (nothing lands in the file until the stream is flushed).  This
script sidesteps that by invoking `metalstat` in *one-shot* mode once
per second and emitting one compact JSON object per line, with an
`elapsed_s` field added so downstream analyzers can align the timeline
without needing wall clock parsing.

Usage
-----
    python metalstat_logger.py > /tmp/metalstat.jsonl 2> /tmp/metalstat.err &
    # ... run your workload ...
    pkill -f metalstat_logger

Each JSONL line is the full metalstat JSON schema plus:
    "elapsed_s": float  # seconds since this script started

The script exits cleanly on SIGINT/SIGTERM and logs any metalstat
failure as a separate JSON line with only an "error" key, which
analyzers should filter out.
"""
import json
import subprocess
import sys
import time


def main() -> None:
    t0 = time.time()
    while True:
        try:
            started = time.time()
            result = subprocess.run(
                [
                    "metalstat",
                    "-a",
                    "--json",
                    "--no-color",
                    "--no-header",
                ],
                capture_output=True,
                text=True,
                timeout=3,
            )
            if result.returncode != 0:
                time.sleep(0.5)
                continue
            data = json.loads(result.stdout)
            data["elapsed_s"] = round(started - t0, 3)
            print(json.dumps(data, separators=(",", ":")), flush=True)
            remaining = 1.0 - (time.time() - started)
            if remaining > 0:
                time.sleep(remaining)
        except KeyboardInterrupt:
            return
        except Exception as exc:
            print(json.dumps({"error": str(exc)}), flush=True)
            time.sleep(0.5)


if __name__ == "__main__":
    main()
