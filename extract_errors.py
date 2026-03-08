import os

def extract_last_traceback(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    tracebacks = []
    current_traceback = []
    in_traceback = False

    for line in lines:
        if "Traceback (" in line or "Internal Server Error:" in line:
            in_traceback = True
            current_traceback = [line]
        elif in_traceback:
            if line.startswith("[") or "HTTP/1.1" in line: # typical log prefix
                in_traceback = False
                tracebacks.append("".join(current_traceback))
                current_traceback = []
            else:
                current_traceback.append(line)
        
        # also capture simple Exception lines
        if "Exception:" in line or "Error:" in line:
            if not in_traceback:
                 current_traceback = [line]
                 tracebacks.append("".join(current_traceback))

    if current_traceback:
        tracebacks.append("".join(current_traceback))
        
    print("--- LAST 3 TRACEBACKS ---")
    for tb in tracebacks[-3:]:
        print(tb)
        print("-" * 40)

if __name__ == '__main__':
    extract_last_traceback('error.log')
