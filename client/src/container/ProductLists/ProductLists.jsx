import React, { useState, useEffect, forwardRef } from 'react';
import './ProductLists.scss';

const ProductLists = forwardRef(({ medicineName: medName, products: initialProducts }, ref) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [recieved, setRecieved] = useState(false);
  const [medicineName, setMedicineName] = useState("");

  useEffect(() => {
    setProducts(initialProducts);
    setMedicineName(medName);
  }, [initialProducts, medName]);

  const [hoveredProductName, setHoveredProductName] = useState(null);

  const handleMouseEnter = (productName) => {
    setHoveredProductName(productName);
  };

  const handleMouseLeave = () => {
    setHoveredProductName(null);
  };

  const truncateProductName = (productName) => {
    const maxLength = 50;
    if (productName.length > maxLength) {
      return productName.substring(0, maxLength) + "...";
    }
    return productName;
  };

  const WebNames = {
    0: "PharmEasy",
    1: "NetMeds",
    2: "MedKart",
    3: "IndiaMart",
    4: "TATA 1mg",
  };

  return (
    <div ref={ref}>
      {(initialProducts.length > 0 || medicineName.length > 0) && (
        <div className="app__products">
          <React.Fragment>
            <h1 className="app__products-search-heading">
              results found for "<span>{medicineName}</span>"
            </h1>
            {Object.keys(products).map((scrapperKey) => (
              <div key={scrapperKey} className="app__products-container">
                <div className="web__heading">
                  <div className="line"></div>
                  <div className="parallogram">
                    <h2>{WebNames[scrapperKey]}</h2>
                  </div>
                </div>
                <ul>
                  <div className="app__products-list">
                    {products[scrapperKey].map((product, index) => (
                      <div className="app__products-item-card" key={index}>
                        <li>
                          <a href={product.link}>
                            <img src={product.img} alt="" />
                          </a>
                          <div className="product__name" title={product.name}>
                            <a href={product.link}>
                              {hoveredProductName === product.name
                                ? product.name
                                : truncateProductName(product.name)}
                            </a>
                          </div>
                          <div className="product__price">
                            {product.offer_price ? (
                              <>
                                <span className="product__original-price">
                                  &#8377; {product.price}
                                </span>
                                <span className="product__offer">
                                  &#8377; {product.offer_price}
                                </span>
                              </>
                            ) : (
                              <span className="product__offer">&#8377; {product.price}</span>
                            )}
                          </div>
                        </li>
                      </div>
                    ))}
                  </div>
                </ul>
              </div>
            ))}
          </React.Fragment>
        </div>
      )}
    </div>
  );
});

export default ProductLists;
