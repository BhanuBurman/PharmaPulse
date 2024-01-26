import React from 'react';


const AppWrap = (Component, classNames) => function HOC({scrollToContact, ...props }){
  return (
    <div className={`app__container ${classNames}`}>
      <div className="app__wrapper app__flex">
      <Component scrollToContact={scrollToContact} {...props} />
      </div>
    </div>
  )
}

export default AppWrap
