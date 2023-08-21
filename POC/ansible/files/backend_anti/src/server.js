const express = require("express");
const app = express();
const rateLimit = require("express-rate-limit");
const products = require("./dummyData");

const fs = require("fs");
const suspiciousUserAgents = fs
  .readFileSync("bad-user-agents.txt")
  .toString()
  .split("\n");

const customCors = (req, res, next) => {
  const allowedOrigins = ["http://localhost:3003"];

  const origin = req.headers.origin;

  if (allowedOrigins.includes(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
    res.setHeader(
      "Access-Control-Allow-Headers",
      "Content-Type, Authorization"
    );
    next();
  } else {
    console.log(res.origin);
    res.status(403).json({ message: "Access Forbidden, try again later" });
  }
};

const limiter = rateLimit({
  windowMs: 1 * 10 * 1000, // 10 seconden
  max: 8, // Maximaal aantal verzoeken binnen het tijdsbestek
  message: "Access Forbidden, try again later",
});

const userAgentChecker = (req, res, next) => {
  const userAgent = req.headers["user-agent"];

  if (suspiciousUserAgents.includes(userAgent)) {
    res.status(403).json({ message: "Access Forbidden, try again later" });
  }

  next();
};

app.use(userAgentChecker);
app.use(customCors);
app.use(limiter);

app.get("/api/products/:productId", (req, res) => {
  const productId = parseInt(req.params.productId);
  const product = products.find((product) => product.id === productId);
  if (product) {
    res.json(product);
  } else {
    res.status(404).json({ error: "Product not found" });
  }
});

app.get("/api/products", (req, res) => {
  const startIndex = parseInt(req.query.startIndex);
  const endIndex = parseInt(req.query.endIndex);
  const paginatedProducts = products.slice(startIndex, endIndex);
  const productsLength = products.length;
  const response = {
    paginatedProducts,
    productsLength,
  };

  res.json(response);
});

const port = 5002;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
