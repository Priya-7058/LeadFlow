# LeadFlow — AI-Powered Lead Management API

LeadFlow is a REST API built with Python and FastAPI that helps businesses manage sales leads, validate customer information, prevent duplicate records, track lead statuses, and classify customer enquiries using Google Gemini AI.

The project demonstrates API development, database integration, input validation, automated testing, and practical LLM integration.

## Features

### Lead Management
- Create new leads.
- Retrieve individual leads and list all leads.
- Update existing lead details.
- Delete leads.
- Track lead statuses: New, Contacted, Qualified, Converted, and Lost.
- Prevent duplicate email addresses.

### Search and Filtering
- Search leads by name, email, or company.
- Filter leads by status.
- Support pagination using `skip` and `limit`.

### AI-Powered Classification
- Analyze customer enquiries using Google Gemini.
- Classify leads as High, Medium, or Low potential.
- Generate an explanation for each classification.
- Recommend a suggested next action for the sales team.

### Validation and Testing
- Validate request data using Pydantic.
- Validate email addresses.
- Enforce field length constraints.
- Handle missing leads and duplicate records.
- Test API endpoints and AI service failures using pytest.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| FastAPI | REST API framework |
| Pydantic | Request validation and response schemas |
| SQLAlchemy | Database ORM |
| SQLite | Database |
| Google Gemini API | AI-powered lead classification |
| pytest | Automated testing |
| Uvicorn | Development server |
| python-dotenv | Environment variable loading |

## Project Structure

```text
LeadFlow/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── ai_service.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── .env
├── .gitignore
├── README.md
├── leadflow.db
├── list_gemini_models.py
├── test_ai_service.py
├── test_gemini.py
└── test_main.py
```

## Prerequisites

- Python installed on your system.
- pip, Python's package installer.
- A Google Gemini API key for AI classification.

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd LeadFlow
```

Replace the placeholder with your repository URL after publishing the project.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install fastapi uvicorn sqlalchemy pytest httpx email-validator google-genai python-dotenv
```

### 4. Configure your environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key.

**Security:** Never commit your real API key or `.env` file to GitHub.

### 5. Start the application

```bash
python -m uvicorn app.main:app --reload
```

The API will be available locally at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

Health check:

`http://127.0.0.1:8000/health`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/leads` | Create a lead |
| GET | `/leads` | List leads with search, filtering, and pagination |
| GET | `/leads/{lead_id}` | Retrieve a specific lead |
| PUT | `/leads/{lead_id}` | Update lead details |
| PATCH | `/leads/{lead_id}/status` | Update lead status |
| DELETE | `/leads/{lead_id}` | Delete a lead |
| POST | `/leads/classify` | Classify a customer enquiry using AI |

## Example: Create a Lead

Request:

```http
POST /leads
Content-Type: application/json
```

```json
{
  "name": "Alex Johnson",
  "email": "alex@example.com",
  "phone": "9876543210",
  "company": "Example Technologies",
  "enquiry": "We need an AI automation solution for our sales team."
}
```

A successful creation returns HTTP `201 Created`.

## Example: Classify a Lead

Request:

```http
POST /leads/classify
Content-Type: application/json
```

```json
{
  "enquiry": "We want to purchase an AI automation solution this month. Please send pricing."
}
```

Example response:

```json
{
  "classification": "High",
  "reason": "The customer has a specific purchasing timeline and has requested pricing.",
  "suggested_action": "Contact the customer and provide pricing details."
}
```

The example response is illustrative. Actual AI-generated wording may vary.

## Search and Filtering

Search leads by name, email, or company:

```http
GET /leads?search=Example
```

Filter by status:

```http
GET /leads?status=Qualified
```

Combine search, status filtering, and pagination:

```http
GET /leads?search=Example&status=New&skip=0&limit=10
```

## Running Tests

Run the automated test suite:

```bash
python -m pytest -v -p no:cacheprovider
```

The project currently has **10 passing automated tests**, covering core endpoints, lead creation, validation, duplicate prevention, AI classification responses, invalid AI requests, and AI service failure handling.

AI endpoint tests use mocked responses to avoid making real Gemini API calls during automated testing.

## Error Handling

The API handles common error scenarios, including:

- Invalid request data.
- Duplicate email addresses.
- Requests for leads that do not exist.
- Invalid lead statuses.
- AI service failures.

## Future Improvements

Potential enhancements include:

- Automatically classify a lead when it is created.
- Store AI classifications and recommendations in the database.
- Add lead scoring and prioritization.
- Add authentication and authorization.
- Introduce structured logging and more comprehensive tests.
- Add Docker support and deployment configuration.
- Build a frontend dashboard for sales teams.

## Disclaimer

AI-generated classifications are recommendations, not guarantees of a customer's likelihood to purchase. Sales teams should use them alongside other relevant information.

## Author

Developed as a Python backend and AI integration project to demonstrate REST API development, database management, testing, and LLM-powered business automation.