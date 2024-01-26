import React, { useState, useEffect } from "react";
import firebase from "firebase/compat/app";
import userProfile from "../../assets/user-profile.png";
import { Link as ScrollLink, animateScroll as scroll } from "react-scroll";
import { HiMenuAlt4, HiX } from "react-icons/hi";
import "firebase/compat/auth";
import "./Navbar.scss";

const Navbar = ({ openSignUp, openLogin }) => {
  const [loggedIn, setLoggedIn] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    // Listen for changes in the authentication state
    const unsubscribe = firebase.auth().onAuthStateChanged((user) => {
      setLoggedIn(!!user);
    });

    return () => {
      // Unsubscribe when the component unmounts
      unsubscribe();
    };
  }, []);


  const toggleDropdown = () => {
    setShowDropdown(!showDropdown);
  };

  const scrollToSection = (section) => {
    const element = document.getElementById(section);
    if (element) {
      // Scroll to the element
      element.scrollIntoView({
        behavior: "instant",
        block: "start",
      });
    }
  };
  const handleToggle = (ele) =>{
    const element = document.getElementById("menu");
    if(ele){
      element.style.right = "-17rem";
    }else{
      element.style.right = "-80rem";
    }
  }
  const handleLogout = () => {
    firebase.auth().signOut();
  };

  return (
    <>
    <nav className="app__navbar">
      <div className="app__navbar-logo">PharmaPulse</div>
      <div className="app__navbar-lists">

      <div className="left-nav">
        <ul className="app__navbar-links">
          {["home", "about", "contact"].map((item) => (
            <li className="app__flex p-text" key={`link-${item}`}>
              <div />
              <ScrollLink to={item} smooth={true} duration={100} offset={-150}>
                <a href="#" onClick={() => scrollToSection(item)}>
                  {item}
                </a>
              </ScrollLink>
            </li>
          ))}
        </ul>
      </div>
      <div className="right-nav">
        {!loggedIn && (
          <div className="app__navbar-buttons">
            <a href="#" onClick={openSignUp} className="signup-button">
              Sign up
            </a>
            <a href="#" onClick={openLogin} className="login-button">
              Log in
            </a>
          </div>
        )}
        {loggedIn && (
          <div className="user-profile" onClick={toggleDropdown}>
            {/* Replace this with the actual user profile circular picture */}
            <button>
              <img src={userProfile} alt="User Profile" />
            </button>
            {showDropdown && (
              <div className="user-profile-dropdown">
                <a href="#">Hi! User</a>
                {/* <a href="#">Change Password</a> */}
                <a className="logout-button" onClick={handleLogout}>Logout
                </a>
              </div>
            )}
          </div>
        )}
      </div>
      
    </div>
    <div className="navbar__menu">
    <HiMenuAlt4 onClick={() => { handleToggle(true);}} />
    
      <div id="menu">
      <HiX onClick={() => {handleToggle(false);}} />
      <ul>
          {["home", "about", "contact"].map((item) => (
            <li  key={`link-${item}`}>
              <ScrollLink to={item} smooth={true} duration={100} offset={-150}>
                <a href="#" onClick={() => scrollToSection(item)}>
                  {item}
                </a>
              </ScrollLink>
            </li>
          ))}
        </ul>
          </div>
       
        </div>
    </nav>

    
    </>
  );
};

export default Navbar;
