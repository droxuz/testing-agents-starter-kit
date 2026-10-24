"""Harness for black-box and white-box unit test generation agents."""

import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(REPO_ROOT / ".env")
os.environ.setdefault("MSWEA_SILENT_STARTUP", "1")

# Hard total timeout wrapper to prevent hanging on zombie HTTP keep-alive streams
try:
    import requests
    from concurrent.futures import ThreadPoolExecutor, TimeoutError

    _orig_post = requests.post
    _post_pool = ThreadPoolExecutor(max_workers=32)

    def _hard_timeout_post(url, *args, **kwargs):
        fut = _post_pool.submit(_orig_post, url, *args, **kwargs)
        try:
            return fut.result(timeout=240.0)
        except TimeoutError:
            raise requests.exceptions.Timeout(f"Hard total request timeout (240s) exceeded for {url}")

    requests.post = _hard_timeout_post
except Exception:
    pass
