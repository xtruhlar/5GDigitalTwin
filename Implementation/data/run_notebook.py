import time
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

notebook_path = "./main.ipynb"  # Update with the correct path

while True:
    print("🔄 Running main.ipynb...")

    try:
        # Load the notebook
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # Execute the notebook
        ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        ep.preprocess(notebook)

        # Save the executed notebook
        with open(notebook_path, "w", encoding="utf-8") as f:
            nbformat.write(notebook, f)

        print("✅ Notebook executed successfully!")

    except Exception as e:
        print(f"❌ Error running notebook: {e}")

    # Wait 1 second before running again
    time.sleep(1.5)
