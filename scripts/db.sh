#!/bin/bash

# Function to display usage
function show_usage {
    echo "Usage: $0 [command]"
    echo "Commands:"
    echo "  init      - Initialize the database and run migrations"
    echo "  migrate   - Run database migrations"
    echo "  upgrade   - Upgrade database to latest version"
    echo "  downgrade - Downgrade database by one version"
    echo "  reset     - Reset the database (drop all tables and recreate)"
}

# Check if command is provided
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

# Execute command
case "$1" in
    init)
        echo "Initializing database..."
        poetry run alembic upgrade head
        ;;
    migrate)
        echo "Creating new migration..."
        poetry run alembic revision --autogenerate -m "$2"
        ;;
    upgrade)
        echo "Upgrading database..."
        poetry run alembic upgrade head
        ;;
    downgrade)
        echo "Downgrading database..."
        poetry run alembic downgrade -1
        ;;
    reset)
        echo "Resetting database..."
        poetry run alembic downgrade base
        poetry run alembic upgrade head
        ;;
    *)
        show_usage
        exit 1
        ;;
esac