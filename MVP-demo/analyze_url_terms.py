#!/usr/bin/env python3

import yaml
import re
from urllib.parse import urlparse

def extract_terms_from_url(url):
    """Extract potential terms from a URL path, including multi-word phrases and key single words."""
    # Common English stop words to exclude
    stop_words = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 
        'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with',
        'or', 'but', 'not', 'what', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'only',
        'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now'
    }
    
    # Important financial acronyms and short terms to whitelist
    financial_acronyms = {
        'etf', 'ipo', 'cfd', 'mt4', 'mt5', 'api', 'otc', 'dax', 'gtd', 'pip', 'net',
        'gdp', 'g20', 'g10', 'bbb', 'ccc', 'sec', 'roe', 'npl', 'peg', 'imf', 'bep',
        'ism', 'emv', 'xpo', 'amm', 'dma', 'ddu', 'grs', 'irs', 'vix', 'dow', 'vif',
        'xva', 'etp', 'fis', 'tsx', 'cac', 'sse', 'jse', 'lbs', 'omx', 'del', 'cum',
        'mix', 'put', 'buy', 'out', 'low', 'mid', 'tax', 'for', 'all', 'off', 'tri',
        'non', 'per', 'bar', 'kse', 'pse', 'ups', 'a50', '100', '225', '200', '500',
        'web', 'app', 'key', 'top', 'are', 'usd', 'eur', 'aud', 'jpy', 'cad', 'gbp',
        'chf', 'nzd', 'amd', 'tui', 'arm', 'sui', 'neo', 'inu', 'lot', 'oil', 'nio',
        'fee', 'how', 'our', 'why', 'day', 'sar', 'esg', 'ppp', 'web3', 'croci',
        'comex', 'opec', 'node', 'vwap', 'ebitda', 'ebid', 'moneyness', 'paydown',
        'layering', 'delta', 'staking', 'sampling', 'stagflation', 'sell', 'year',
        'cost', 'risk', 'time', 'fund', 'bond', 'swap', 'call', 'put', 'buy', 'sell'
    }
    
    parsed = urlparse(url)
    path = parsed.path.lower()
    terms = set()
    segments = path.split('/')
    for segment in segments:
        if segment and segment not in ['en-int', 'learn', 'glossary', 'market-guides']:
            # Remove common suffixes
            clean_segment = re.sub(r'-(definition|guide|trading|funds?|market|what|is|the|of|a|an)$', '', segment)
            # Add full phrase (hyphens/underscores to spaces)
            if '-' in clean_segment or '_' in clean_segment:
                phrase = clean_segment.replace('-', ' ').replace('_', ' ')
                if 2 <= len(phrase.split()) <= 4:
                    terms.add(phrase)
            # Add all 1-4 word n-grams from the segment
            words = re.split(r'[-_]', clean_segment)
            for n in range(1, min(5, len(words)+1)):
                for i in range(len(words)-n+1):
                    ngram = ' '.join(words[i:i+n])
                    if len(ngram) > 2:
                        # Filter out stop words unless they're financial acronyms
                        if len(ngram) <= 3:
                            # For short terms (3 chars or less), only include if they're financial acronyms
                            if ngram.lower() in financial_acronyms:
                                terms.add(ngram)
                        else:
                            # For longer terms, exclude if they're stop words
                            if ngram.lower() not in stop_words:
                                terms.add(ngram)
    return list(terms)

def main():
    # Load URLs
    with open('../urls.yaml', 'r') as file:
        urls_data = yaml.safe_load(file)
    
    print("=== URL TERM EXTRACTION ANALYSIS ===\n")
    
    all_terms = []
    short_terms = []
    
    for url in urls_data:
        terms = extract_terms_from_url(url)
        
        print(f"URL: {url}")
        print(f"Extracted terms: {terms}")
        
        for term in terms:
            all_terms.append({
                'term': term,
                'url': url,
                'length': len(term),
                'word_count': len(term.split())
            })
            
            # Check for short terms
            if len(term) <= 3:
                short_terms.append({
                    'term': term,
                    'url': url,
                    'length': len(term)
                })
        
        print("-" * 80)
    
    print(f"\n=== SUMMARY ===")
    print(f"Total unique terms extracted: {len(set(item['term'] for item in all_terms))}")
    
    # Show short terms
    if short_terms:
        print(f"\nSHORT TERMS (3 chars or less) that would be linked:")
        unique_short = {}
        for item in short_terms:
            if item['term'] not in unique_short:
                unique_short[item['term']] = item['url']
        
        for term, url in unique_short.items():
            print(f"  '{term}' -> {url}")
    else:
        print("\nNo short terms (3 chars or less) would be linked.")
    
    # Show common short words that might be extracted
    common_short_words = ['is', 'in', 'on', 'at', 'to', 'of', 'for', 'and', 'or', 'the', 'a', 'an']
    found_common = [item for item in all_terms if item['term'].lower() in common_short_words]
    
    if found_common:
        print(f"\nCOMMON SHORT WORDS that would be linked:")
        unique_common = {}
        for item in found_common:
            if item['term'] not in unique_common:
                unique_common[item['term']] = item['url']
        
        for term, url in unique_common.items():
            print(f"  '{term}' -> {url}")
    else:
        print("\nNo common short words would be linked.")
    
    # Show statistics
    if all_terms:
        lengths = [item['length'] for item in all_terms]
        word_counts = [item['word_count'] for item in all_terms]
        
        print(f"\nSTATISTICS:")
        print(f"Average term length: {sum(lengths) / len(lengths):.1f} characters")
        print(f"Average word count: {sum(word_counts) / len(word_counts):.1f} words")
        print(f"Shortest term: {min(lengths)} characters")
        print(f"Longest term: {max(lengths)} characters")

if __name__ == "__main__":
    main() 