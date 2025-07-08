#!/usr/bin/env python3
"""
Script to show detailed matching results with context for the "what is investor" article.
"""

from internal_linking import InternalLinker

def main():
    # Initialize the linker
    linker = InternalLinker()
    
    # Get detailed matches for the "what is investor" article
    print("=== DETAILED MATCHES WITH CONTEXT FOR 'WHAT IS INVESTOR' ===\n")
    
    detailed_matches = linker.get_detailed_matches('Articles/what is investor')
    
    print(f"Total detailed matches found: {len(detailed_matches)}\n")
    
    for i, match in enumerate(detailed_matches, 1):
        print(f"Match {i}:")
        print(f"- matched_phrase: {match['matched_phrase']}")
        print(f"- context: {match['context']}")
        print(f"- target_page: {match['target_page']}")
        print()

if __name__ == "__main__":
    main() 