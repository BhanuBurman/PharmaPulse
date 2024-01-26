import React from "react";

import chatImg from "../../assets/chat__img.jpg";
import emailIcon from "../../assets/email-icon.png";
import phoneIcon from "../../assets/phone-icon.png";
import AppWrap from "../../wrapper/AppWrap";

import "./Contact.scss";
const Contact = ({ scrollToContact }) => {
  const handleContactClick = () => {
    // You can customize this logic as needed
    scrollToContact();
  };
  return (
    <div className="app__contact" id="contact">
      <div className="form_container">
        <h4>Get in Touch</h4>
        <h1>Let's Chat, Reach Out to Us</h1>
        <p>
          Have questions or feedback?We're here to help.Send us a message, and
          we'll respond within 24 hours
        </p>
        <div className="line"></div>
        <form action="">
          <div className="user__name">
            <div className="first__name">
              <label>FirstName</label>
              <input type="text" placeholder="First name" />
            </div>
            <div className="last__name">
              <label>LastName</label>
              <input type="text" placeholder="Last name" />
            </div>
          </div>
          <div className="user__email">
            <label>EmailAddress</label>
            <input type="email" placeholder="Email address" />
          </div>
          <div className="user__message">
            <label>Message</label>
            <textarea
              name="user_text"
              id=""
              cols="30"
              rows="4"
              placeholder="Leave us message"
            ></textarea>
          </div>
          <button type="submit">Submit</button>
        </form>
      </div>
      <div className="img_container">
        <div className="chat__image">
          <img src={chatImg} alt="" />
        </div>
        <div className="my__info">
          <a href="mailto:bhanuburman484@gmail.com" className="my__email">
            <img src={emailIcon} alt="email" />
            <div className="email__info">
              <h3>Email</h3>
              <p>bhanuburman484@gmail.com</p>
            </div>
          </a>
          <a href="tel:+91 8305855239" className="my__phone">
            <img src={phoneIcon} alt="phone" />
            <div className="phone__info">
              <h3>Phone</h3>
              <p>+918305855239</p>
            </div>
          </a>
        </div>
      </div>
    </div>
  );
};

export default AppWrap(Contact,"");
