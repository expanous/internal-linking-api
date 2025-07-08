#!/usr/bin/env python3
"""
Test script to process a few URLs with AI to verify the functionality.
"""

import yaml
import json
import os
from dotenv import load_dotenv
from process_glossary_urls_with_ai import process_url_with_ai, extract_glossary_urls

# Load .env if present
load_dotenv()

def test_single_url():
    """Test processing a single URL."""
    test_url = "https://capital.com/en-int/learn/glossary/absolute-return-funds-definition"
    
    print(f"🧪 Testing single URL: {test_url}")
    
    result = process_url_with_ai(test_url)
    
    if result:
        print("✅ Success!")
        print(json.dumps(result, indent=2))
    else:
        print("❌ Failed to process URL")

def test_few_urls():
    """Test processing a few URLs."""
    # Get first 2 glossary URLs to be conservative with API usage
    glossary_urls = extract_glossary_urls('urls.yaml')[:2]
    
    print(f"🧪 Testing {len(glossary_urls)} URLs...")
    
    results = []
    for i, url in enumerate(glossary_urls, 1):
        print(f"\n🔄 Processing {i}/{len(glossary_urls)}: {url}")
        
        result = process_url_with_ai(url)
        
        if result:
            results.append(result)
            print(f"✅ Success: {result.get('term', 'Unknown')}")
        else:
            print("❌ Failed")
    
    # Save test results
    if results:
        with open('test_glossary_terms.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved {len(results)} test results to test_glossary_terms.json")
        
        # Show summary
        print("\n📊 Test Results Summary:")
        for result in results:
            print(f"  - {result.get('term', 'Unknown')} ({result.get('category', 'Unknown')})")
            print(f"    Aliases: {', '.join(result.get('aliases', [])[:3])}...")

def main():
    """Main test function."""
    print("🧪 Starting AI processing tests...")
    
    # Check if API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-key-here'")
        return
    
    try:
        # Test single URL first
        test_single_url()
        
        print("\n" + "="*50 + "\n")
        
        # Test a few URLs
        test_few_urls()
        
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main() 