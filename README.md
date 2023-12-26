# Hospitality Services NLP Project

This project involves utilizing Natural Language Processing (NLP) techniques to query and analyze hospitality-related data using SPARQL (SPARQL Protocol and RDF Query Language) and Flask framework.

## Requirements

- Python 3.x
- Flask
- SPARQLWrapper
- rdflib
- nltk

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Access the application in your browser at `http://localhost:5000`.

3. Enter your queries in the provided form and submit to retrieve relevant information from the hospitality data.

## Project Structure

- `app.py`: Flask application handling NLP processing and SPARQL querying.
- `templates/index.html`: HTML form for user input.
- `templates/result.html`: Display of query results and NLP processing steps.

## Additional Notes

- Ensure the SPARQL endpoint URL (`http://localhost:3030/HospitalityProject/query`) in `app.py` matches your actual endpoint.
- Customize the HTML templates (`index.html` and `result.html`) and Python functions (`run_query`, NLP functions) to suit your specific use case or expand the functionality.
- Make sure to handle error cases and edge scenarios for robustness in a production environment.
