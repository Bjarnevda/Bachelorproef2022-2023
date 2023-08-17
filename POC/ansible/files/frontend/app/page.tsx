import Shop from "./Shop";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

const fetchProductsInitially = async () => {
  try {
    const response = await fetch(
      `${API_URL}/api/products?startIndex=0&endIndex=9`,
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
