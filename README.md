# Attendance Automation API

An automated attendance system using Selenium and FastAPI to handle sign-in/sign-out operations.

## Project Structure

```
project_root/
├── app/                    # Application package
│   ├── __init__.py        # Makes app a Python package
│   └── main.py            # Main application file
├── tests/                 # Test directory
├── .env                   # Environment variables (not in git)
├── .env.template          # Template for environment variables
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile            # Docker build instructions
└── requirements.txt      # Python dependencies
```

## Setup

1. Clone the repository
2. Copy `.env.template` to `.env` and fill in your credentials:
   ```bash
   cp .env.template .env
   ```

3. Build and run with Docker:
   ```bash
   docker-compose up --build
   ```

## API Endpoints

The API will be available at `http://localhost:6060` with the following endpoints:

- `/docs` - OpenAPI documentation
- `/sign-in` - POST endpoint for signing in
- `/sign-out` - POST endpoint for signing out

## Development

To run tests:
```bash
python -m pytest tests/
```

To run the application locally without Docker:
```bash
uvicorn app.main:app --reload --port 6060
```

## Environment Variables

Required environment variables:
- `LOGIN_USERNAME`: Your login username
- `LOGIN_PASSWORD`: Your login password

## License

[Your License Here]