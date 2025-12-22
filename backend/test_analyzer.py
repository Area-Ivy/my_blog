"""Test Elasticsearch analyzer configuration"""
import os
import sys
import json

try:
    from .search import get_search_client
except ImportError:
    from search import get_search_client

def test_analyzer():
    """Test the text_zh_search analyzer with Chinese text"""
    try:
        client = get_search_client()
        
        # Test the analyzer
        test_text = "服务端设施"
        print(f"Testing analyzer with text: {test_text}")
        print("-" * 50)
        
        response = client.indices.analyze(
            index="articles",
            body={
                "analyzer": "text_zh_search",
                "text": test_text
            }
        )
        
        tokens = response.get("tokens", [])
        print(f"Found {len(tokens)} tokens:")
        for i, token in enumerate(tokens, 1):
            print(f"  {i}. '{token.get('token')}' (position: {token.get('position')})")
        
        print("\n" + "=" * 50)
        print("Analyzer test result:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        
        # Also test with a longer sentence
        print("\n" + "-" * 50)
        test_text2 = "中华人民共和国"
        print(f"\nTesting with longer text: {test_text2}")
        response2 = client.indices.analyze(
            index="articles",
            body={
                "analyzer": "text_zh_search",
                "text": test_text2
            }
        )
        
        tokens2 = response2.get("tokens", [])
        print(f"Found {len(tokens2)} tokens:")
        for i, token in enumerate(tokens2, 1):
            print(f"  {i}. '{token.get('token')}' (position: {token.get('position')})")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_analyzer()

