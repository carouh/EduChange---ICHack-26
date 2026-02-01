# GoodCents Banking Ecosystem

> Transform spare change into meaningful impact through intelligent charity roundups

## Overview

GoodCents is an innovative banking feature that automatically rounds up everyday transactions and donates the spare change to charitable causes. Built as a hackathon proof-of-concept, this project demonstrates how modern banking apps can seamlessly integrate charitable giving into the customer experience.

### The Big Idea

Every time you make a purchase, the transaction amount is rounded up to the nearest pound (or dollar), and the difference is automatically donated to charity. For example:

- Purchase: £4.67 → Roundup: £0.33 donated
- Purchase: £15.43 → Roundup: £0.57 donated
- Purchase: £28.99 → Roundup: £0.01 donated

These micro-donations accumulate throughout the month, turning everyday spending into meaningful charitable contributions without requiring any conscious effort from the user.

## Key Features

### AI-Powered Charity Matching

The system uses intelligent algorithms to recommend charities based on:

- **Purchase patterns**: What categories you spend money on
- **Transaction context**: What you're buying and from whom
- **Personal preferences**: Your saved charity preferences (when available)
- **Confidence scoring**: Each recommendation includes an AI confidence level

**Example**: Buying educational supplies triggers recommendations for education-focused charities like Room to Read or Khan Academy, with 89% confidence matching.

### Bank-Agnostic Architecture

GoodCents is designed as a **white-label feature** that can be adopted by any banking institution:

- Clean API integration for existing banking systems
- Customizable branding and charity partner networks
- Regulatory compliance framework built-in
- Minimal technical overhead for implementation

### Seamless User Experience

- **Zero friction**: Roundups happen automatically on every transaction
- **Real-time updates**: Instant reflection in mobile banking app
- **Full transparency**: Clear breakdown of donations and impact
- **User control**: Easy opt-in/opt-out and charity preferences

## Project Structure

This demonstration includes three integrated components:

### 1. Bank Mobile App (`bank_mobile_app.html`)

A simulated, modern, responsive mobile banking interface featuring:

- Account balance and transaction history
- Dedicated GoodCents charity tab
- AI charity recommendations with confidence scores
- Monthly donation tracking and impact metrics
- Professional iOS/Android-style design

### 2. E-Commerce Checkout (`checkout_demo.html`)

A simulated online shopping checkout that:

- Processes payments through the banking backend
- Calculates automatic roundups
- Demonstrates real-world integration scenarios
- Shows instant transaction updates

### 3. Good Cents Server (`good_cents_server.py`)

A Python-based demo server providing:

- RESTful API for payment processing
- State management for accounts and transactions
- Real-time roundup calculations
- Demo orchestration and presentation mode

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation & Running

1. **Ensure all files are in the same directory:**
   ```
   bank_mobile_app.html
   checkout_demo.html
   good_cents_server.py
   ```

2. **Start the server:**
   ```bash
   python good_cents_server.py
   ```

3. **Access the demo:**
   The server will automatically open your browser to `http://localhost:8000/demo`

   Or manually visit:
   - **Demo Overview**: http://localhost:8000/demo
   - **Mobile Bank**: http://localhost:8000/bank
   - **E-Commerce Checkout**: http://localhost:8000/checkout


### Key Points

- **Effortless giving**: No conscious action required from users
- **Meaningful impact**: Small amounts accumulate into significant donations
- **AI personalization**: Smart charity matching based on spending behavior
- **Universal adoption**: Any bank can integrate this feature
- **Financial inclusion**: Makes charitable giving accessible to everyone


### AI Recommendation Engine

The system analyzes:
1. **Merchant category** (e.g., "BookDepot" → Education)
2. **Purchase amount** (micro vs. large purchases)
3. **User history** (saved preferences if available)
4. **Charity database** (matching causes to context)

Output: Ranked charity recommendations with confidence scores

## Real-World Applications

### For Consumers
- **Painless giving**: Donate without thinking about it
- **Budget-friendly**: Never more than £1 per transaction
- **Personalized impact**: Support causes that align with lifestyle
- **Transparency**: See exactly where money goes

### For Charities
- **Consistent funding**: Predictable monthly micro-donations
- **Lower acquisition costs**: Automatic donor enrollment
- **Broader reach**: Access to entire customer base
- **Data insights**: Understanding donor behavior patterns

### For Banks
- **Customer engagement**: Increase app usage and brand loyalty
- **CSR initiatives**: Built-in corporate social responsibility
- **Competitive differentiation**: Stand out in crowded banking market
- **New revenue streams**: Partnership opportunities with charities

## Future Enhancements

- [ ] **Charity portfolio management**: Select multiple favorite charities
- [ ] **Donation matching**: Banks match customer roundups
- [ ] **Impact tracking**: See real outcomes from donations (schools built, meals provided, etc.)
- [ ] **Social features**: Share impact with friends, team challenges
- [ ] **Tax integration**: Automatic donation receipts for tax deductions
- [ ] **Cryptocurrency support**: Roundup donations in crypto
- [ ] **International expansion**: Multi-currency and global charity networks
- [ ] **Advanced AI**: Machine learning for better charity recommendations
- [ ] **Gamification**: Badges, milestones, and achievement tracking

## Market Potential

- **50M+ banking customers** in UK alone
- **Average roundup**: £0.30 per transaction
- **Average transactions**: 15 per month
- **Potential monthly donation per user**: £4.50
- **Total market potential**: £225M+ monthly for UK market

## Integration Guide

Banks interested in implementing GoodCents can:

1. **White-label the interface** with their branding
2. **Integrate API endpoints** into existing backend systems
3. **Customize charity network** based on regional presence
4. **Configure roundup rules** (to nearest £1, 50p, etc.)
5. **Deploy regulatory compliance** per jurisdiction


## Acknowledgments

This is a demonstration project showcasing the GoodCents concept, built as a hackathon demonstration of how technology can make charitable giving frictionless and accessible to everyone.


**Made with ❤️ for making the world a better place, one transaction at a time.**
