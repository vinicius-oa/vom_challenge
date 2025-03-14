See [instructions.md](instructions.md), then later add your docs to this file.

# Decision Policy API

* ## How to run it:
  * ### Prerequisites:
    * Python version: **3.9.x - 3.13.x**
    
  * ### Steps:
    * ```sh
      # In your OS's terminal e.g. cmd
      cd backend
      ```
    * ```sh
      python -m venv .venv
      ```
    * ```sh
      # MacOS/Linux
      source .venv/bin/activate
      
      # Windows
      .venv\Scripts\activate
      ```
    * ```sh
      pip install -r requirements-dev.lock
      ```
    * ```sh
      # Run it
      
      ## MacOs/Linux
      python src/main.py
      
      ## Windows
      python src\main.py
      
      
      
      # Run tests
      pytest
      ```