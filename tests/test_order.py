def test_create_order(client,auth_headers):
    product_resp = client.post("/api/products/",json = {"name":"苹果","price":20,"stock":10})
    product_id = product_resp.json()["id"]
    response = client.post("/api/orders/",json={"items": [{"product_id": product_id, "quantity": 2}]},headers=auth_headers)
    assert response.status_code==200
    assert "total_amount" in response.json()
    assert "product_id" in response.json()["items"][0]

def test_order_no_auth(client):
    product_resp = client.post("/api/products/", json={"name": "苹果", "price": 20, "stock": 10})
    product_id = product_resp.json()["id"]
    response = client.post("/api/orders/", json={"items": [{"product_id":product_id, "quantity": 2}]})
    assert response.status_code ==401

def test_order_insufficient_stock(client,auth_headers):
    product_resp = client.post("/api/products/", json={"name": "苹果", "price": 20, "stock": 5})
    product_id = product_resp.json()["id"]
    response = client.post("/api/orders/", json={"items": [{"product_id":product_id, "quantity": 100}]}, headers=auth_headers)
    assert response.status_code==409
    assert "库存不足" in response.json()["detail"]

def test_order_list(client,auth_headers):
    product_resp = client.post("/api/products/", json={"name": "苹果", "price": 20, "stock": 10})
    product_id = product_resp.json()["id"]
    client.post("/api/orders/", json={"items": [{"product_id":product_id, "quantity": 2}]}, headers=auth_headers)
    response = client.get("/api/orders/",headers=auth_headers)
    assert response.status_code==200
    assert len(response.json()) == 1

def test_order_detail_other_user(client,auth_headers):
    product_resp = client.post("/api/products/", json={"name": "苹果", "price": 20, "stock": 10})
    product_id = product_resp.json()["id"]
    response01 = client.post("/api/orders/", json={"items": [{"product_id": product_id, "quantity": 2}]}, headers=auth_headers)
    order_id = response01.json()["id"]

    response02 = client.post("/api/users/register", json={
        "username": "newuser",
        "email": "new@test.com",
        "password": "123456"
    })
    response03 = client.post("/api/users/login", json={
        "username": "newuser",
        "password": "123456"
    })
    userb_token = response03.json()["access_token"]
    userb_headers = {"Authorization":f"Bearer {userb_token}"}
    response04 = client.get(f"/api/orders/{order_id}",headers=userb_headers)
    assert response04.status_code==403



