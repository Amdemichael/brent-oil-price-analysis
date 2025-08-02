.PHONY: all lint test run build

all: lint test run

lint:
    flake8 src/analysis src/backend --max-line-length=88
    cd src/frontend/oil-price-dashboard && npx eslint src --ext .js,.jsx

test:
    pytest src/analysis/tests src/backend/tests
    cd src/frontend/oil-price-dashboard && npm test

run:
    docker-compose up --build

build:
    docker-compose build