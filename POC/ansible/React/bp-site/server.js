const express = require("express");
const next = require("next");
const app = express();

const products = require("./dummyData");

const customCors = (req, res, next) => {
  const allowedOrigin = "http://localhost:3000";

  const origin = req.headers.origin;

  if (origin === allowedOrigin) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
    res.setHeader(
      "Access-Control-Allow-Headers",
      "Content-Type, Authorization"
    );
    next();
  } else {
    console.log(res.origin);
    res.status(403).json({ message: "Access Forbidden" });
  }
};

app.use(customCors);

app.get("/api/products/:productId", (req, res) => {
  const productId = parseInt(req.params.productId);
  const product = products.find((product) => product.id === productId);
  if (product) {
    res.json(product);
  } else {
    res.status(404).json({ error: "Product not found" });
  }
});

app.get("/api/products/:page", (req, res) => {
  const page = parseInt(req.params.page);
  const startIndex = parseInt(req.query.startIndex);
  const endIndex = parseInt(req.query.endIndex);
  const paginatedProducts = products.slice(startIndex, endIndex);
  const productsLength = products.length;
  const response = {
    paginatedProducts,
    productsLength,
  };

  console.log(res.origin);

  res.json(response);
});

const port = 5000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
