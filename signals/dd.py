import typing as t
import time
import subprocess
import os
from sqlmesh import signal, DatetimeRanges, ExecutionContext

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@signal()
def clientdetails_loaded(
    batch: DatetimeRanges,
    context: ExecutionContext,
) -> t.Union[bool, DatetimeRanges]:

    result = context.engine_adapter.fetchdf("""
        SELECT COUNT(*) AS cnt
        FROM PORTFOLIO_DB2.PUBLIC.CLIENTDETAILS1 s
        LEFT JOIN PORTFOLIO_DB2.PUBLIC.STG_CLIENTDETAILS t
        ON s.CLIENTID = t.CLIENT_ID
        WHERE t.CLIENT_ID IS NULL
    """)
    col = result.columns[0]
    row_count = int(result[col].iloc[0])

    if row_count == 0:
        print("❌ No new data found — skipping", flush=True)
        return False
    else:
        print(f"✅ {row_count} new rows found — executing model...", flush=True)
        return True


if __name__ == "__main__":
    print("🟢 Auto runner started. Press Ctrl+C to stop.", flush=True)
    run_count = 0

    while True:
        run_count += 1
        print(f"\n─── Run #{run_count} ───────────────────────────", flush=True)

        try:
            subprocess.run(
                ["sqlmesh", "run"],
                cwd=PROJECT_DIR
            )
        except KeyboardInterrupt:
            print("🛑 Stopped by user.", flush=True)
            break
        except Exception as e:
            print(f"❌ FAILED: {e}", flush=True)

        print("⏰ Next run in 5 minutes... (Ctrl+C to stop)", flush=True)
        try:
            time.sleep(240)
        except KeyboardInterrupt:
            print("🛑 Stopped by user.", flush=True)
            break