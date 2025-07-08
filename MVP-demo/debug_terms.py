#!/usr/bin/env python3
"""
Debug script to see what terms are being extracted from URLs.
"""

from interlink_service import InterlinkService

def main():
    service = InterlinkService()
    
    target_entries = [
        {"url": "https://capital.com/en-int/learn/glossary/portfolio-definition"},
        {"url": "https://capital.com/en-int/learn/glossary/index-funds-definition"},
        {"url": "https://capital.com/en-int/learn/market-guides/what-is-share-trading"},
        {"url": "https://capital.com/en-int/learn/market-guides/trade-etfs"},
        {"url": "https://capital.com/en-int/learn/market-guides/what-is-commodity-trading"},
        {"url": "https://capital.com/en-int/learn/market-guides/algo-trading"}
    ]
    
    print("Terms extracted from URLs:")
    print("=" * 50)
    
    for entry in target_entries:
        url = entry['url']
        terms = service.extract_terms_from_url(url)
        print(f"\nURL: {url}")
        print(f"Terms: {terms}")
    
    print("\n" + "=" * 50)
    print("Testing phrase matching:")
    
    # Test the specific case of "index funds"
    test_text = "index funds and mutual funds"
    doc = service.nlp(test_text)
    
    # Create a simple test with "index funds" as a target
    target_terms = ["index funds", "funds"]
    prepared_phrases = service._prepare_target_phrases(target_terms)
    
    print(f"\nTest text: '{test_text}'")
    print(f"Target terms: {target_terms}")
    print(f"Prepared phrases: {prepared_phrases}")
    
    matches = service._find_phrase_matches(doc, prepared_phrases, set())
    print(f"Matches found: {matches}")

if __name__ == "__main__":
    main() 