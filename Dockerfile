FROM python:3.12-slim-bookworm as base

# Install system dependencies
RUN apt update && apt install -y --no-install-recommends gcc libpq-dev postgresql-client poppler-utils

# Set the virtual environment location
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"


FROM base as builder

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Install the application dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR


FROM base as runtime

# Create directory for the app user
RUN mkdir -p /home/app

# Create the app user
RUN addgroup --system app && adduser --system --group app

# Create the appropriate directories for the application
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Copy the virtual environment
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy the project resources
COPY . $APP_HOME

# Configure the entrypoint file
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# Set ownership to the app user
RUN chown -R app:app $APP_HOME

# Switch to the app user
USER app

# Run the application
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
