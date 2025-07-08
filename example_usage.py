#!/usr/bin/env python3
"""
Example usage of the InternalLinker class.
This script demonstrates how to use the internal linking functionality.
"""

from internal_linking import InternalLinker

def main():
    # Initialize the linker
    linker = InternalLinker()
    
    # Example 1: Get unique matches for a specific article
    print("=== Example 1: Unique matches for policy-mix article ===")
    unique_matches = linker.get_unique_matches('Articles/policy-mix')
    print(f"Found {len(unique_matches)} unique matches:")
    
    for term, url in unique_matches:
        print(f"  - '{term}' -> {url}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 2: Process all articles and show summary
    print("=== Example 2: Summary of all articles ===")
    results = linker.process_all_articles()
    
    for article_name, result in results.items():
        print(f"{article_name}: {result['total_matches']} matches")
    
    print("\n" + "="*60 + "\n")
    
    # Example 3: Create HTML version with links
    print("=== Example 3: Create HTML version with links ===")
    html_content = linker.create_html_links('Articles/policy-mix', 'policy-mix-with-links.html')
    print("HTML content created and saved to 'policy-mix-with-links.html'")
    print("First 500 characters of HTML:")
    print(html_content[:500] + "...")
    
    print("\n" + "="*60 + "\n")
    
    # Example 4: Get matches for algo-trading article
    print("=== Example 4: Matches for algo-trading article ===")
    algo_matches = linker.get_unique_matches('Articles/algo-trading')
    print(f"Found {len(algo_matches)} unique matches:")
    
    for term, url in algo_matches:
        print(f"  - '{term}' -> {url}")

if __name__ == "__main__":
    main() 