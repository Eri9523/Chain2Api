# SmartContracts-to-API

A clean-architecture API service that bridges the gap between Ronin Network smart contracts and RESTful endpoints.

## Overview

This project exposes a simplified HTTP API to interact with complex smart contracts (ERC20 tokens, DEXs, etc.) on the Ronin blockchain. It abstracts away the complexity of Web3, ABIs, and contract interactions, providing a clean interface for developers.


## Setup

1.  **Clone the repository**
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment**:
    Copy `.env.example` to `.env` and set your provider URL:
    ```env
    WEB3_HTTPS_PROVIDER_URL=https://api.roninchain.com/rpc
    ```

## API Endpoints

Once running, the API provides the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tokens/` | List all supported tokens |
| `GET` | `/tokens/{symbol}/balance/{address}` | Get token balance for a wallet |
| `GET` | `/tokens/{symbol}/price` | Get current price in USDC (via Katana) |
| `GET` | `/tokens/{symbol}/supply` | Get total token supply |

## Running the Server

```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive Swagger UI.
