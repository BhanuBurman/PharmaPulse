import React, { useState, useEffect } from 'react';
import header_img1 from '../../assets/Header-img-1.jpg';
import header_img2 from '../../assets/Header-img-2.jpg';
import header_img3 from '../../assets/Header-img-3.jpg';
import searchButton from '../../assets/search.png';

import AppWrap from '../../wrapper/AppWrap';

import './Header.scss';

const Header = ({onClicked , onDataFetched,productListRef}) => {
  const images = [header_img1, header_img2, header_img3];
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [medicineName, setMedicineName] = useState('');
  const [clicked, setClicked] = useState(false);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentImageIndex((prevIndex) => {
        // Increment the index
        const newIndex = prevIndex + 1;
  
        // Check if it's the last index
        if (newIndex === images.length) {
          // Reset to a negative value corresponding to the width
          return 0;
        }
  
        return newIndex;
      });
    }, 3000);
  
    return () => clearInterval(intervalId);
  }, [images.length]);
  

  const handleSearch = async () => {
    try {
      // Send a request to the backend with the medicineName
      setClicked(true);
      const response = await fetch(`/products?medicine=${encodeURIComponent(medicineName)}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log('Data from header', data);
  
      // Update the medicineName state first
      setMedicineName(medicineName);
      
      // Extract the 'products' property and pass it to the parent component
      onDataFetched(data);
      
      // Call onClicked after updating the medicineName state
      onClicked(medicineName);

      // Scroll to the ProductList component
      if (productListRef.current) {
        productListRef.current.scrollIntoView({
          behavior: 'instant',
          block: 'start', // Align to the top of the element
          offset: -150, // Set your desired offset value here
        });
      }
      setClicked(false);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
  

  return (
    <div className="app__header" id='home'>
      <div className="header__info">
        <div className='header__info-first'>Get the Best Deals on Medicines with PharmaPulse"</div>
        <div className='header__info-second'>140890+ medicine prices from top leading Pharma Platforms</div>
      </div>
      <div className="header__imgs">
        <div className="slider" style={{ transform: `translateX(${-currentImageIndex * 100}%)` }}>
          {images.map((img, index) => (
            <img
              key={index}
              className={`header-img-${index + 1} ${index === currentImageIndex ? 'active' : ''}`}
              src={img}
              alt=""
            />
          ))}
        </div>
        <div className="overlay"></div>
      </div>
      <div className="header__searchBar">
      <input
          type="text"
          placeholder='Search Medicine'
          value={medicineName}
          onChange={(e) => setMedicineName(e.target.value)}
        />
        <button type='submit' onClick={handleSearch}>
          <img src={searchButton} alt="" />
        </button>
      </div>
        {clicked &&(
          <div className='loading'>
          <div className="loading__info">Please wait... this will take a moment</div>
          <div className="loading__button"></div>
          </div>
        )}
    </div>
  );
};

export default AppWrap(Header,"");
