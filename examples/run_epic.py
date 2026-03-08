from src.epic_core import EpicCore

if __name__ == "__main__":
    epic = EpicCore()
    query = "What is the capital of France?"
    response = epic.process_query(query)
    print("EPIC Response:", response)
