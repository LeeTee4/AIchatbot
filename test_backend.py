#!/usr/bin/env python3
"""
Simple test script to verify Django backend connectivity
Run this to test if your backend is working before using the frontend
"""

import requests
import json
import sys

# Backend URL
BASE_URL = "http://localhost:8000"

def test_backend():
    print("🔧 Testing Lee Electronics AI Chatbot Backend...")
    print(f"Backend URL: {BASE_URL}")
    print("-" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/chat/", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print()
    
    # Test 2: Test endpoint
    print("2. Testing test endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/test/", timeout=5)
        if response.status_code == 200:
            print("✅ Test endpoint passed")
            data = response.json()
            print(f"   Message: {data.get('message')}")
            print(f"   Gemini configured: {data.get('gemini_configured')}")
        else:
            print(f"❌ Test endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Test endpoint error: {e}")
    
    print()
    
    # Test 3: Chat functionality
    print("3. Testing chat functionality...")
    try:
        test_message = {"question": "test"}
        response = requests.post(
            f"{BASE_URL}/api/chat/", 
            json=test_message,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Chat test passed")
            data = response.json()
            print(f"   Response: {data.get('answer')}")
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Chat test error: {e}")
    
    print()
    
    # Test 4: Real chat message
    print("4. Testing real chat message...")
    try:
        real_message = {"question": "What products do you offer?"}
        response = requests.post(
            f"{BASE_URL}/api/chat/", 
            json=real_message,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        if response.status_code == 200:
            print("✅ Real chat test passed")
            data = response.json()
            answer = data.get('answer', '')
            print(f"   Response: {answer[:100]}{'...' if len(answer) > 100 else ''}")
        else:
            print(f"❌ Real chat test failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Real chat test error: {e}")
    
    print()
    print("-" * 50)
    print("🏁 Backend testing complete!")
    print()
    print("If all tests pass, your backend is working correctly.")
    print("If the frontend still shows 'disconnected', it's likely a CORS issue.")
    print()
    print("Next steps:")
    print("1. Make sure both Django (port 8000) and React (port 3000) are running")
    print("2. Try opening http://localhost:8000/api/test/ in your browser")
    print("3. Check browser console for CORS errors when using the frontend")

if __name__ == "__main__":
    test_backend()
