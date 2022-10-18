def get_huggingface_token():
    with open("huggingface.token", "r") as f:
        lines = f.readlines()
        print(f"Token retrieved: {lines[0]}")
        return lines[0]