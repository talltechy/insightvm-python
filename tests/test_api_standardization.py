#!/usr/bin/env python3
"""
Test script for API standardization changes.

This script verifies that:
1. New pattern (_request() direct usage) returns parsed JSON
2. Legacy pattern (helper methods) returns Response objects
3. Binary download pattern (return_raw=True) works correctly
4. Backward compatibility is maintained
"""

import sys
from typing import Dict, Any
import requests

# Add src to path
sys.path.insert(0, 'src')

from rapid7 import InsightVMClient


def test_new_pattern_scans_api(client: InsightVMClient) -> bool:
    """
    Test ScansAPI (new pattern) - should return parsed JSON directly.
    """
    print("\n=== Testing ScansAPI (New Pattern) ===")
    
    try:
        # Test list() method
        result = client.scans.list(page=0, size=10)
        
        # Verify return type
        if not isinstance(result, dict):
            print(f"❌ FAIL: scans.list() returned {type(result)}, expected dict")
            return False
        
        # Check for expected keys
        if 'resources' not in result:
            print(f"❌ FAIL: scans.list() missing 'resources' key")
            return False
        
        print(f"✅ PASS: scans.list() returns dict with 'resources'")
        print(f"   Type: {type(result)}")
        print(f"   Keys: {list(result.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_new_pattern_reports_api(client: InsightVMClient) -> bool:
    """
    Test ReportsAPI (new pattern) - should return parsed JSON directly.
    """
    print("\n=== Testing ReportsAPI (New Pattern) ===")
    
    try:
        # Test list() method
        result = client.reports.list(page=0, size=10)
        
        # Verify return type
        if not isinstance(result, dict):
            print(f"❌ FAIL: reports.list() returned {type(result)}, expected dict")
            return False
        
        # Check for expected keys
        if 'resources' not in result:
            print(f"❌ FAIL: reports.list() missing 'resources' key")
            return False
        
        print(f"✅ PASS: reports.list() returns dict with 'resources'")
        print(f"   Type: {type(result)}")
        print(f"   Keys: {list(result.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_legacy_pattern_assets_api(client: InsightVMClient) -> bool:
    """
    Test AssetAPI (legacy pattern) - should return Response objects.
    """
    print("\n=== Testing AssetAPI (Legacy Pattern) ===")
    
    try:
        # Access the internal method that uses helper methods
        # We'll test by calling the internal get() method directly
        response = client.assets.get('assets', params={'page': 0, 'size': 10})
        
        # Verify return type is Response
        if not isinstance(response, requests.Response):
            print(f"❌ FAIL: assets.get() returned {type(response)}, expected Response")
            return False
        
        # Verify we can call .json()
        data = response.json()
        if not isinstance(data, dict):
            print(f"❌ FAIL: response.json() returned {type(data)}, expected dict")
            return False
        
        print(f"✅ PASS: assets.get() returns Response object")
        print(f"   Type: {type(response)}")
        print(f"   Can call .json(): True")
        print(f"   Data type after .json(): {type(data)}")
        
        # Also test the public list() method which wraps this
        list_result = client.assets.list(page=0, size=10)
        if not isinstance(list_result, dict):
            print(f"❌ FAIL: assets.list() returned {type(list_result)}, expected dict")
            return False
        
        print(f"✅ PASS: assets.list() correctly parses JSON internally")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_legacy_pattern_sites_api(client: InsightVMClient) -> bool:
    """
    Test SiteAPI (legacy pattern) - should return Response objects.
    """
    print("\n=== Testing SiteAPI (Legacy Pattern) ===")
    
    try:
        # Test internal get() method
        response = client.sites.get('sites', params={'page': 0, 'size': 10})
        
        # Verify return type is Response
        if not isinstance(response, requests.Response):
            print(f"❌ FAIL: sites.get() returned {type(response)}, expected Response")
            return False
        
        # Verify we can call .json()
        data = response.json()
        if not isinstance(data, dict):
            print(f"❌ FAIL: response.json() returned {type(data)}, expected dict")
            return False
        
        print(f"✅ PASS: sites.get() returns Response object")
        print(f"   Type: {type(response)}")
        print(f"   Can call .json(): True")
        
        # Also test the public list() method
        list_result = client.sites.list(page=0, size=10)
        if not isinstance(list_result, dict):
            print(f"❌ FAIL: sites.list() returned {type(list_result)}, expected dict")
            return False
        
        print(f"✅ PASS: sites.list() correctly parses JSON internally")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_direct_request_method(client: InsightVMClient) -> bool:
    """
    Test _request() method directly with both return modes.
    """
    print("\n=== Testing BaseAPI._request() Method ===")
    
    try:
        # Test default behavior (returns JSON)
        print("\n--- Testing _request() with default behavior (JSON parsing) ---")
        json_result = client.assets._request('GET', 'assets', params={'page': 0, 'size': 1})
        
        if not isinstance(json_result, dict):
            print(f"❌ FAIL: _request() default returned {type(json_result)}, expected dict")
            return False
        
        print(f"✅ PASS: _request() default returns parsed JSON")
        print(f"   Type: {type(json_result)}")
        print(f"   Has 'resources': {'resources' in json_result}")
        
        # Test return_raw=True (returns Response)
        print("\n--- Testing _request() with return_raw=True ---")
        raw_result = client.assets._request(
            'GET', 'assets', 
            params={'page': 0, 'size': 1},
            return_raw=True
        )
        
        if not isinstance(raw_result, requests.Response):
            print(f"❌ FAIL: _request(return_raw=True) returned {type(raw_result)}, expected Response")
            return False
        
        print(f"✅ PASS: _request(return_raw=True) returns Response object")
        print(f"   Type: {type(raw_result)}")
        print(f"   Can access .content: {len(raw_result.content)} bytes")
        print(f"   Can call .json(): {isinstance(raw_result.json(), dict)}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_type_consistency(client: InsightVMClient) -> bool:
    """
    Test that return types match type hints across all modules.
    """
    print("\n=== Testing Type Consistency ===")
    
    all_passed = True
    
    # Test Scans API
    try:
        scans_list = client.scans.list()
        if not isinstance(scans_list, dict):
            print(f"❌ FAIL: scans.list() type mismatch")
            all_passed = False
        else:
            print(f"✅ PASS: scans.list() -> Dict[str, Any]")
    except Exception as e:
        print(f"❌ ERROR in scans.list(): {e}")
        all_passed = False
    
    # Test Reports API
    try:
        reports_list = client.reports.list()
        if not isinstance(reports_list, dict):
            print(f"❌ FAIL: reports.list() type mismatch")
            all_passed = False
        else:
            print(f"✅ PASS: reports.list() -> Dict[str, Any]")
    except Exception as e:
        print(f"❌ ERROR in reports.list(): {e}")
        all_passed = False
    
    # Test Assets API
    try:
        assets_list = client.assets.list()
        if not isinstance(assets_list, dict):
            print(f"❌ FAIL: assets.list() type mismatch")
            all_passed = False
        else:
            print(f"✅ PASS: assets.list() -> Dict[str, Any]")
    except Exception as e:
        print(f"❌ ERROR in assets.list(): {e}")
        all_passed = False
    
    # Test Sites API
    try:
        sites_list = client.sites.list()
        if not isinstance(sites_list, dict):
            print(f"❌ FAIL: sites.list() type mismatch")
            all_passed = False
        else:
            print(f"✅ PASS: sites.list() -> Dict[str, Any]")
    except Exception as e:
        print(f"❌ ERROR in sites.list(): {e}")
        all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("=" * 70)
    print("API STANDARDIZATION TEST SUITE")
    print("=" * 70)
    
    # Create client
    try:
        print("\n📡 Connecting to InsightVM...")
        client = InsightVMClient()
        print(f"✅ Connected to: {client.auth.base_url}")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        print("\nMake sure:")
        print("  1. .env file exists with credentials")
        print("  2. InsightVM instance is accessible")
        print("  3. Credentials are valid")
        return 1
    
    # Run all tests
    tests = [
        ("New Pattern - Scans API", test_new_pattern_scans_api),
        ("New Pattern - Reports API", test_new_pattern_reports_api),
        ("Legacy Pattern - Assets API", test_legacy_pattern_assets_api),
        ("Legacy Pattern - Sites API", test_legacy_pattern_sites_api),
        ("Direct _request() Method", test_direct_request_method),
        ("Type Consistency", test_type_consistency),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func(client)
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ EXCEPTION in {test_name}: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n📊 Results: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! Standardization is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed. Review output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
