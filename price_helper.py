import requests
from bs4 import BeautifulSoup
import re
import time
from statistics import mean, median
import concurrent.futures

def clean_price(price_str):
    """Extract and clean price from string"""
    if not price_str:
        return None
    price = re.findall(r'\d+\.?\d*', price_str.replace(',', ''))
    return float(price[0]) if price else None

def search_amazon(query):
    """Search Amazon for prices"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f'https://www.amazon.com/s?k={query}'
    
    try:
        print(f"Searching Amazon for: {query}")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Amazon status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Amazon error response: {response.text[:500]}")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        prices = []
        price_elements = soup.select('.a-price-whole')
        print(f"Found {len(price_elements)} price elements on Amazon")
        
        for price in price_elements:
            clean = clean_price(price.text)
            if clean:
                prices.append(clean)
                print(f"Found Amazon price: ${clean:.2f}")
        
        return prices[:5] if prices else []
    except Exception as e:
        print(f"Amazon search error: {str(e)}")
        return []

def search_ebay(query):
    """Search eBay for prices"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f'https://www.ebay.com/sch/i.html?_nkw={query}'
    
    try:
        print(f"Searching eBay for: {query}")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"eBay status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"eBay error response: {response.text[:500]}")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        prices = []
        price_elements = soup.select('.s-item__price')
        print(f"Found {len(price_elements)} price elements on eBay")
        
        for price in price_elements:
            clean = clean_price(price.text)
            if clean:
                prices.append(clean)
                print(f"Found eBay price: ${clean:.2f}")
        
        return prices[:5] if prices else []
    except Exception as e:
        print(f"eBay search error: {str(e)}")
        return []

def format_price_range(prices):
    """Format price range from list of prices"""
    if not prices:
        return "N/A"
    
    min_price = min(prices)
    max_price = max(prices)
    
    if min_price == max_price:
        return f"${min_price:.2f}"
    return f"${min_price:.2f} - ${max_price:.2f}"

def search_prices(item_name, item_type, brand):
    """Search for new and used prices of an item"""
    try:
        # Construct search query
        search_query = f"{brand} {item_name} {item_type}".strip()
        search_query = re.sub(r'\s+', '+', search_query)
        print(f"\nStarting price search for: {search_query}")
        
        # Search both platforms concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            amazon_future = executor.submit(search_amazon, search_query)
            ebay_future = executor.submit(search_ebay, search_query)
            
            amazon_prices = amazon_future.result()
            ebay_prices = ebay_future.result()
        
        # Combine and analyze prices
        all_prices = amazon_prices + ebay_prices
        if not all_prices:
            return {
                "new_price": "N/A",
                "used_price": "N/A",
                "search_query": search_query,
                "amazon_url": f"https://www.amazon.com/s?k={search_query}",
                "ebay_url": f"https://www.ebay.com/sch/i.html?_nkw={search_query}"
            }
        
        # Sort prices and estimate new vs used
        all_prices.sort()
        split_point = len(all_prices) // 2
        higher_prices = all_prices[split_point:]  # Assume higher prices are new
        lower_prices = all_prices[:split_point]   # Assume lower prices are used
        
        return {
            "new_price": format_price_range(higher_prices),
            "used_price": format_price_range(lower_prices),
            "search_query": search_query,
            "amazon_url": f"https://www.amazon.com/s?k={search_query}",
            "ebay_url": f"https://www.ebay.com/sch/i.html?_nkw={search_query}"
        }
        
    except Exception as e:
        print(f"Error searching prices: {str(e)}")
        return {
            "new_price": "N/A",
            "used_price": "N/A",
            "search_query": search_query
        }
