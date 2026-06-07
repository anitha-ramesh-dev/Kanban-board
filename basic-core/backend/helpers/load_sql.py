def load_sql(filename):
    with open(f"sql/{filename}", "r") as file:
        return file.read()