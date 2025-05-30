
# HSN Code Validator and Suggestion Agent (Google ADK + Python)

This project implements an intelligent agent using the **Google Agent Developer Kit (ADK)** to validate and suggest **HSN (Harmonized System Nomenclature) codes** based on user input. The agent handles both numeric HSN code validation and natural language descriptions for code suggestions.

## 🔧 Features

- Validate the format and existence of a given HSN code
- Suggest relevant HSN codes based on product or service descriptions
- Provide hierarchical parent HSN codes when available
- Full error handling for invalid inputs or malformed datasets
- Integrated with Google's ADK framework and Gemini model for conversational interaction

---

## 📁 Project Structure

```text
.
├── adk_hsn_agent.py           # Main ADK agent setup and runtime loop
├── hsn_code_validator.py      # HSN code validation logic
├── hsn_code_suggestor.py      # TF-IDF based suggestion engine
├── hsn_data_loader.py         # Excel loading and preprocessing
├── hsn_error_handler.py       # Centralized validation and error handling
├── HSN_SAC.xlsx               # Excel file with HSNCode and Description columns
```

---

## 📦 Requirements

- Python 3.8+
- Google ADK (installed via npm or pip depending on environment)
- Python dependencies:

```bash
pip install pandas scikit-learn openpyxl
```

---
## Demo Project Direct Link
```text
If you want to directly run the project you can go ahead and click the link below.
http://192.168.3.46:8501

```
## 🚀 How to Run

1. Ensure the following files are in the same directory:
   - `adk_hsn_agent.py`
   - `hsn_code_validator.py`
   - `hsn_code_suggestor.py`
   - `hsn_data_loader.py`
   - `hsn_error_handler.py`
   - `HSN_SAC.xlsx` (with columns: `HSNCode` and `Description`)

2. Run the ADK agent from the terminal:

```bash
python adk_hsn_agent.py
```

3. Follow the on-screen prompt:

```text
HSN Code Validator and Suggestion Agent
Type 'exit' to quit. Provide an HSN code (e.g., '01011010') or a product/service description (e.g., 'live horses').
```

---

## 💡 Example Usage

```text
Enter HSN code or description: 01011010
Agent Response: Valid HSN Code: 01011010 — purebred breeding animals. Parent Codes: ['01', '0101', '010110']

Enter HSN code or description: live horses
Agent Response:
Suggestions:
0101 — live horses, asses, mules and hinnies
01011010 — purebred breeding animals
...

Enter HSN code or description: exit
Exiting.
```

---

## ⚠️ Error Handling

- Invalid HSN code format
- Missing or malformed Excel data
- Too short or generic description inputs
- Logging to `hsn_agent.log` for debugging

---

## 📌 Notes

- This agent uses `gemini-1.5-flash-latest` via the ADK `LlmAgent`
- Ensure your Google API key is set correctly via `os.environ["GOOGLE_API_KEY"]`

---

## 📜 License

This project is intended for assessment, prototyping, and demonstration purposes.
