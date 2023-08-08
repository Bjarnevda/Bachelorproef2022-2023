import Shop, { ShopProps } from "./Shop";

const fetchProductsInitially = async () => {
  try {
    const response = await fetch(
      `http://localhost:5000/api/products?startIndex=${0}&endIndex=${9}`,
      {
        headers: {
          Origin: "http://localhost:3000",
        },
      }
    );
    const data = await response.json();

    return data;
  } catch (error) {
    console.error("Error fetching products:", error);
    return [];
  }
};

export default async function Home() {
  const shopData = await getData();
  const { paginatedProducts, productsLength } = shopData;

  return (
    <Shop productsData={paginatedProducts} productsLength={productsLength} />
  );
}

async function getData() {
  const res = await fetchProductsInitially();

  return res;
}
