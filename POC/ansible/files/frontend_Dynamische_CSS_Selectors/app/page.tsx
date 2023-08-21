import Shop from "./Shop";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

const fetchProducts = async (
  indexOfFirstArticle: number,
  indexOfLastArticle: number
) => {
  try {
    const response = await fetch(
      `${API_URL}/api/products?startIndex=${indexOfFirstArticle}&endIndex=${indexOfLastArticle}`,
      {
        headers: {
          Origin: "http://localhost:3001",
        },
      }
    );
    return await response.json();
  } catch (error) {
    console.error("Error fetching products:", error);
    return [];
  }
};

export default async function Home({
  searchParams,
}: {
  searchParams: { [key: string]: string | undefined };
}) {
  const { paginatedProducts, productsLength } = await getData(
    searchParams.page
  );

  if (searchParams.page == undefined) {
    searchParams.page = "1";
  }

  return (
    <Shop
      productsData={paginatedProducts}
      productsLength={productsLength}
      page={parseInt(searchParams.page)}
    />
  );
}

async function getData(page: string | undefined) {
  if (page == undefined) {
    return await fetchProducts(0, 9);
  } else {
    const indexOfFirstArticle = (parseInt(page) - 1) * 9;
    const indexOfLastArticle = parseInt(page) * 9;
    return await fetchProducts(indexOfFirstArticle, indexOfLastArticle);
  }
}
