# Emotion-Aware Agent

An intelligent agent capable of understanding and responding to human emotions through natural language processing.

## Features

- Emotion detection from text input
- Context-aware responses
- RESTful API endpoint for integration
- Built with Python and modern NLP libraries

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/emotion-aware-agent.git
   cd emotion-aware-agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:
   ```bash
   python app.py
   ```

2. The API will be available at `http://localhost:5000`

## API Endpoints

- `POST /analyze` - Analyze text for emotion detection

## Project Structure

- `app.py` - Main application file
- `requirements.txt` - Project dependencies
- `README.md` - This file

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
