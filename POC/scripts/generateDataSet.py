import random

num_products = 350  # Specify the number of products you want to generate

products = []
used_article_numbers = set()

for i in range(1, num_products + 1):
    rating = random.randint(1, 5)
    originalprice = random.choice([100, 150])
    artikelnummer = None
    while artikelnummer is None or artikelnummer in used_article_numbers:
        artikelnummer = random.randint(100000, 999999)

    used_article_numbers.add(artikelnummer)

    product = {
        "id": i,
        "title": f"Product {i}",
        "rating": rating,
        "description": f"Lorem ipsum dolor sit amet for Product {i}",
        "originalprice": originalprice,
        "price": 100,
        "image1": f"img/products/0{random.randint(1, 5)}.jpg",
        "image2": f"img/products/0{random.randint(1, 5)}.jpg",
        "image3": f"img/products/0{random.randint(1, 5)}.jpg",
        "image4": f"img/products/0{random.randint(1, 5)}.jpg",
        "image5": f"img/products/0{random.randint(1, 5)}.jpg",
        "artikelnummer": artikelnummer,
        "instock": True,
    }
    products.append(product)

with open("dummy-data.js", "w") as js_file:
    js_file.write("const products = ")
    js_file.write(str(products))
    js_file.write(";\n\nmodule.exports = products;\n")

print("Products data exported to products.js")