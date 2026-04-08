# uv: The Best Python Manager

uv is a modern Python package and project manager written in Rust, much faster and simpler than alternatives like `pip` and `virtualenv`. It will automatically install Python into your virtual environment, and will manage your dependencies and virtual environments for you.

## Install `uv`:

- **macOS, Linux, and WSL:**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

- **Windows:**

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

## Project Management
Most often, you'll be working in a project that you want to save and use across different systems. In these cases it's usually best to initialize a project and manage dependencies using a `pyproject.toml` file.

- **Initialize a project:**

    ```bash
    uv init --bare
    ```

    *This creates a `pyproject.toml` and `uv.lock` to manage your project and dependencies.*

    *`--bare` omits the creation of a `README.md`, `main.py`, and Git repository, which may be helpful for your future projects, but is not necessary for this workshop.*


- **Add dependencies:**

    ```bash
    uv add <package-name>
    ```
    
    *Automatically creates a virtual environment (in `.venv`), resolves dependency conflicts, updates your `pyproject.toml` and `uv.lock` files, and installs the package(s).*

- **Remove dependencies:**

    ```bash
    uv remove <package-name>
    ```

    *Removes the package from your environment and `pyproject.toml`/`uv.lock` files, keeping your project clean.*

- **Run a script:**

    ```bash
    uv run <script-name>.py
    ```

    *Executes your Python script automatically within the `.venv` context. You never need to run `source .venv/bin/activate` again (though you still can if you want)! You can also use `uv run` to run other installed CLI tools like `uv run pytest`.*

- **View Dependency Tree:**
    ```bash
    uv tree
    ```
    *Prints a visual tree of all your installed packages and their sub-dependencies, making it easy to see exactly what libraries were pulled in and why.*

- **Sync with `pyproject.toml`:**

    ```bash
    uv sync
    ```

    *If you download or clone a Python project with a `pyproject.toml` file, run `uv sync` to sync your local environment with the declared dependencies and versions.*

## One-Off Scripts and Tools
Often you will want a single Python script without the clutter of a full project and `.venv` directory. We can use `uv` to run scripts with temporary dependencies or embed dependency metadata directly in the script itself!

- **Run a script with temporary dependencies:**

    ```bash
    uv run --with <package-name> <script-name>.py
    ```

    *Creates an ephemeral environment, installs the specified package(s), runs the script, and cleans up!*

- **Inline Script Metadata (PEP 723):**
    You can embed dependencies directly inside your Python file! Run this command to add dependency metadata to the top of your script:

    ```bash
    uv add --script <script-name>.py <package-name>
    ```

    *This modifies the script to include a special comment block declaring its dependencies. Now, anyone with `uv` can simply run:*

    ```bash
    uv run <script-name>
    ```

    *`uv` will automatically read the inline requirements and execute the script in an isolated environment.*

- **Run a tool without installing it:**

    ```bash
    uvx <package-name> [args...]
    ```

    *`uvx` is a special command that allows you to run any executable from a package without installing it globally, similar to `npx` in the Node.js ecosystem. For example:*

## The Classic Workflow
If you prefer the old way of doing things, `uv` can also be used as a drop-in replacement for `pip` and `virtualenv` with blazing fast performance and better dependency resolution.

- **Create a virtual environment:**

    ```bash
    uv venv
    ```

    *Creates a `.venv` folder with an isolated Python environment.*

- **Install packages:**

    ```bash
    uv pip install <package-name>
    ```

    *Installs the package into the active environment, but way faster than `pip`.*

- **Activate the environment:**

    ```bash
    # Linux/macOS/WSL
    source .venv/bin/activate
    ```

    ```powershell
    # Windows
    .\.venv\Scripts\Activate.ps1
    ```

    *Activates the virtual environment in your current shell session, just like `virtualenv`. If you want to use `python` commands rather than `uv run`, you can activate the environment.*

- **Run a script:**

    ```bash
    uv run <script-name>.py
    ```

    *Runs the script using the Python interpreter from the active environment. The environment does not need to be activated first.*

## Managing Python Versions
If the scripts or packages you are using require specific Python versions, `uv` will download them for you automatically and transparently.

- **Run a script with a specific version:**
    ```bash
    uv run --python <python-version> <script-name>.py
    ```
    *Runs the script using the specified Python version. If the version is not on your system, `uv` downloads it automatically without polluting your PATH. For example:*

    ```bash
    uv run --python 3.10 exploit.py
    ```

    *Runs `exploit.py` using Python 3.10.*


- **Pin a version for your project:**
    ```bash
    uv python pin <python-version>
    ```
    *Creates a `.python-version` file that specifies the Python version for the project. Any `uv run` commands in this directory will now automatically use the pinned Python version.*

> [!NOTE]
> If you have already installed packages, you may need to edit the `requires-python` field of your `pyproject.toml` to specify the new version and run `uv sync` to update the environment.

## Converting Old Pip Projects
If you have an older project with a `requirements.txt` file, converting it to `uv` is incredibly easy. `uv` also offers a fully compatible, drop-in replacement interface for standard `pip`.

- **Add dependencies from an old `requirements.txt`:**

    ```bash
    uv add -r requirements.txt
    ```

    *Installs all requirements into the active environment.*

## Clean Up

- **Clean the Cache to free up space:**

    ```bash
    uv cache clean
    ```

    *Because `uv` caches downloads and wheels globally to make environment creation instant, it can take up lots of space over time. Run this periodically to free it up!*
