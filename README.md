See [instructions.md](instructions.md), then later add your docs to this file.

# Decision Policy API
* ## Docs
  * [README.md](backend%2FREADME.md)
* ## How to run it
  * ### Prerequisites
    * Python version: **3.9.x - 3.13.x**
    
  * ### Steps
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
    
  * ### Docs
    * http://localhost:8001/docs
    * [Decision Policy API.postman_collection.json](backend%2Fsrc%2Fdomain%2Fcommon%2Fcontrollers%2Fdocs%2FDecision%20Policy%20API.postman_collection.json)