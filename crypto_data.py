from flask import Flask, render_template, request
import openai
import requests
import json

# Set up Flask app
app = Flask(__name__, template_folder='templates')

# Set up OpenAI API credentials
openai.api_key = "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"

# CoinGecko API endpoint for top 100 cryptocurrencies by market cap
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en"

def get_crypto_data():
    # Retrieve data from CoinGecko API endpoint
    response = requests.get(url)
    data = json.loads(response.content)
    print('Making request to CoinGecko API...')
    return data
    

# Define home page route
@app.route('/')
def home():
    return render_template('index.html')

# Define route for chatbot response
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get user input from form
    question = request.form['question']
    
    # Use GPT-3 model to generate response
    response = openai.Completion.create(
        engine="davinci", prompt=question, max_tokens=1024, n=1, stop=None, temperature=0.5,
    )
    
    # Format response as a string
    response_text = response.choices[0].text
    
    # Format response as HTML
    response_html = response_text.replace('\n', '<br>').replace('<br>', '\n')
    
    # Retrieve data from CoinGecko API endpoint
    data = get_crypto_data()
    
    # Loop through the list of cryptocurrency dictionaries to find Ethereum's data
    for crypto in data:
        if crypto['id'] == 'ethereum':
            if 'market_data' in crypto:
                ethereum_data = crypto['market_data']
                ethereum_total_supply = ethereum_data.get('total_supply')
                if ethereum_total_supply:
                    response_html += f"<br><br>The total supply of Ethereum is {ethereum_total_supply:,} ETH."
                else:
                    response_html += "<br><br>The total supply of Ethereum is not available."
            else:
                response_html += "<br><br>Market data for Ethereum is not available."
            break
    
    # Render template with chatbot response
    return render_template('chatbot.html', response=response_html)

if __name__ == '__main__':
    app.run(debug=True)





