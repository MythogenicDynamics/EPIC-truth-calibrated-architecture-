# examples/run_epic.py
from src.epic_core import EpicCore

if __name__ == "__main__":
    epic = EpicCore()
    query = "What is the current president of the United States?"
    response = epic.process_query(query)
    print("EPIC Response:", response)
