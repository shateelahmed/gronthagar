# Gronthagar - The Digital Library

## Installation
`Git`, `Docker` and  `Docker Compose` are required to install and run this project. Please intall them if you don't have them already.
Steps:
1. Clone the repositrory using the following command `git clone https://github.com/shateelahmed/gronthagar.git`
2. Go inside the `gronthagar` directory and duplicate the `.env.example` file and rename it as `.env`
3. Fill out all the environment variablae to your liking
4. Inside the `gronthagar` directory, run `docker compose up -d --build` to build and run the project.
5. To run the database migrations, run the following command `docker exec -u www gronthagar-backend alembic upgrade head`
6. Visit `http://localhost:3000` to view the app.
6. Visit `http://localhost:8000/docs` and `http://localhost:8000/redoc` to view the API documentations.

## Testing
1. To run tests of the backend app, execute the following command `docker exec -u www gronthagar-backend pytest`