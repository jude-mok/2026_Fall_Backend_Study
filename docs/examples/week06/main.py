from fastapi import FastAPI, HTTPException, Query

from database import connect_db

app = FastAPI(title='Week 06: Local PostgreSQL')


@app.get('/users')
def list_users(limit: int = Query(default=20, ge=1, le=100)):
    with connect_db() as conn:
        rows = conn.execute(
            'SELECT id, name, email FROM users ORDER BY id LIMIT %s',
            (limit,),
        ).fetchall()
    return {'items': rows}


@app.get('/users/{user_id}')
def get_user(user_id: int):
    with connect_db() as conn:
        user = conn.execute(
            'SELECT id, name, email FROM users WHERE id = %s',
            (user_id,),
        ).fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user
