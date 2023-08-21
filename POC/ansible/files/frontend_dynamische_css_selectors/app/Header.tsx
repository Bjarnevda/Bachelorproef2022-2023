export default function Header() {
  return (
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
  );
}
