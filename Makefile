# Brent Oil Price Analysis - Makefile

.PHONY: help install setup run-backend run-frontend run-all clean test

help:
	@echo "Brent Oil Price Analysis - Available Commands:"
	@echo ""
	@echo "Setup Commands:"
	@echo "  install     - Install all dependencies"
	@echo "  setup       - Setup the project (install + data preparation)"
	@echo ""
	@echo "Run Commands:"
	@echo "  run-backend - Start the Flask backend server"
	@echo "  run-frontend- Start the React frontend development server"
	@echo "  run-all     - Start both backend and frontend"
	@echo ""
	@echo "Analysis Commands:"
	@echo "  notebooks   - Run Jupyter notebooks for analysis"
	@echo "  test        - Run tests"
	@echo ""
	@echo "Utility Commands:"
	@echo "  clean       - Clean generated files"
	@echo "  help        - Show this help message"

install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "Installing backend dependencies..."
	cd src/backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd src/frontend/oil-price-dashboard && npm install
	@echo "Installation complete!"

setup: install
	@echo "Setting up the project..."
	@echo "Creating output directories..."
	mkdir -p data/outputs
	mkdir -p data/processed
	@echo "Setup complete! Run 'make run-all' to start the application."

run-backend:
	@echo "Starting Flask backend server..."
	cd src/backend && python app.py

run-frontend:
	@echo "Starting React frontend development server..."
	cd src/frontend/oil-price-dashboard && npm start

run-all:
	@echo "Starting both backend and frontend..."
	@echo "Backend will be available at: http://localhost:5000"
	@echo "Frontend will be available at: http://localhost:3000"
	@echo ""
	@echo "Starting backend in background..."
	cd src/backend && python app.py &
	@echo "Starting frontend..."
	cd src/frontend/oil-price-dashboard && npm start

notebooks:
	@echo "Running Jupyter notebooks..."
	jupyter notebook notebooks/

test:
	@echo "Running tests..."
	python -m pytest src/analysis/tests/ -v
	python -m pytest src/backend/tests/ -v

clean:
	@echo "Cleaning generated files..."
	rm -rf data/outputs/*
	rm -rf data/processed/*
	rm -rf src/frontend/oil-price-dashboard/build
	rm -rf src/frontend/oil-price-dashboard/node_modules
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "Cleanup complete!"

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker build -t brent-oil-analysis .

docker-run:
	@echo "Running Docker container..."
	docker-compose up

# Development commands
dev-setup: setup
	@echo "Development setup complete!"
	@echo "To start development:"
	@echo "  1. Terminal 1: make run-backend"
	@echo "  2. Terminal 2: make run-frontend"
	@echo "  3. Open http://localhost:3000 in your browser"

# Analysis commands
run-analysis:
	@echo "Running complete analysis pipeline..."
	python run_analysis.py

# Quick start for users
quick-start: setup
	@echo "Quick start guide:"
	@echo "1. Backend is starting at http://localhost:5000"
	@echo "2. Frontend is starting at http://localhost:3000"
	@echo "3. Wait for both servers to start, then open http://localhost:3000"
	@echo ""
	@echo "Starting servers..."
	$(MAKE) run-all