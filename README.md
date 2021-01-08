# flask
start: pythom -m app.main


# migration db
python -m  app.manage db migrate
python -m app.manage db upgrade