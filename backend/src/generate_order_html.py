import os
import json

def generate_html(order_data, output_path):
    """
    Generates an HTML file visualizing the beverage order.
    
    Args:
        order_data (dict): The order details.
        output_path (str): The path to save the generated HTML file.
    """
    drink_type = order_data.get("drinkType", "Coffee")
    size = order_data.get("size", "Medium")
    milk = order_data.get("milk", "None")
    extras = order_data.get("extras", [])
    name = order_data.get("name", "Customer")
    
    # Determine cup size dimensions
    if size.lower() == "small":
        cup_height = "150px"
        cup_width = "100px"
    elif size.lower() == "large":
        cup_height = "250px"
        cup_width = "140px"
    else: # Medium
        cup_height = "200px"
        cup_width = "120px"
        
    # Check for whipped cream
    has_whipped_cream = False
    if extras:
        for extra in extras:
            if "whipped" in extra.lower() or "cream" in extra.lower():
                 has_whipped_cream = True
                 break

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order for {name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify_content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 30px;
        }}
        .visual-area {{
            position: relative;
            height: 300px;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            padding-top: 50px; /* Space for whipped cream */
        }}
        .cup {{
            width: {cup_width};
            height: {cup_height};
            background-color: #8D6E63; /* Coffee color */
            border-radius: 0 0 15px 15px;
            position: relative;
            box-shadow: inset -10px 0 20px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        .cup::before {{
            content: '';
            position: absolute;
            top: -10px;
            left: 0;
            width: 100%;
            height: 20px;
            background-color: #A1887F;
            border-radius: 50%;
            border: 2px solid #6D4C41;
            box-sizing: border-box;
        }}
        .cup-handle {{
            position: absolute;
            top: 20px;
            right: -30px;
            width: 30px;
            height: 50px;
            border: 8px solid #8D6E63;
            border-left: none;
            border-radius: 0 20px 20px 0;
        }}
        .whipped-cream {{
            position: absolute;
            top: -30px;
            left: 50%;
            transform: translateX(-50%);
            width: {cup_width};
            height: 50px;
            background-color: #FFF;
            border-radius: 50% 50% 10% 10%;
            box-shadow: inset -5px -5px 10px #EEE;
            z-index: 10;
        }}
        .whipped-cream::after {{
            content: '';
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 40px;
            height: 40px;
            background-color: #FFF;
            border-radius: 50% 50% 50% 0;
            transform: translateX(-50%) rotate(45deg);
        }}
        .receipt {{
            text-align: left;
            background-color: #fff8e1;
            padding: 20px;
            border: 1px dashed #ccc;
            width: 100%;
            max-width: 300px;
            box-sizing: border-box;
        }}
        .receipt h2 {{
            margin-top: 0;
            border-bottom: 1px solid #ccc;
            padding-bottom: 10px;
            font-size: 1.2em;
        }}
        .receipt-item {{
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
        }}
        .receipt-total {{
            margin-top: 15px;
            padding-top: 10px;
            border-top: 1px solid #ccc;
            font-weight: bold;
            text-align: right;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="visual-area">
            <div class="cup">
                <div class="cup-handle"></div>
                { '<div class="whipped-cream"></div>' if has_whipped_cream else '' }
            </div>
        </div>
        
        <div class="receipt">
            <h2>Order Receipt</h2>
            <div class="receipt-item">
                <span>Customer:</span>
                <span>{name}</span>
            </div>
            <div class="receipt-item">
                <span>Drink:</span>
                <span>{drink_type}</span>
            </div>
            <div class="receipt-item">
                <span>Size:</span>
                <span>{size}</span>
            </div>
            <div class="receipt-item">
                <span>Milk:</span>
                <span>{milk}</span>
            </div>
            <div class="receipt-item">
                <span>Extras:</span>
                <span>{', '.join(extras) if extras else 'None'}</span>
            </div>
            <div class="receipt-total">
                Status: Paid
            </div>
        </div>
    </div>
</body>
</html>
    """
    
    with open(output_path, "w") as f:
        f.write(html_content)
    
    return output_path
