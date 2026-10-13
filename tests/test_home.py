def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/html")
    assert b"<h1>PEX" in response.content
    assert b"Expense tracking features are not implemented yet." in response.content
