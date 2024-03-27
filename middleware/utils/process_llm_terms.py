import re

def process_llm_terms(case_response: str) -> str:
    "Process the response of the terms processed by the llm"

    # Remove content within parentheses including the parentheses themselves
    case_response = re.sub(r'\s*\([^)]*\)', '', case_response)

    # Remove 'etc.' from the end if it exists
    case_response = case_response.rstrip(".")
    if case_response.endswith("etc"):
        case_response = case_response[:-3].rstrip(", ")

    # Remove numbers followed by parenthesis or directly followed by spaces
    cleaned_string = re.sub(r'\d+\)\s*|\d+\s+', '', case_response)

    # Remove punctuation (except for commas and hyphens as they might be part of medical terms)
    cleaned_string = re.sub(r'[^\w\s,-]', '', cleaned_string)

    # Split the string into individual terms based on commas
    terms = cleaned_string.split(',')

    # Strip whitespace and remove empty entries
    terms = [term.strip() for term in terms if term.strip() != ""]

    # Remove 'etc' if it's present, considering case insensitivity
    terms = [term for term in terms if term.lower() != "etc"]

    # Remove duplicates by converting the list to a set, then back to a list
    unique_terms = list(set(terms))

    # Join the unique terms back into a string
    return " ".join(unique_terms)