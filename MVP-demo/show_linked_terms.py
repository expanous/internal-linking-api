#!/usr/bin/env python3

import yaml
from interlink_service import InterlinkService
import re

def load_urls():
    """Load URLs from the yaml file."""
    with open('../urls.yaml', 'r') as file:
        return yaml.safe_load(file)

def load_html_content():
    """Load the algo-trading HTML content."""
    with open('../Articles/algo-trading', 'r') as file:
        return file.read()

def extract_linked_terms(html_content):
    """Extract all linked terms from the HTML content."""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
    
    linked_terms = []
    for link in links:
        term = link.get_text().strip()
        url = link.get('href', '')
        linked_terms.append({
            'term': term,
            'url': url,
            'length': len(term),
            'word_count': len(term.split())
        })
    
    return linked_terms

def main():
    # Load data
    urls_data = load_urls()
    html_content = load_html_content()
    
    # Initialize service
    service = InterlinkService()
    
    # Process the HTML
    processed_html = service.process_html_with_glossary(html_content, urls_data)
    
    # Extract linked terms
    linked_terms = extract_linked_terms(processed_html)
    
    print("=== LINKED TERMS ANALYSIS ===\n")
    
    # Show all linked terms
    print("All linked terms:")
    for i, item in enumerate(linked_terms, 1):
        print(f"{i:2d}. '{item['term']}' -> {item['url']}")
        print(f"    Length: {item['length']} chars, Words: {item['word_count']}")
    
    print("\n" + "="*50)
    
    # Show short words (3 characters or less)
    short_words = [item for item in linked_terms if item['length'] <= 3]
    if short_words:
        print(f"\nSHORT WORDS LINKED ({len(short_words)} found):")
        for item in short_words:
            print(f"  '{item['term']}' -> {item['url']}")
    else:
        print("\nNo short words (3 chars or less) were linked.")
    
    # Show single-letter words
    single_letter = [item for item in linked_terms if len(item['term']) == 1]
    if single_letter:
        print(f"\nSINGLE LETTER WORDS LINKED ({len(single_letter)} found):")
        for item in single_letter:
            print(f"  '{item['term']}' -> {item['url']}")
    else:
        print("\nNo single-letter words were linked.")
    
    # Show common short words
    common_short_words = ['is', 'in', 'on', 'at', 'to', 'of', 'for', 'and', 'or', 'the', 'a', 'an']
    found_common = [item for item in linked_terms if item['term'].lower() in common_short_words]
    if found_common:
        print(f"\nCOMMON SHORT WORDS LINKED ({len(found_common)} found):")
        for item in found_common:
            print(f"  '{item['term']}' -> {item['url']}")
    else:
        print("\nNo common short words were linked.")
    
    # Statistics
    print(f"\nSTATISTICS:")
    print(f"Total links: {len(linked_terms)}")
    print(f"Average term length: {sum(item['length'] for item in linked_terms) / len(linked_terms):.1f} characters")
    print(f"Average word count: {sum(item['word_count'] for item in linked_terms) / len(linked_terms):.1f} words")
    
    # Show shortest and longest terms
    if linked_terms:
        shortest = min(linked_terms, key=lambda x: x['length'])
        longest = max(linked_terms, key=lambda x: x['length'])
        print(f"Shortest term: '{shortest['term']}' ({shortest['length']} chars)")
        print(f"Longest term: '{longest['term']}' ({longest['length']} chars)")

if __name__ == "__main__":
    main() 