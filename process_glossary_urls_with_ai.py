#!/usr/bin/env python3
"""
Script to process URLs from urls.yaml and generate enriched JSON objects using OpenAI API.
Uses the provided prompt to extract terms, aliases, and categories.
"""

import os
import time
import yaml
import json
import re
from urllib.parse import urlparse
from typing import List, Dict, Optional
import openai
from dotenv import load_dotenv
from openai import OpenAI

# Load .env if present
load_dotenv()

# Configure OpenAI API
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def extract_glossary_urls(urls_file: str = 'urls.yaml') -> List[str]:
    """
    Extract glossary URLs from the YAML file.
    
    Args:
        urls_file: Path to the YAML file containing URLs
        
    Returns:
        List of glossary URLs
    """
    with open(urls_file, 'r') as f:
        urls = yaml.safe_load(f)
    
    glossary_urls = []
    for url in urls:
        # Check if it's a glossary URL
        if '/learn/glossary/' in url and url.endswith('-definition'):
            glossary_urls.append(url)
    
    return glossary_urls

def process_url_with_ai(url: str, max_retries: int = 3) -> Optional[Dict]:
    """
    Process a single URL using the OpenAI prompt to generate enriched JSON.
    
    Args:
        url: The URL to process
        max_retries: Maximum number of retry attempts
        
    Returns:
        JSON object with term, url, aliases, and category, or None if failed
    """
    
    prompt = f"""You are an SEO and internal linking assistant. Given a URL pointing to an educational article or glossary entry- your job is to

extract the main glossary term and generate an enriched JSON object with:
- term: the human-readable glossary term
- url: the input URL
- aliases: a list of common synonyms or variations (singular/plural, informal, alternate phrasing). Will be used for anchor interlinks later. Include the initial term as well. 
- category: the financial topic this term belongs to 

Return only the JSON.

URL: {url}"""

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert SEO assistant specializing in financial glossary terms and internal linking."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content.strip()
            # Remove code block markers if present
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            # Try to parse JSON
            try:
                result = json.loads(content)
                
                # Validate required fields
                required_fields = ['term', 'url', 'aliases', 'category']
                if all(field in result for field in required_fields):
                    return result
                else:
                    print(f"❌ Missing required fields in response for {url}")
                    if attempt < max_retries - 1:
                        print(f"🔄 Retrying... (attempt {attempt + 2}/{max_retries})")
                        time.sleep(2)
                        continue
                    return None
                    
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON for {url}: {e}")
                print(f"Response: {content}")
                if attempt < max_retries - 1:
                    print(f"🔄 Retrying... (attempt {attempt + 2}/{max_retries})")
                    time.sleep(2)
                    continue
                return None
                
        except openai.RateLimitError as e:
            print(f"⏳ Rate limit hit for {url}. Waiting 60 seconds...")
            time.sleep(60)
            if attempt < max_retries - 1:
                print(f"🔄 Retrying after rate limit... (attempt {attempt + 2}/{max_retries})")
                continue
            return None
        except openai.APIError as e:
            print(f"❌ API error for {url}: {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in 5 seconds... (attempt {attempt + 2}/{max_retries})")
                time.sleep(5)
                continue
            return None
        except Exception as e:
            print(f"❌ Unexpected error for {url}: {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in 2 seconds... (attempt {attempt + 2}/{max_retries})")
                time.sleep(2)
                continue
            return None
    
    return None

def process_all_glossary_urls(urls_file: str = 'urls.yaml', output_file: str = 'glossary_terms.json', 
                             batch_size: int = 10, delay: float = 2.0):
    """
    Process all glossary URLs and generate enriched JSON objects.
    
    Args:
        urls_file: Path to the YAML file containing URLs
        output_file: Path to save the JSON output
        batch_size: Number of URLs to process before saving
        delay: Delay between API calls in seconds
    """
    
    # Check if OpenAI API key is set
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-key-here'")
        return []
    
    # Extract glossary URLs
    glossary_urls = extract_glossary_urls(urls_file)
    print(f"📋 Found {len(glossary_urls)} glossary URLs to process")
    
    if not glossary_urls:
        print("❌ No glossary URLs found in the file")
        return []
    
    # Load existing results if file exists
    existing_terms = []
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_terms = json.load(f)
            print(f"📁 Loaded {len(existing_terms)} existing terms from {output_file}")
        except:
            print("📁 Starting fresh - no existing terms loaded")
    
    # Create a set of already processed URLs
    processed_urls = {term['url'] for term in existing_terms}
    
    # Filter out already processed URLs
    urls_to_process = [url for url in glossary_urls if url not in processed_urls]
    print(f"🔄 Need to process {len(urls_to_process)} new URLs")
    
    if not urls_to_process:
        print("✅ All URLs already processed!")
        return existing_terms
    
    # Process URLs in batches
    all_terms = existing_terms.copy()
    successful = 0
    failed = 0
    
    start_time = time.time()
    
    for i, url in enumerate(urls_to_process, 1):
        print(f"\n🔄 Processing {i}/{len(urls_to_process)}: {url}")
        
        result = process_url_with_ai(url)
        
        if result:
            all_terms.append(result)
            successful += 1
            print(f"✅ Success: {result.get('term', 'Unknown term')}")
        else:
            failed += 1
            print(f"❌ Failed to process")
        
        # Calculate progress and estimated time
        elapsed_time = time.time() - start_time
        avg_time_per_url = elapsed_time / i
        remaining_urls = len(urls_to_process) - i
        estimated_remaining = remaining_urls * avg_time_per_url
        
        print(f"📊 Progress: {i}/{len(urls_to_process)} ({i/len(urls_to_process)*100:.1f}%)")
        print(f"⏱️ Estimated time remaining: {estimated_remaining/60:.1f} minutes")
        
        # Save batch periodically
        if i % batch_size == 0:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_terms, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved batch ({i}/{len(urls_to_process)})")
        
        # Delay between requests to respect rate limits
        if i < len(urls_to_process):
            print(f"⏳ Waiting {delay} seconds before next request...")
            time.sleep(delay)
    
    # Final save
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_terms, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Processing complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Total terms saved: {len(all_terms)}")
    print(f"📄 Saved to: {output_file}")
    
    # Show statistics
    categories = {}
    total_aliases = 0
    
    for term_obj in all_terms:
        category = term_obj.get('category', 'unknown')
        categories[category] = categories.get(category, 0) + 1
        total_aliases += len(term_obj.get('aliases', []))
    
    print(f"\n📊 Final Statistics:")
    print(f"Total terms: {len(all_terms)}")
    print(f"Total aliases: {total_aliases}")
    print(f"Categories: {len(categories)}")
    
    print(f"\n📊 Categories breakdown:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} terms")
    
    return all_terms

def validate_glossary_file(file_path: str = 'glossary_terms.json'):
    """
    Validate the generated glossary file.
    
    Args:
        file_path: Path to the glossary JSON file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            terms = json.load(f)
        
        print(f"\n🔍 Validating {file_path}...")
        
        required_fields = ['term', 'url', 'aliases', 'category']
        valid_terms = 0
        invalid_terms = 0
        
        for i, term_obj in enumerate(terms):
            if all(field in term_obj for field in required_fields):
                valid_terms += 1
            else:
                invalid_terms += 1
                print(f"❌ Term {i+1} missing required fields: {term_obj}")
        
        print(f"✅ Valid terms: {valid_terms}")
        print(f"❌ Invalid terms: {invalid_terms}")
        
        # Show some examples
        print(f"\n📝 Example entries:")
        for i, term_obj in enumerate(terms[:3]):
            print(f"\n{i+1}. {term_obj.get('term', 'Unknown')}")
            print(f"   Category: {term_obj.get('category', 'Unknown')}")
            print(f"   Aliases: {', '.join(term_obj.get('aliases', [])[:5])}...")
            print(f"   URL: {term_obj.get('url', 'Unknown')}")
        
    except FileNotFoundError:
        print(f"❌ File {file_path} not found")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {file_path}: {e}")

def main():
    """Main function to run the processing."""
    print("🚀 Starting glossary URL processing with AI...")
    
    # Check if API key is available
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-key-here'")
        return
    
    try:
        # Process all URLs
        terms = process_all_glossary_urls(
            urls_file='urls.yaml',
            output_file='glossary_terms.json',
            batch_size=3,  # Process 3 URLs at a time to be conservative
            delay=3.0      # 3 second delay between requests to respect rate limits
        )
        
        # Validate the output
        validate_glossary_file('glossary_terms.json')
        
    except KeyboardInterrupt:
        print("\n⏹️ Processing interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 