#!/usr/bin/env python3
"""
Bank Demo Server with Claude AI Integration
Complete banking ecosystem with real AI charity selection
"""

import http.server
import socketserver
import os
import webbrowser
import time
import json
import math
import random
import asyncio
import threading
from urllib.parse import urlparse
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    print("Anthropic not installed. Install with: pip install anthropic")
    ANTHROPIC_AVAILABLE = False

# =============================================================================
# CONFIGURATION
# =============================================================================

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")
# =============================================================================
ACCOUNT = {
    "balance": 2847.93,
    "monthly_donated": 1.59
}

SETTINGS = {
    "roundups_enabled": True,
    "ai_charity_selection": True,
    "round_to_pound": True,
    "monthly_cap": False
}

CHARITIES = {
    "Teach First": {
        "name": "Teach First",
        "description": "Places exceptional graduates in challenging schools to tackle educational inequality",
        "costPerImpact": 25.50,
        "unit": "training hours",
        "focus": ["education", "books", "learning"],
        "keywords": ["book", "study", "education", "academic", "university", "college", "textbook", "waterstones", "amazon"],
        "color": "#4f46e5"
    },
    "Into University": {
        "name": "Into University", 
        "description": "Supports young people from disadvantaged backgrounds into higher education",
        "costPerImpact": 15.75,
        "unit": "mentoring sessions",
        "focus": ["education", "mentoring", "university"],
        "keywords": ["university", "college", "study", "academic", "course", "tuition", "campus"],
        "color": "#7c3aed"
    },
    "Coram Beanstalk": {
        "name": "Coram Beanstalk",
        "description": "Helps children who have fallen behind with their reading through volunteer support", 
        "costPerImpact": 12.30,
        "unit": "reading sessions",
        "focus": ["literacy", "children", "reading"],
        "keywords": ["book", "read", "library", "literature", "novel", "magazine", "children", "waterstones"],
        "color": "#059669"
    },
    "FareShare": {
        "name": "FareShare",
        "description": "Redistributes surplus food to charities and community groups fighting hunger",
        "costPerImpact": 8.50,
        "unit": "meals provided",
        "focus": ["food", "hunger", "community"],
        "keywords": ["food", "restaurant", "grocery", "supermarket", "cafe", "coffee", "lunch", "dinner", "snack", "costa", "tesco", "mcdonalds"],
        "color": "#dc2626"
    },
    "Crisis": {
        "name": "Crisis",
        "description": "Works directly with homeless people to help them rebuild their lives",
        "costPerImpact": 18.75,
        "unit": "support sessions",
        "focus": ["homelessness", "housing", "support"],
        "keywords": ["transport", "travel", "uber", "taxi", "bus", "train", "accommodation", "hotel"],
        "color": "#ea580c"
    },
    "Mind": {
        "name": "Mind",
        "description": "Provides advice and support to empower anyone experiencing a mental health problem",
        "costPerImpact": 22.00,
        "unit": "counseling hours",
        "focus": ["mental health", "wellbeing", "support"],
        "keywords": ["pharmacy", "health", "medical", "fitness", "gym", "wellness", "therapy", "counseling"],
        "color": "#0891b2"
    }
}

TRANSACTIONS = [
    {
        "id": 1,
        "merchant": "Costa Coffee",
        "amount": 4.65,
        "roundup": 0.35,
        "charity": "FareShare",
        "time": "2 minutes ago",
        "type": "purchase",
        "ai_confidence": 89
    },
    {
        "id": 2,
        "merchant": "Amazon Books",
        "amount": 23.99,
        "roundup": 0.01,
        "charity": "Teach First", 
        "time": "1 hour ago",
        "type": "purchase",
        "ai_confidence": 95
    },
    {
        "id": 3,
        "merchant": "Tesco Express",
        "amount": 8.47,
        "roundup": 0.53,
        "charity": "FareShare",
        "time": "3 hours ago", 
        "type": "purchase",
        "ai_confidence": 87
    },
    {
        "id": 4,
        "merchant": "Uber",
        "amount": 12.30,
        "roundup": 0.70,
        "charity": "Crisis",
        "time": "Yesterday",
        "type": "purchase",
        "ai_confidence": 92
    }
]

# =============================================================================
# AI CHARITY SELECTION
# =============================================================================

def ai_select_charity_claude(merchant_name, amount):
    """Use Claude AI to select the most appropriate charity"""
    if not CLAUDE_API_KEY or not ANTHROPIC_AVAILABLE:
        return fallback_charity_selection(merchant_name)
    
    try:
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        
        charities_info = "\n".join([
            f"- {name}: {info['description']} (£{info['costPerImpact']} per {info['unit']})"
            for name, info in CHARITIES.items()
        ])
        
        prompt = f"""You are an AI assistant for a banking app that helps students donate spare change to charities.

A student just made a purchase at "{merchant_name}" for £{amount:.2f}.

Available charities:
{charities_info}

Based on the merchant type and purchase context, which charity would be most appropriate for this transaction? 

Consider:
- What type of business this merchant is
- How the purchase relates to the charity's mission
- What would make sense to a student

Respond with only a JSON object in this format:
{{"charity": "Charity Name", "confidence": 85, "reasoning": "Brief explanation"}}

Choose from the exact charity names listed above."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text.strip()
        
        # Parse JSON response
        try:
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            result = json.loads(response_text)
            charity_name = result.get("charity", "Teach First")
            confidence = result.get("confidence", 85)
            reasoning = result.get("reasoning", "AI selected based on merchant type")
            
            # Validate charity name
            if charity_name not in CHARITIES:
                charity_name = "Teach First"  # Fallback
                
            print(f"🤖 AI selected {charity_name} with {confidence}% confidence: {reasoning}")
            return charity_name, confidence, reasoning
            
        except json.JSONDecodeError:
            print(f"Could not parse AI response: {response_text}")
            return fallback_charity_selection(merchant_name)
            
    except Exception as e:
        print(f"Claude AI error: {e}")
        return fallback_charity_selection(merchant_name)

def fallback_charity_selection(merchant_name):
    """Fallback charity selection when AI is not available"""
    merchant_lower = merchant_name.lower()
    
    # Smart keyword matching
    if any(word in merchant_lower for word in ['book', 'amazon', 'waterstones', 'study', 'education']):
        return "Teach First", 89, "Education-related purchase"
    elif any(word in merchant_lower for word in ['coffee', 'food', 'restaurant', 'tesco', 'cafe']):
        return "FareShare", 87, "Food-related purchase"
    elif any(word in merchant_lower for word in ['uber', 'transport', 'travel', 'taxi']):
        return "Crisis", 85, "Transport-related purchase"
    elif any(word in merchant_lower for word in ['gym', 'fitness', 'health', 'pharmacy']):
        return "Mind", 83, "Health/wellness-related purchase"
    else:
        return "Teach First", 75, "General education support"

# =============================================================================
# HTTP SERVER
# =============================================================================

class BankHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/' or path == '/bank':
                self.serve_file('bank_mobile_app.html')
            elif path == '/checkout':
                self.serve_file('checkout_demo.html')
            elif path == '/demo':
                self.serve_demo_page()
            elif path == '/api/account':
                self.serve_json(ACCOUNT)
            elif path == '/api/transactions':
                self.serve_json({"transactions": TRANSACTIONS})
            elif path == '/api/charities':
                self.serve_json({"charities": CHARITIES})
            elif path == '/api/settings':
                self.serve_json({"settings": SETTINGS})
            else:
                super().do_GET()
        except Exception as e:
            print(f"GET Error: {e}")
            self.send_error(500)
    
    def do_POST(self):
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/api/payment':
                self.handle_payment()
            elif path == '/api/settings':
                self.handle_settings_update()
            else:
                self.send_error(404)
        except Exception as e:
            print(f"POST Error: {e}")
            self.send_error(500)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def serve_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def serve_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            print(f"File not found: {filename}")
            self.send_error(404, f"File {filename} not found")
        except Exception as e:
            print(f"Error serving file {filename}: {e}")
            self.send_error(500)
    
    def handle_payment(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                payment_data = json.loads(post_data.decode('utf-8'))
            else:
                payment_data = {}
            
            amount = float(payment_data.get("amount", 10.0))
            merchant = payment_data.get("merchant", "Test Store")
            
            print(f"💳 Processing payment: £{amount:.2f} at {merchant}")
            
            # Check if roundups are enabled
            if not SETTINGS["roundups_enabled"]:
                roundup = 0.0
                charity = None
                ai_confidence = 0
                ai_reasoning = "Roundups disabled"
                print("Roundups disabled - no charity donation")
            else:
                # Calculate roundup
                if SETTINGS["round_to_pound"]:
                    roundup = round(math.ceil(amount) - amount, 2)
                else:
                    roundup = round((math.ceil(amount * 4) / 4) - amount, 2)  # Round to nearest 25p
                
                # Select charity using AI
                if SETTINGS["ai_charity_selection"]:
                    charity, ai_confidence, ai_reasoning = ai_select_charity_claude(merchant, amount)
                else:
                    charity, ai_confidence, ai_reasoning = fallback_charity_selection(merchant)
                
                # Check monthly cap
                if SETTINGS["monthly_cap"] and (ACCOUNT["monthly_donated"] + roundup) > 10.00:
                    old_roundup = roundup
                    roundup = max(0, 10.00 - ACCOUNT["monthly_donated"])
                    if roundup != old_roundup:
                        print(f"⚠️  Monthly cap reached. Roundup reduced from £{old_roundup:.2f} to £{roundup:.2f}")
            
            # Create transaction
            new_transaction = {
                "id": len(TRANSACTIONS) + 1,
                "merchant": merchant,
                "amount": amount,
                "roundup": roundup,
                "charity": charity,
                "time": "Just now",
                "type": "purchase",
                "ai_confidence": ai_confidence if charity else 0,
                "ai_reasoning": ai_reasoning if charity else "No charity donation"
            }
            
            # Update global state
            TRANSACTIONS.insert(0, new_transaction)
            ACCOUNT["balance"] = round(ACCOUNT["balance"] - amount, 2)
            if roundup > 0:
                ACCOUNT["monthly_donated"] = round(ACCOUNT["monthly_donated"] + roundup, 2)
            
            # Log the transaction
            if roundup > 0:
                print(f"Payment processed: £{amount:.2f} to {merchant}")
                print(f"AI selected {charity} (confidence: {ai_confidence}%)")
                print(f"Roundup: £{roundup:.2f} donated to {charity}")
                print(f"New balance: £{ACCOUNT['balance']:.2f}")
            else:
                print(f"Payment processed: £{amount:.2f} to {merchant} (no roundup)")
            
            # Send response
            response_data = {
                "status": "success",
                "transaction": new_transaction,
                "new_balance": ACCOUNT["balance"],
                "monthly_donated": ACCOUNT["monthly_donated"],
                "message": f"Payment processed! {f'£{roundup:.2f} donated to {charity}' if roundup > 0 else 'No roundup applied'}"
            }
            
            self.serve_json(response_data)
            
        except Exception as e:
            print(f"Payment error: {e}")
            error_response = {
                "status": "error",
                "message": f"Payment failed: {str(e)}"
            }
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def handle_settings_update(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                settings_data = json.loads(post_data.decode('utf-8'))
                
                # Update settings
                for key, value in settings_data.items():
                    if key in SETTINGS:
                        SETTINGS[key] = value
                        print(f"Setting updated: {key} = {value}")
                
                self.serve_json({"status": "success", "settings": SETTINGS})
            else:
                self.serve_json({"settings": SETTINGS})
            
        except Exception as e:
            print(f"Settings error: {e}")
            self.send_error(400, f"Invalid settings data: {str(e)}")
    
    def serve_demo_page(self):
        ai_status = "Claude AI Enabled" if (CLAUDE_API_KEY and ANTHROPIC_AVAILABLE) else "⚠️ Claude AI Disabled (Add API key)"
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GoodCents Banking Demo</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: white; padding: 2rem; margin: 0;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ 
            text-align: center; margin-bottom: 3rem; 
            background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 20px;
            backdrop-filter: blur(10px);
        }}
        .logo {{ font-size: 3rem; margin-bottom: 1rem; }}
        .status {{ 
            padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; 
            background: {'rgba(34,197,94,0.2)' if (CLAUDE_API_KEY and ANTHROPIC_AVAILABLE) else 'rgba(239,68,68,0.2)'};
            border: 1px solid {'#22c55e' if (CLAUDE_API_KEY and ANTHROPIC_AVAILABLE) else '#ef4444'};
        }}
        .demo-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem; }}
        .demo-card {{ 
            background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 20px; 
            text-align: center; backdrop-filter: blur(10px);
        }}
        .demo-button {{ 
            background: #4f46e5; color: white; padding: 1rem 2rem; 
            border-radius: 10px; text-decoration: none; display: inline-block;
            transition: all 0.3s ease;
        }}
        .demo-button:hover {{ background: #3730a3; transform: translateY(-2px); }}
        .instructions {{ 
            background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 20px;
            backdrop-filter: blur(10px);
        }}
        .step {{ 
            margin-bottom: 1rem; padding: 1rem; 
            background: rgba(0,0,0,0.3); border-radius: 10px;
        }}
        .api-key-notice {{
            background: rgba(239,68,68,0.1); border: 1px solid #ef4444;
            padding: 1rem; border-radius: 10px; margin-top: 1rem;
        }}
        @media (max-width: 768px) {{
            .demo-grid {{ grid-template-columns: 1fr; }}
            body {{ padding: 1rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="logo">GoodCents Banking Demo</h1>
            <p>AI-powered charity roundups for student banking</p>
            <div class="status">{ai_status}</div>
        </div>

        <div class="demo-grid">
            <div class="demo-card">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📱</div>
                <h2>Bank Mobile App</h2>
                <p>Banking interface with AI charity selection</p>
                <a href="/bank" target="_blank" class="demo-button">Open Mobile Bank</a>
            </div>

            <div class="demo-card">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🛒</div>
                <h2>E-Commerce Checkout</h2>
                <p>Test payments with real-time updates</p>
                <a href="/checkout" target="_blank" class="demo-button">Open Checkout</a>
            </div>
        </div>

        <div class="instructions">
            <h3>Demo Instructions</h3>
            <div class="step"><strong>1.</strong> Open both apps using the buttons above</div>
            <div class="step"><strong>2.</strong> In mobile bank: Check transactions and charity settings</div>
            <div class="step"><strong>3.</strong> In checkout: Select merchant type and make payment</div>
            <div class="step"><strong>4.</strong> Watch AI select charity and transaction appear instantly</div>
            <div class="step"><strong>5.</strong> Toggle settings to see behavior changes</div>
            <div class="step"><strong>6.</strong> Try different merchants to see AI variety</div>
        </div>
        
        {f'''
        <div class="api-key-notice">
            <h4>Add Claude API Key for Full AI Features</h4>
            <p>Edit the server file and add your Claude API key to enable real AI charity selection.</p>
            <code>CLAUDE_API_KEY = "your-api-key-here"</code>
        </div>
        ''' if not CLAUDE_API_KEY else ''}

        <div style="text-align: center; margin-top: 2rem; opacity: 0.7;">
            <p>Server running • Real-time updates • AI-powered charity matching</p>
        </div>
    </div>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

# =============================================================================
# MAIN SERVER
# =============================================================================

def start_server(port=8000):
    try:
        with socketserver.TCPServer(("", port), BankHandler) as httpd:
            ai_status = "Claude AI Ready" if (CLAUDE_API_KEY and ANTHROPIC_AVAILABLE) else "⚠️ No AI (add API key)"
            
            print(f"""
GoodCents Banking Demo Server
================================

✅ Server running at: http://localhost:{port}
{ai_status}

📱 Quick Links:
   • Demo Overview: http://localhost:{port}/demo
   • Mobile Bank:   http://localhost:{port}/bank  
   • Checkout:      http://localhost:{port}/checkout

🎯 Features:
   • Real-time payment processing
   • AI charity selection with Claude
   • Live transaction updates
   • Settings that actually work
   • Professional demo interface

📋 Required Files:
   • bank_mobile_app.html
   • checkout_demo.html

💡 To enable full AI features:
   1. Get Claude API key from https://console.anthropic.com
   2. Add it to CLAUDE_API_KEY variable in this file
   3. Install: pip install anthropic

Press Ctrl+C to stop.
            """)
            
            # Try to open browser
            try:
                time.sleep(1)
                webbrowser.open(f'http://localhost:{port}/demo')
            except:
                pass
            
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {port} is already in use.")
            print(f"Try: python {__file__} {port+1}")
        else:
            print(f"Server error: {e}")
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    import sys
    
    # Check for API key
    if not CLAUDE_API_KEY:
        print("""
⚠️  Claude API Key Not Set
========================

To enable full AI features:
1. Get your API key from: https://console.anthropic.com
2. Edit this file and set: CLAUDE_API_KEY = "your-key-here" 
3. Install anthropic: pip install anthropic

The demo will work without AI, but with basic charity selection.
        """)
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    
    # Check required files
    required_files = ['bank_mobile_app.html', 'checkout_demo.html']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"Missing files: {', '.join(missing_files)}")
        print("Download the complete file set and run from the same directory.")
    else:
        start_server(port)