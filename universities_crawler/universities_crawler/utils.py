def clean_content(content: list[str]):
    cleaned_content = [text.strip().replace(' ', ' ').replace('​', ' ').lower() for text in
                       content]  # Remove leading/trailing whitespace and non-breaking spaces
    return ' '.join(cleaned_content)
