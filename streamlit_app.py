"""Streamlit Cloud entrypoint for the verified competition application bundle."""
import hashlib
from pathlib import Path
import runpy
import tempfile
import zipfile

archive = Path(__file__).with_name("mindsync_app.zip")
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
bundle = Path(tempfile.gettempdir()) / ("mindsync-hosted-" + digest)
ready = bundle / ".bundle-ready"
if not ready.exists():
    bundle.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as contents:
        for member in contents.namelist():
            path = Path(member)
            if path.is_absolute() or ".." in path.parts:
                raise RuntimeError("Invalid application bundle path")
        contents.extractall(bundle)
    ready.write_text(digest)
runpy.run_path(str(bundle / "deployment/streamlit_app.py"), run_name="__main__")
