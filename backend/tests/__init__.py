import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
src_path = backend_dir.joinpath("/".join((str(backend_dir), "src")))
sys.path.append(str(src_path))
