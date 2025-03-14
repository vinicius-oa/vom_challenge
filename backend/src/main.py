""" WebApp Entrypoint """
from pathlib import Path

import uvicorn

if __name__ == "__main__":
    backend_dir = Path(__file__).parent
    log_file_path = str(
        backend_dir.joinpath(
            "/".join((str(backend_dir), "config/log_conf.yaml"))
        )
    )

    uvicorn.run(
        "config.factory:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_config=log_file_path
    )
