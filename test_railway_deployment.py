#!/usr/bin/env python3
"""
Test script for Railway deployment
"""

import requests
import json
import sys

def test_railway_deployment(base_url):
    """Test the Railway deployment"""
    
    print(f"Testing Railway deployment at: {base_url}")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=30)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=30)
        if response.status_code == 200:
            root_data = response.json()
            print(f"✅ Root endpoint working: {root_data.get('message', 'Unknown')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: Statistics
    print("\n3. Testing statistics endpoint...")
    try:
        response = requests.get(f"{base_url}/stats", timeout=30)
        if response.status_code == 200:
            stats_data = response.json()
            print(f"✅ Statistics loaded: {stats_data.get('total_terms', 0)} terms")
        else:
            print(f"❌ Statistics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Statistics error: {e}")
    
    # Test 4: Process article
    print("\n4. Testing article processing...")
    test_content = """
    <p>This is a test article about ETFs and mutual funds. 
    We will discuss various investment strategies and portfolio management techniques.</p>
    """
    
    try:
        response = requests.post(
            f"{base_url}/process",
            json={
                "content": test_content,
                "max_links": 3
            },
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Article processing successful:")
            print(f"   - Total links: {result.get('total_links', 0)}")
            print(f"   - New links added: {result.get('new_links_added', 0)}")
        else:
            print(f"❌ Article processing failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Article processing error: {e}")
    
    # Test 5: Categories
    print("\n5. Testing categories endpoint...")
    try:
        response = requests.get(f"{base_url}/categories", timeout=30)
        if response.status_code == 200:
            categories_data = response.json()
            print(f"✅ Categories loaded: {categories_data.get('count', 0)} categories")
        else:
            print(f"❌ Categories failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Categories error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Railway deployment test completed!")
    print(f"📖 API Documentation: {base_url}/docs")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_railway_deployment.py <railway-url>")
        print("Example: python test_railway_deployment.py https://your-app.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    success = test_railway_deployment(base_url)
    
    if not success:
        sys.exit(1) 