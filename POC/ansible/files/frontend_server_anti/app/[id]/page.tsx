import { ProductItem } from "../Product";
import Header from "../Header";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5002";

const fetchProduct = async (id: number) => {
  try {
    const response = await fetch(`${API_URL}/api/products/${id}`, {
      headers: {
        Origin: "http://localhost:3003",
      },
    }); // Assuming you have an API endpoint for fetching product details
    return response.json();
  } catch (error) {
    console.error("Error fetching product data:", error);
  }
};

export default async function ProductPage({
  params,
}: {
  params: { id: string };
}) {
  const id = parseInt(params.id.split("_")[1]);

  const productdata = await getData(id);

  console.log(productdata);

  return (
    <div>
      <Header></Header>
      <ProductItem piprops={productdata} />;
    </div>
  );
}

async function getData(id: number) {
  return await fetchProduct(id);
}
