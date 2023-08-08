import Shop from "./Shop";

const fetchProductsInitially = async () => {
  try {
    const response = await fetch(
      'http://localhost:5000/api/products?startIndex=0&endIndex=9',
      {
        headers: {
          Origin: "http://localhost:3000",
        },
      }
    );
    return await response.json();
  } catch (error) {
    console.error("Error fetching products:", error);
    return [];
  }
};

export default async function Home() {
  const {
    paginatedProducts,
    productsLength,
  } = await getData();

  return (
    <Shop
      productsData={paginatedProducts}
      productsLength={productsLength}
    />
  );
}

async function getData() {
  return await fetchProductsInitially();
}
