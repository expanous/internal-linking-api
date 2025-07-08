#!/usr/bin/env python3
"""
Script to save detailed matching results with context for the "what is investor" article to a file.
"""

from internal_linking import InternalLinker

def main():
    # Initialize the linker
    linker = InternalLinker()
    
    # Get detailed matches for the "what is investor" article
    detailed_matches = linker.get_detailed_matches('Articles/what is investor')
    
    # Save to file
    output_file = 'investor_matches_with_context.txt'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== DETAILED MATCHES WITH CONTEXT FOR 'WHAT IS INVESTOR' ===\n\n")
        f.write(f"Total detailed matches found: {len(detailed_matches)}\n\n")
        
        for i, match in enumerate(detailed_matches, 1):
            f.write(f"Match {i}:\n")
            f.write(f"- matched_phrase: {match['matched_phrase']}\n")
            f.write(f"- context: {match['context']}\n")
            f.write(f"- target_page: {match['target_page']}\n")
            f.write("\n")
    
    print(f"Results saved to: {output_file}")
    print(f"Total matches saved: {len(detailed_matches)}")

if __name__ == "__main__":
    main() 