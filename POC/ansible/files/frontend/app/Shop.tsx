"use client";
import Paginate from "./Paginate";
import ProductList, { ProductItemProps } from "./Product";
import React, { useState, useEffect, useCallback } from "react";

export interface ShopProps {
  productsData: ProductItemProps[];
  productsLength: number;
}

export default function Shop(shopData: ShopProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const [totalArticles, setTotalArticles] = useState(shopData.productsLength);
  const [articlesPerPage, setArticlesPerPage] = useState(9);
  const [indexOfLastArticle, setIndexOfLastArticle] = useState(
    currentPage * articlesPerPage
  );

  const [products, setProducts] = useState(shopData.productsData);

  const [indexOfFirstArticle, setindexOfFirstArticle] = useState(
    indexOfLastArticle - articlesPerPage
  );

  const fetchProducts = useCallback(async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"}/api/products?startIndex=${indexOfFirstArticle}&endIndex=${indexOfLastArticle}`
      );
      const data = await response.json();

      setProducts(data.paginatedProducts); // Assuming the API returns an array of products
      setTotalArticles(data.productsLength);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  }, [indexOfFirstArticle, indexOfLastArticle]);

  const initialShowArrowUp =
    typeof localStorage !== "undefined"
      ? localStorage.getItem("showArrowUp") || "false"
      : "false"; // Provide a default value here

  const [showArrowUp, setShowArrowUp] = useState(initialShowArrowUp === "true");



  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY >= 200) {
        setShowArrowUp(true);
      } else {
        setShowArrowUp(false);
      }
    };

    // Add scroll event listener when the component mounts
    window.addEventListener("scroll", handleScroll);

    // Remove scroll event listener when the component unmounts
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  useEffect(() => {
    // Save the state to local storage whenever it changes
    localStorage.setItem("showArrowUp", JSON.stringify(showArrowUp));
  }, [showArrowUp]);


  const paginate = (pageNumber: number) => {
    if (
      pageNumber < 1 ||
      pageNumber > Math.ceil(totalArticles / articlesPerPage)
    )
      return;

    if (pageNumber * articlesPerPage > totalArticles)
      setIndexOfLastArticle(totalArticles);
    else setIndexOfLastArticle(pageNumber * articlesPerPage);

    if (pageNumber * articlesPerPage - articlesPerPage < 0)
      setindexOfFirstArticle(1);
    else setindexOfFirstArticle(pageNumber * articlesPerPage - articlesPerPage);

    setCurrentPage(pageNumber);
  };

  return (
    <div id="category" className="category">
      <header className="header-area header-sticky text-center header-default">
        <div className="header-main-stick fixed-header">
          <div className="header-nav">
            <div className="container ">
              <div className="nav-left float-center">
                <div className="ttheader-service">
                  NOT A REAL STORE - DEMO FOR RESEARCH PURPOSES AND HAS NO
                  FUNCTIONALITY
                </div>
              </div>
            </div>
          </div>
          <div className="header-main-head">
            <div className="header-main">
              <div className="container">
                <div className="header-left float-left d-flex d-lg-flex d-md-block d-xs-block">
                  <div className="language-wrapper toggle">
                    <button
                      type="button"
                      className="btn text-capitalize dropdown-toggle"
                    >
                      <img
                        src="img/banner/en.png"
                        alt="en"
                        style={{ display: "inline" }}
                      />
                      <span>English</span>
                    </button>
                    <div id="language-dropdown" className="language">
                      <ul>
                        <li>
                          <img src="img/banner/en.png" alt="en" />
                          <span>English</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
                <div className="header-middle float-left">
                  <div className="logo">
                    <a href="index.html">
                      <img src="img/logos/logo.png" alt="NatureCircle" />
                    </a>
                  </div>
                </div>
                <div className="header-right d-flex d-xs-block d-sm-flex justify-content-end float-right">
                  <div className="cart-wrapper">
                    <button type="button" className="btn">
                      <i className="material-icons">shopping_cart</i>
                      <span className="ttcount">0</span>
                    </button>
                    <div id="cart-dropdown" className="cart-menu">
                      <ul className="w-100 float-left">
                        <li>
                          <table className="table table-striped">
                            <tbody></tbody>
                          </table>
                        </li>
                        <li>
                          <table className="table price mb-30">
                            <tbody>
                              <tr>
                                <td className="text-left">
                                  <strong>Total</strong>
                                </td>
                                <td className="text-right">
                                  <strong>$0</strong>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </li>
                        <li className="buttons w-100 float-left">
                          <form action="cart_page.html">
                            <input
                              className="btn pull-left mt_10 btn-primary btn-rounded w-100"
                              type="submit"
                            />
                          </form>
                          <form action="checkout_page.html">
                            <input
                              className="btn pull-right mt_10 btn-primary btn-rounded w-100"
                              type="submit"
                            />
                          </form>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* main */}

      <div className="main-content w-100 float-left">
        <div className="container">
          <div className="row">
            <div
              className="content-wrapper col-xl-9 col-lg-9 order-lg-2 Cwidth"
              style={{
                position: "relative",
                overflow: "visible",
                boxSizing: "border-box",
                minHeight: "1px",
                width: "75%",
              }}
            >
              <div className="block-category mb-30 w-100 float-right">
                <div className="category-cover">
                  <img
                    src="/img/banner/category-banner.png"
                    alt="category-banner"
                  />
                </div>
              </div>
              <header className="product-grid-header d-flex d-xs-block d-sm-flex d-lg-flex w-100 float-left">
                <div className="shop-results-wrapper d-flex d-sm-flex d-xs-block d-lg-flex justify-content-end col-md-9 col-sm-9 col-xs-12">
                  <div className="shop-results d-flex align-items-center">
                    <span>Show</span>
                    <div className="shop-select">
                      <select
                        name="number"
                        id="number"
                        onChange={(val) =>
                          setArticlesPerPage(parseInt(val.target.value))
                        }
                      >
                        <option value="9">9</option>
                        <option value="25">25</option>
                        <option value="50">50</option>
                        <option value="75">75</option>
                        <option value="100">100</option>
                      </select>
                    </div>
                  </div>
                </div>
              </header>
              <div className="tab-content text-center products w-100 float-left">
                <div
                  className="tab-pane fade sort text-left active"
                  id="sort-view"
                  role="tabpanel"
                >
                  {/* productList */}
                  <ProductList products={products} />
                </div>
              </div>
              <Paginate
                articlesPerPage={articlesPerPage}
                totalArticles={totalArticles}
                paginate={paginate}
                indexOfFirstArticle={indexOfFirstArticle}
                indexOfLastArticle={indexOfLastArticle}
                currentPage={currentPage}
              />
            </div>

            <div
              className="left-column sidebar col-xl-3 col-lg-3 order-lg-1 Lwidth"
              style={{ width: "25%" }}
            >
              <div className="sidebar-filter left-sidebar w-100 float-left">
                <div className="title">
                  <a
                    data-toggle="collapse"
                    href="#sidebar-main"
                    aria-expanded="false"
                    aria-controls="sidebar-main"
                    className="d-lg-none block-toggler"
                  >
                    Product Categories
                  </a>
                </div>
                <div id="sidebar-main" className="sidebar-main collapse">
                  <div className="sidebar-block categories">
                    <h3 className="widget-title">
                      <a
                        data-toggle="collapse"
                        href="#categoriesMenu"
                        role="button"
                        aria-expanded="true"
                        aria-controls="categoriesMenu"
                      >
                        Categories
                      </a>
                    </h3>
                    <div
                      id="categoriesMenu"
                      className="expand-lg collapse show"
                    >
                      <div className="nav nav-pills flex-column mt-4">
                        {" "}
                        <a
                          href="#"
                          className="nav-link d-flex justify-content-between mb-2 "
                        >
                          <span>Jackets</span>
                          <span className="sidebar-badge"> 120</span>
                        </a>
                        <div className="nav nav-pills flex-column ml-3">
                          <a href="#" className="nav-link mb-2">
                            Lorem ipsum
                          </a>
                          <a href="#" className="nav-link mb-2">
                            Donec vitae
                          </a>
                        </div>
                        <a
                          href="#"
                          className="nav-link d-flex justify-content-between mb-2 active"
                        >
                          <span>Jeans &amp; chinos</span>
                          <span className="sidebar-badge"> 55</span>
                        </a>
                        <div className="nav nav-pills flex-column ml-3">
                          <a href="#" className="nav-link mb-2">
                            Dolor
                          </a>
                          <a href="#" className="nav-link mb-2">
                            Sit amet
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="sidebar-block price">
                    <h3 className="widget-title">
                      <a
                        data-toggle="collapse"
                        href="#price"
                        role="button"
                        aria-expanded="true"
                        aria-controls="price"
                      >
                        Price
                      </a>
                    </h3>
                    <div id="price" className="collapse show">
                      <div className="price-inner">
                        <label>Price range:</label>
                        <input
                          type="text"
                          id="amount"
                          style={{
                            border: 0,
                            fontWeight: "bold",
                            background: "none",
                          }}
                        />
                        <div id="slider-range"></div>
                      </div>
                    </div>
                  </div>
                  <div className="sidebar-block color">
                    <h3 className="widget-title">
                      <a
                        data-toggle="collapse"
                        href="#color"
                        role="button"
                        aria-expanded="true"
                        aria-controls="color"
                      >
                        Color
                      </a>
                    </h3>
                    <div
                      id="color"
                      className="sidebar-widget-option-wrapper collapse show"
                    >
                      <div className="color-inner">
                        <div className="sidebar-widget-option">
                          <a
                            href="#"
                            style={{ backgroundColor: "#000000" }}
                          ></a>
                          Black <span>(4)</span>
                        </div>
                        <div className="sidebar-widget-option">
                          <a
                            href="#"
                            style={{ backgroundColor: "#11426b" }}
                          ></a>
                          Blue <span>(3)</span>
                        </div>
                        <div className="sidebar-widget-option">
                          <a
                            href="#"
                            style={{ backgroundColor: "#7d5a3c" }}
                          ></a>
                          Brown <span>(3)</span>
                        </div>
                        <div className="sidebar-widget-option">
                          <a
                            href="#"
                            style={{ backgroundColor: "#ffffff" }}
                          ></a>
                          White <span>(3)</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="sidebar-block size">
                    <h3 className="widget-title">
                      <a
                        data-toggle="collapse"
                        href="#size"
                        role="button"
                        aria-expanded="true"
                        aria-controls="size"
                      >
                        Size
                      </a>
                    </h3>
                    <div
                      id="size"
                      className="sidebar-widget-option-wrapper collapse show"
                    >
                      <div className="size-inner">
                        <div className="sidebar-widget-option">
                          <input type="checkbox" id="size-1" />
                          <label htmlFor="size-1">
                            L <span>(4)</span>
                          </label>
                        </div>
                        <div className="sidebar-widget-option">
                          <input type="checkbox" id="size-2" />
                          <label htmlFor="size-2">
                            XS <span>(3)</span>
                          </label>
                        </div>
                        <div className="sidebar-widget-option">
                          <input type="checkbox" id="size-3" />
                          <label htmlFor="size-3">
                            S <span>(3)</span>
                          </label>
                        </div>
                        <div className="sidebar-widget-option">
                          <input type="checkbox" id="size-4" />
                          <label htmlFor="size-4">
                            Xl <span>(3)</span>
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="sidebar-left-banner left-sidebar w-100 float-left">
                <div className="ttleftbanner">
                  <a href="#">
                    <img src="img/banner/left-banner.jpg" alt="left-banner" />
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}

      <footer className="page-footer font-small footer-default">
        {/* Copyright */}
        <div className="footer-bottom-wrap">
          <div className="container">
            <div className="row">
              <div className="footer-copyright text-center py-3">
                © 2019 - Boostrap theme by store™
              </div>
            </div>
          </div>
        </div>
        <a
          href="#"
          id="goToTop"
          title="Back to top"
          className={`btn btn-primary${showArrowUp ? " show" : ""}`}
        >
          <i className="material-icons arrow-up">keyboard_arrow_up</i>
        </a>
      </footer>
    </div>
  );
}
