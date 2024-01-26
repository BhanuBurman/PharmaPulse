import React from 'react'

import Twitter from "../../assets/twitter-logo.png"
import facebook from "../../assets/fb-logo.png"
import linkin from "../../assets/linkin-logo.png";
import google from "../../assets/google-logo.png";


import "./Footer.scss"

const Footer = () => {
  return (
    <div className='app__footer'>
      <div className='copyright'>
        Copyright &#169;2024 PharmaPulse
      </div>
      <div className="app__footer__main">
        <div className="footer__heading">
          Contact with Us
        </div>
        <div className="footer__info">
          <p>

        Stay updated on the latest developments and features of our platform. Follow us on social media for regular updates, announcements, and health-related tips. Your feedback is invaluable to us, and we look forward to building a healthier and more connected community together. Feel free to reach out to us for any inquiries or collaboration opportunities. Thank you for being a part of PharmaPulse!
          </p>
        </div>
        <div className="footer__social__media">
          <a href=""><img src={facebook} alt="meta" /></a>
          <a href=""><img src={Twitter} alt="twitter" /></a>
          <a href=""><img src={google} alt="google" /></a>
          <a href=""><img src={linkin} alt="linkedin" /></a>
        </div>
      </div>
      
      <div className="nav__list">
        <ul>
          <li>Home</li>
          <li>About</li>
          <li>Contact</li>
        </ul>
      </div>
    </div>
  )
}

export default Footer
