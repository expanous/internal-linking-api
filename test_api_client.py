#!/usr/bin/env python3
"""
Test client for the Enhanced Internal Linking API
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("🏥 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_statistics():
    """Test statistics endpoint"""
    print("📊 Testing statistics...")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"Total terms: {stats['total_terms']}")
        print(f"Total aliases: {stats['total_aliases']}")
        print(f"Categories: {len(stats['categories'])}")
    print()

def test_categories():
    """Test categories endpoint"""
    print("📂 Testing categories...")
    response = requests.get(f"{BASE_URL}/categories")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total categories: {data['count']}")
        print("Top 5 categories:")
        for i, category in enumerate(data['categories'][:5]):
            print(f"  {i+1}. {category}")
    print()

def test_process_article():
    """Test article processing endpoint"""
    print("📝 Testing article processing...")
    
    # Sample article content
    article_content = """
    <p>Revenue is a key financial metric that companies use to measure their performance. 
    ETFs are popular investment vehicles that provide diversification. 
    Investors often look at both revenue and profit when analyzing stocks.</p>
    
    <h2>Key Points</h2>
    <ul>
        <li>Revenue represents total sales</li>
        <li>ETFs offer diversification benefits</li>
        <li>Investors should consider multiple metrics</li>
    </ul>
    """
    
    payload = {
        "content": article_content,
        "max_links": 5,
        "current_url": "https://capital.com//en-int/learn/glossary/revenue-definition"
    }
    
    response = requests.post(f"{BASE_URL}/process", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total links: {result['total_links']}")
        print(f"Existing links: {result['existing_links']}")
        print(f"New links added: {result['new_links_added']}")
        print(f"Max links: {result['max_links']}")
        print("HTML preview (first 200 chars):")
        print(result['html_content'][:200] + "...")
    else:
        print(f"Error: {response.text}")
    print()

def test_analyze_article():
    """Test article analysis endpoint"""
    print("🔍 Testing article analysis...")
    
    article_content = """
    <p>Revenue and ETFs are important concepts in finance. 
    Investors use various strategies to maximize returns.</p>
    """
    
    payload = {
        "content": article_content,
        "current_url": "https://capital.com//en-int/learn/glossary/revenue-definition"
    }
    
    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total matches: {result['total_matches']}")
        print(f"Unique terms: {result['unique_terms']}")
        print("Matches by category:")
        for category, matches in result['matches_by_category'].items():
            print(f"  {category}: {len(matches)} matches")
    else:
        print(f"Error: {response.text}")
    print()

def main():
    """Run all tests"""
    print("🚀 Enhanced Internal Linking API Test Client")
    print("=" * 50)
    
    try:
        test_health()
        test_statistics()
        test_categories()
        test_process_article()
        test_analyze_article()
        
        print("✅ All tests completed!")
        print(f"\n📖 API Documentation available at: {BASE_URL}/docs")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running:")
        print("   python3 api_internal_linking.py")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main() 