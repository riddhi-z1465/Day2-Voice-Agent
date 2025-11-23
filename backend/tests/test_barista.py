import unittest
import json
import os
import shutil
import asyncio
from agent import BaristaAgent, save_order_to_file

class TestBaristaAgent(unittest.TestCase):
    def setUp(self):
        self.orders_dir = "orders"
        if os.path.exists(self.orders_dir):
            shutil.rmtree(self.orders_dir)

    def tearDown(self):
        if os.path.exists(self.orders_dir):
            shutil.rmtree(self.orders_dir)

    def test_save_order_helper(self):
        # Test the helper function directly
        drink_type = "Latte"
        size = "Medium"
        milk = "Oat"
        extras = ["Vanilla Syrup"]
        name = "John"

        result = save_order_to_file(drink_type, size, milk, extras, name)
        
        self.assertEqual(result, "Order saved successfully.")
        self.assertTrue(os.path.exists(self.orders_dir))
        self.assertTrue(os.path.isdir(self.orders_dir))
        
        # Check if a file was created
        files = os.listdir(self.orders_dir)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].startswith("order_"))
        self.assertTrue(files[0].endswith(".json"))
        
        with open(os.path.join(self.orders_dir, files[0]), 'r') as f:
            saved_data = json.load(f)
            
        expected_data = {
            "drinkType": drink_type,
            "size": size,
            "milk": milk,
            "extras": extras,
            "name": name
        }
        self.assertEqual(saved_data, expected_data)

    def test_agent_initialization(self):
        # Test that the agent initializes with the correct instructions
        agent = BaristaAgent()
        self.assertIn("barista", agent.instructions.lower())

if __name__ == '__main__':
    unittest.main()
