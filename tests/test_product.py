def test_create_product(client):
    response = client.post("/api/products/",json={
        "name":"苹果",
        "price":20,
        "description":"香甜可口",
        "category":"水果",
        "stock":20
    })
    assert response.status_code==201
    assert "name" in response.json()

def test_product_list(client):
    client.post("/api/products/", json={
        "name": "苹果",
        "price": 20,
        "description": "香甜可口",
        "category": "水果",
        "stock": 20
    })
    client.post("/api/products/", json={
        "name": "香蕉",
        "price": 25,
        "description": "口感软糯",
        "category": "水果",
        "stock": 10
    })
    response = client.get("/api/products/",params={"skip":0,"limit":10})
    assert response.status_code==200
    assert len(response.json()) == 2

def test_product_detail(client):
    create_resp = client.post(f"/api/products/",json={
        "name": "苹果",
        "price": 20,
        "description": "香甜可口",
        "category": "水果",
        "stock": 20
    })
    product_id = create_resp.json()["id"]
    response = client.get(f"/api/products/{product_id}")
    assert response.status_code==200
    assert "name" in response.json()
    assert "id" in response.json()

def test_update_product(client):
    create_resp = client.post(f"/api/products/", json={
        "name": "苹果",
        "price": 20,
        "description": "香甜可口",
        "category": "水果",
        "stock": 20
    })
    product_id = create_resp.json()["id"]
    response = client.put(f"/api/products/{product_id}",json={"name":"香蕉"})
    assert "name" in response.json()
    assert response.status_code==200
    assert response.json()["name"] == "香蕉"

def test_delete_product(client):
    create_resp = client.post(f"/api/products/", json={
        "name": "苹果",
        "price": 20,
        "description": "香甜可口",
        "category": "水果",
        "stock": 20
    })
    product_id = create_resp.json()["id"]
    client.delete(f"/api/products/{product_id}")
    response = client.get(f"/api/products/{product_id}")
    assert response.status_code==404
