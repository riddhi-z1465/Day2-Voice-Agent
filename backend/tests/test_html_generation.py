import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from generate_order_html import generate_html

def test_html_generation():
    # Test case 1: Small Coffee with Whipped Cream
    order1 = {
        "drinkType": "Mocha",
        "size": "Small",
        "milk": "Whole",
        "extras": ["Whipped Cream", "Chocolate Syrup"],
        "name": "Alice"
    }
    output1 = "test_order_1.html"
    generate_html(order1, output1)
    
    with open(output1, "r") as f:
        content = f.read()
        assert "height: 150px" in content, "Small cup height incorrect"
        assert '<div class="whipped-cream"></div>' in content, "Whipped cream missing"
        assert "Alice" in content, "Name missing"
        
    print(f"Test 1 passed. Generated {output1}")

    # Test case 2: Large Coffee without Whipped Cream
    order2 = {
        "drinkType": "Latte",
        "size": "Large",
        "milk": "Oat",
        "extras": ["Sugar"],
        "name": "Bob"
    }
    output2 = "test_order_2.html"
    generate_html(order2, output2)
    
    with open(output2, "r") as f:
        content = f.read()
        assert "height: 250px" in content, "Large cup height incorrect"
        assert '<div class="whipped-cream"></div>' not in content, "Whipped cream should not be present"
        assert "Bob" in content, "Name missing"
        
    print(f"Test 2 passed. Generated {output2}")

if __name__ == "__main__":
    test_html_generation()
