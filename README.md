# Technical Assignment

This project contains the solution for the technical assignment provided.

## Project Overview

Create a backend application that allows users to upload PDF documents and interact with an AI about the content of
those documents through API endpoints.

# Notes on the implementation

## About

This repository contains a Django(4) w/ DRF project that implements the backend for the REST API described in the
technical assignment.

The project is structured as follows:

- `djangopdfchat/` contains the Django project settings and configuration
- `api_v1/` contains the Django app that implements the API endpoints and some business logic
- `filehandler/` contains the business logic for handling the PDF file operations
- `gpt/` contains the business logic for interacting with the OpenAI API
- `tests/` contains the tests for the API endpoints and the business logic
- `uploads/` is the directory where the uploaded PDF files are stored (only visible after uploading a first file)

I decided to implement the important CRUD operations for the documents (upload, list, retrieve, delete) and also the
interaction with the AI through the chat endpoint. I also added some tests to cover the API endpoints and the business
logic.

Among design decisions and specifically tradeoffs:

- the AI interaction always sends the entire document content to the OpenAI API, which can be a problem for large
  documents
- the AI interaction is a simple request/response cycle, which can be improved by streaming the messages back and forth
- the AI interaction does not use embeddings for the document content and the input message, which could improve the
  AI's
  responses and the RAG process
- the file deletion logic is very simple and does not ensure that the files are properly deleted from the storage and
  the
  database
- the tests do not cover all edge cases and possible errors

## Setup

The easiest way to run the project is to use the provided Dockerfile and docker-compose.yml files.
To do so, you need to have Docker and docker-compose installed on your machine.

First, use the `.env.template` file to create a `.env.dev` file with the necessary environment variables.
Fill in the appropriate values. The created file will then be used by the Docker Compose file to set the environment.

To run the project, execute the following command:

```bash
docker-compose up -d
```

This will build the Docker images for both a PostgreSQL database and the Django application, start the containers and
also add a test user to the database.

## API Endpoints

All API endpoints built for this project require a valid JWT token to be passed in the `Authorization` header of the
request, like so:

```http
Authorization: JWT <JWT token>
```

To obtain a JWT token, you can use the following endpoint:

- [POST] `/auth/jwt/create`: used to authenticate a user and obtain a JWT token
    - For this exercise, you can use the following credentials from the initial data:
        - username: `django`
        - password: `testing123`

All API endpoints built for this project are available under the `/api/v1/` URL prefix. They are:

- [GET] `documents/`: used to list all the documents uploaded by the authenticated user
- [POST] `documents/`: used to upload a new PDF document
    - the request body needs to be a `multipart/form-data` and contain the PDF file to be uploaded under `file`
- [GET] `documents/<document_id>/`: used to retrieve the metadata of a specific document
    - the document ID is a UUID that identifies the document
    - the document must have been uploaded by the authenticated user
- [DELETE] `documents/<document_id>/`: used to delete a specific document
    - the document ID is a UUID that identifies the document
    - the document must have been uploaded by the authenticated user
- [POST] `documents/<document_id>/chat/`: used to interact with the AI about the content of a specific document
    - the document ID is a UUID that identifies the document
    - the document must have been uploaded by the authenticated user
    - the request body needs to be a JSON object with the following structure:
        ```json
        {
            "input": "Hello, AI!"
        }
        ```
    - the `input` key is required and should contain the message to be sent to the AI
    - the AI will respond with a message based on the content of the document and the input message

Please refer to the OpenAPI documentation file `schema.yml` for an even more detailed description of the available
endpoints.

## Tests

The project contains a set of tests for the API endpoints and the business logic. To run the tests, you can use the
following command:

```bash
pytest
```

This will run the tests and display the results in the terminal. Make sure to have a `.env` file with the necessary
environment variables set up before running the tests, as well as have a running PostgreSQL database that the tests can
connect to.

You may also want to run PyLint to check the code quality. To do so, you can use the following command:

```bash
pylint api_v1 filehandler gpt
```

## Further improvements

Given the time constraints, there are some improvements that could/should be made to the project:

- Add more error handling and validation to the API endpoints, as well as to the business logic (e.g. more granular
  exceptions, better error messages)
- Add more tests to cover the API endpoints and the business logic, also looking for edge cases and possible errors
- Add pagination to the `documents/` endpoint to avoid performance issues with a large number of documents
- Add better file deletion logic, to ensure that the files are properly deleted from the storage and the database (i.e.
  no orphaned files)
- Add better interaction with the OpenAI API, such as:
    - streaming the messages back and forth (not have a single request/response cycle)
    - create embeddings for the document content and the input message to improve the AI's responses and the RAG process
- Allow more file types to be uploaded, not only PDFs
- Add a rate limiter to prevent abuse of the API
- Add a cache layer to improve the performance of the API
- Add an external file storage solution such as AWS S3 or Google Cloud Storage to store the uploaded PDF files
- Implement a robust logging system to track errors and monitor the application
    - Use tools like Prometheus and Grafana to monitor the application, and Sentry to track errors
- Add a CI/CD pipeline to automate the testing and deployment processes

And the list could go on... :)
