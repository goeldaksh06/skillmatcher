# Skill Matcher

An AI-powered skill assessment platform that helps recruiters find the best candidates based on their skills and experience.

## Features

- AI-powered skill assessment
- Resume parsing and analysis
- Real-time assessment tracking
- Comprehensive analytics
- Secure authentication system
- API integrations

## Tech Stack

### Backend
- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Google Gemini AI

### Frontend (Coming Soon)
- React
- Material-UI
- Redux
- TypeScript

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/skill-matcher.git
cd skill-matcher
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python run.py
```

## Project Structure

```
SKILL_MATCHER/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
└── frontend/ (Coming Soon)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
