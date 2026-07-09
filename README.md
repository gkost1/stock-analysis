# stock-analysis

Stock analysis tooling using the [Finnhub](https://finnhub.io/) API.

## Setup

1. Install [Poetry](https://python-poetry.org/docs/#installation) 

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Create a `.env` file in the project root with your Finnhub API key:

   ```bash
   FINNHUB_API_KEY=your_api_key_here
   ```

4. Run the script:

   ```bash
   poetry run python dataloader.py
   ```
