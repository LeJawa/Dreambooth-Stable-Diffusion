def get_huggingface_token():
    with open("huggingface.token", "r") as f:
        lines = f.readlines()
        return lines[0]