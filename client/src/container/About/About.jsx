import React from 'react';
import aboutImg from "../../assets/about_img.png";
import aboutBackImg from "../../assets/about__background.jpg";
import AppWrap from "../../wrapper/AppWrap.js";
import "./About.scss";

const About = () => {
  return (
    <div className='app__about' id='about'>
      <div className="app__about__container">
        <div className="overlay-about"></div>
        
        <div className="about__main">
          <div className="about__heading">
            <h1>A little bit about me</h1>
            <i>"Hello! I'm a student currently pursuing my studies at Vellore Institute of Technology. I'm passionate about technology and innovation, and I'm working on a project that aims to simplify and streamline the process of finding and comparing medicine prices across different platforms. My goal is to provide users with the best deals on medicines, making healthcare more accessible and affordable. Join me on this journey as we explore the intersection of technology and healthcare!"</i>
          </div>
        </div>
        <div className="about__img">
          <img src={aboutImg} alt="" />
        </div>
        <div className="about__back-img">
          <img src={aboutBackImg} alt="" />
        </div>
      </div>
        
    </div>
  );
};

export default AppWrap(About,"app__whitebg");
