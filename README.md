Run this to build the container:
- docker compose up --build

Run this to add "Hello" message to MySQL:
- curl -X POST http://localhost/submit -H "Content-Type: application/json" -d '{"value": "Hello"}'

