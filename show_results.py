#!/usr/bin/env python3
"""
Script to show unique matching results from all articles.
"""

from internal_linking import InternalLinker

def main():
    linker = InternalLinker()
    
    print("=== UNIQUE MATCHES FROM ALL ARTICLES ===\n")
    
    articles = ['algo-trading', 'policy-mix', 'absolute-return-funds-definition']
    all_terms = set()
    article_results = {}
    
    for article_name in articles:
        matches = linker.get_unique_matches(f'Articles/{article_name}')
        article_results[article_name] = matches
        
        print(f"📄 {article_name}")
        print(f"Total unique matches: {len(matches)}")
        print("Matches:")
        for term, url in matches:
            print(f"  • \"{term}\" -> {url}")
            all_terms.add(term)
        print()
    
    # Summary
    print("=== SUMMARY ===")
    print(f"Total unique terms across all articles: {len(all_terms)}")
    
    # Find most common terms
    term_counts = {}
    for term in all_terms:
        count = sum(1 for article in articles 
                   if any(t == term for t, u in article_results[article]))
        term_counts[term] = count
    
    most_common = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print("\nMost common terms across articles:")
    for term, count in most_common:
        print(f"  • \"{term}\" appears in {count} article(s)")
    
    print(f"\nArticles processed: {len(articles)}")
    print(f"Total glossary terms available: {len(linker.glossary_terms)}")

if __name__ == "__main__":
    main() 