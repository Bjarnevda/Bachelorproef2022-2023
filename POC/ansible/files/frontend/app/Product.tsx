"use client";
import React, { useState, useEffect, useRef } from "react";

interface StarRatingProps {
  numStars: number;
}

const StarRating: React.FC<StarRatingProps> = ({ numStars }) => {
  const starIcons = [];
  for (let i = 1; i <= 5; i++) {
    const isFilled = i <= numStars;

    const starClass = isFilled ? "material-icons" : "material-icons off";

    starIcons.push(
      <span className="fa fa-stack" key={i}>
        <i className={starClass}>star</i>
      </span>
    );
  }

  return (
    <div className="product-ratings d-inline-block align-middle">
      {starIcons}
    </div>
  );
};

export interface ProductItemProps {
  id: number;
  title: string;
  rating: number;
  price: number;
  originalprice: number;
  description: string;
  image1: string;
  image2: string;
  image3: string;
  image4: string;
  image5: string;
  artikelnummer: number;
  instock: boolean;
}

interface ProductModalProps {
  piprops: ProductItemProps;
  onClose: React.MouseEventHandler<HTMLButtonElement>; // Callback to close the modal
}

const ProductModal: React.FC<ProductModalProps> = ({ piprops, onClose }) => {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleBackdropClick = (event: MouseEvent) => {
      if (
        modalRef.current &&
        !modalRef.current.contains(event.target as Node)
      ) {
        const dummyEvent: Partial<React.MouseEvent<HTMLButtonElement>> = {
          currentTarget: document.createElement("button"), // A dummy target element
          target: document.createElement("button"), // A dummy target element
          preventDefault: () => { }, // A dummy preventDefault function
          stopPropagation: () => { }, // A dummy stopPropagation function
          nativeEvent: new MouseEvent("click"), // A dummy native event
          relatedTarget: null,
        };
        onClose(dummyEvent as React.MouseEvent<HTMLButtonElement>);
      }
    };

    document.addEventListener("click", handleBackdropClick);

    // Callback function to initialize the carousel
    function initCarousel() {
      $(".owl-carousel").owlCarousel({
        // Add your carousel options here
        loop: false,
        items: 3,
        nav: true,
        dots: false,
      });
    }

    // Check if the owl.carousel script is loaded
    if (typeof $.fn.owlCarousel === "function") {
      // If loaded, initialize the carousel
      initCarousel();
    } else {
      // If not loaded, wait for the script to load
      $(document).on("owlCarouselLoaded", initCarousel);
    }

    // Clean up event listeners when the component unmounts
    return () => {
      document.removeEventListener("click", handleBackdropClick);
      $(document).off("owlCarouselLoaded", initCarousel);
    };
  }, []);

  return (
    <div
      className="modal fade product_view"
      id="product_view"
      tabIndex={-1}
      role="dialog"
      aria-hidden="false"
    >
      <div className="modal-dialog">
        <div className="modal-content" ref={modalRef}>
          <div className="modal-header">
            <h4 className="modal-title w-100w-100w-100 font-weight-bold d-none">
              Quick view
            </h4>
            <button
              type="button"
              className="close"
              data-dismiss="modal"
              aria-label="Close"
              onClick={onClose}
            >
              <span aria-hidden="false">×</span>
            </button>
          </div>
          <div className="modal-body">
            <div className="row">
              <div className="col-md-6 left-columm">
                <div className="product-large-image tab-content">
                  <div
                    className="tab-pane active"
                    id="product-1"
                    role="tabpanel"
                    aria-labelledby="product-tab-1"
                  >
                    <div className="single-img img-full">
                      <img src={piprops.image1} className="img-fluid" alt="" />
                    </div>
                  </div>
                  <div
                    className="tab-pane"
                    id="product-2"
                    role="tabpanel"
                    aria-labelledby="product-tab-2"
                  >
                    <div className="single-img">
                      <img src={piprops.image2} className="img-fluid" alt="" />
                    </div>
                  </div>
                  <div
                    className="tab-pane"
                    id="product-3"
                    role="tabpanel"
                    aria-labelledby="product-tab-3"
                  >
                    <div className="single-img">
                      <img src={piprops.image3} className="img-fluid" alt="" />
                    </div>
                  </div>
                  <div
                    className="tab-pane"
                    id="product-4"
                    role="tabpanel"
                    aria-labelledby="product-tab-4"
                  >
                    <div className="single-img">
                      <a href={piprops.image4}>
                        <img
                          src={piprops.image4}
                          className="img-fluid"
                          alt=""
                        />
                      </a>
                    </div>
                  </div>
                  <div
                    className="tab-pane"
                    id="product-5"
                    role="tabpanel"
                    aria-labelledby="product-tab-5"
                  >
                    <div className="single-img">
                      <a href={piprops.image5}>
                        <img
                          src={piprops.image5}
                          className="img-fluid"
                          alt=""
                        />
                      </a>
                    </div>
                  </div>
                </div>
                <div className="small-image-list float-left w-100">
                  <div
                    className="nav-add small-image-slider-single-product-tabstyle-3 owl-carousel"
                    role="tablist"
                  >
                    <div className="single-small-image img-full">
                      <a
                        data-toggle="tab"
                        id="product-tab-1"
                        href="#product-1"
                        className="img active"
                      >
                        <img
                          src={piprops.image1}
                          className="img-fluid"
                          alt=""
                        />
                      </a>
                    </div>
                    <div className="single-small-image img-full">
                      <a
                        data-toggle="tab"
                        id="product-tab-2"
                        href="#product-2"
                        className="img"
                      >
                        <img
                          src={piprops.image2}
                          className="img-fluid"
                          alt=""
                        />
                      </a>
                    </div>
                    <div className="single-small-image img-full">
                      <a
                        data-toggle="tab"
                        id="product-tab-3"
                        href="#product-3"
                        className="img"
                      >
                        <img
                          src={piprops.image3}
                          className="img-fluid"
                          alt=""
                        />
                      </a>
                    </div>
                    <div className="single-small-image img-full">
                      <a
                        data-toggle="tab"
                        id="product-tab-4"
                        href="#product-4"
                        className="img"
                      >
                        <img
                          src={piprops.image4}
                          className="img-fluid"
                          alt=""
                        />
                      </a>
                    </div>
                    <div className="single-small-image img-full">
                      <a
                        data-toggle="tab"
                        id="product-tab-5"
                        href="#product-5"
                        className="img"
                      >
                        <img
                          src={piprops.image5}
                          className="img-fluid"
                          alt=""
                        />
                      </a>
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-md-6 product_content">
                <h4 className="product-title text-capitalize">
                  {piprops.title}
                </h4>
                <div className="rating">
                  <StarRating numStars={piprops.rating} />
                </div>
                <span className="description float-left w-100">
                  {piprops.description}
                </span>
                <span
                  className="article-number float-left w-100"
                  style={{ marginBottom: "3%" }}
                >
                  Article number: <b>{piprops.artikelnummer}</b>
                </span>

                <h3 className="price float-left w-100">
                  {piprops.originalprice !== piprops.price ? (
                    <>
                      <div className="regular-price align-middle">
                        ${piprops.price.toFixed(2)}
                      </div>
                      <div className="old-price align-middle">
                        ${piprops.originalprice.toFixed(2)}
                      </div>
                    </>
                  ) : (
                    <div className="regular-price align-middle">
                      ${piprops.price.toFixed(2)}
                    </div>
                  )}
                </h3>

                <div className="btn-cart d-flex align-items-center float-left w-100">
                  <h5>qty:</h5>
                  <input type="number" />
                  {piprops.instock ? (
                    <>
                      <button
                        type="button"
                        className="btn btn-primary btn-cart"
                        disabled={false}
                      >
                        <i className="material-icons">shopping_cart</i>
                        <span>Add To Cart</span>
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        type="button"
                        className="btn btn-primary btn-cart"
                        disabled={true}
                      >
                        <i className="material-icons">shopping_cart</i>
                        <span>Out Of Stock</span>
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const Product: React.FC<ProductItemProps> = (props) => {
  const [isModalVisible, setModalVisible] = useState(false);
  const [productData, setProductData] = useState(null);

  useEffect(() => {
    if (isModalVisible) {
      $("#product_view").modal("show");
    }
  }, [isModalVisible]);

  // Function to hide the modal
  const hideModal: React.MouseEventHandler<HTMLButtonElement> = () => {
    setModalVisible(false);
  };

  const showModal = async () => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/products/${props.id}`
      ); // Assuming you have an API endpoint for fetching product details
      const data = await response.json();
      setProductData(data);
      setModalVisible(true);
    } catch (error) {
      console.error("Error fetching product data:", error);
    }
  };

  const renderModal = () => {
    if (!productData) {
      return null; // Return null if data is not available yet
    }

    return <ProductModal onClose={hideModal} piprops={productData} />;
  };

  return (
    <div className="product-layouts">
      <div className="product-thumb row">
        <div className="image zoom col-xs-12 col-sm-3 col-md-2">
          <a href="#" className="d-block position-relative" onClick={showModal}>
            <img src={props.image1} alt="01" />
            <img
              src={props.image2}
              alt="02"
              className="second_image img-responsive"
            />
          </a>
        </div>
        <div className="thumb-description col-xs-12 col-sm-9 col-md-10 position-static text-left">
          <div className="sort-title col-md-5 col-sm-7 float-left">
            <div className="caption">
              <h4 className="product-title text-capitalize">
                <a
                  href="#"
                  className="d-block position-relative"
                  data-toggle="modal"
                  data-target="#product_view"
                >
                  {props.title}
                </a>
              </h4>
            </div>

            <div className="rating mb-10">
              <StarRating numStars={props.rating} />
            </div>
            <div className="description mb-10">{props.description}</div>
          </div>
          <div className="price-main col-md-3 col-sm-5 float-left text-center text-sm-center text-xs-left">
            <div className="price">
              {props.originalprice !== props.price ? (
                <>
                  <div className="regular-price">${props.price.toFixed(2)}</div>
                  <div className="old-price">
                    ${props.originalprice.toFixed(2)}
                  </div>
                </>
              ) : (
                <div className="regular-price">${props.price.toFixed(2)}</div>
              )}
            </div>
          </div>
          <div className="button-wrapper col-md-4 col-sm-5 float-left text-center text-md-center text-sm-center text-xs-left">
            <div className="button-group text-center">
              {props.instock ? (
                <>
                  <button
                    type="button"
                    className="btn btn-primary btn-cart"
                    data-target="#cart-pop"
                    data-toggle="modal"
                    disabled={false}
                  >
                    <i className="material-icons">shopping_cart</i>
                    <span>Add To Cart</span>
                  </button>
                </>
              ) : (
                <>
                  <button
                    type="button"
                    className="btn btn-primary btn-cart"
                    data-target="#cart-pop"
                    data-toggle="modal"
                    disabled={true}
                  >
                    <i className="material-icons">shopping_cart</i>
                    <span>Out Of Stock</span>
                  </button>
                </>
              )}
              <button
                type="button"
                className="btn btn-primary btn-quickview"
                data-toggle="modal"
                data-target="#product_view"
              >
                <i className="material-icons">visibility</i>
                <span>Quick View</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {isModalVisible && renderModal()}
    </div>
  );
};

interface ProductListProps {
  products: ProductItemProps[];
}

const ProductList: React.FC<ProductListProps> = ({ products }) => {
  return (
    <div>
      {products.map((product) => (
        <Product
          key={product.id}
          id={product.id}
          title={product.title}
          description={product.description}
          image1={product.image1}
          image2={product.image2}
          image3={product.image3}
          image4={product.image4}
          image5={product.image5}
          originalprice={product.originalprice}
          artikelnummer={product.artikelnummer}
          price={product.price}
          rating={product.rating}
          instock={product.instock}
        />
      ))}
    </div>
  );
};

export default ProductList;