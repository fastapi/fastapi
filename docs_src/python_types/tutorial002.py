def get_full_name(first_name: str, last_name: str):
    return f"{first_name.title()} {last_name.title()}"


print(get_full_name("john", "doe"))
