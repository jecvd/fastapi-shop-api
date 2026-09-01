def test_register_success(client):
    response = client.post("/api/users/register",json={
        "username":"newuser",
        "email":"new@test.com",
        "password":"123456"
    })
    assert response.status_code==201
    assert response.json()["username"] == "newuser"

def test_register_duplicate(client):
    data = {"username":"newuser","email":"new@test.com","password":"123456"}
    client.post("/api/users/register",json = data)
    response = client.post("/api/users/register",json = data)
    assert response.status_code == 400

def test_login_success(client):
    client.post("/api/users/register", json={
        "username": "loginuser", "email": "l@t.com", "password": "123456"
    })
    response = client.post("/api/users/login", json={
        "username": "loginuser","password": "123456"
    })
    assert response.status_code==200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    client.post("/api/users/register",json={"username": "wp", "email": "wp@t.com", "password": "123456"})
    response = client.post("/api/users/login",json={"username": "wp", "password": "wrong"})
    assert response.status_code == 400
