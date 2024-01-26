import React, {useState, useEffect,useRef} from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Navbar,Login,Signup } from './components'
import {ProductLists,Footer,Header,Contact,About} from './container'

import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';

import './App.scss'


const firebaseConfig = {
  apiKey: "AIzaSyAjb0apHpkKo9XTDQzO65f5yF9zHac2soE",
  authDomain: "pharmapulse-23ea9.firebaseapp.com",
  databaseURL: "https://pharmapulse-23ea9-default-rtdb.firebaseio.com",
  projectId: "pharmapulse-23ea9",
  storageBucket: "pharmapulse-23ea9.appspot.com",
  messagingSenderId: "1099387759711",
  appId: "1:1099387759711:web:398de745607f10c4213fea",
  measurementId: "G-7RJ9QC9J32"
};

firebase.initializeApp(firebaseConfig);

function App() {
  
  const [data, setData] = useState([]);
  // Add these state variables
const [showSignUp, setShowSignUp] = useState(false);
const [showLogin, setShowLogin] = useState(false);
const openSignUp = () => {
  setShowSignUp(true);
};

const closeSignUp = () => {
  setShowSignUp(false);
};

const openLogin = () => {
  setShowLogin(true);
};

const closeLogin = () => {
  setShowLogin(false);
};


  // useEffect(()=>{
  //   getData();
  // },[])
  // const getData = async () => {
  //   const response = await fetch("http://localhost:5000/")
  //   const data = await response.json()
  //   console.log(data);
  //   setData(data)
  // }
  const [fetchedData, setFetchedData] = useState([]);
  const [medName, setMedName] = useState("");
  const productListRef = useRef();
  // Callback function to receive data from Header
  const handleDataFetched = (data) => {
    setFetchedData(data.products);
  };
  const handleName = ( medName ) => {
    setMedName(medName);
  }

  return (
    <div className="app">
         <Navbar
        openSignUp={openSignUp}
        openLogin={openLogin}
        closeSignUp={closeSignUp}
        closeLogin={closeLogin}
        showSignUp={showSignUp}
        showLogin={showLogin}
      />
        <Header onClicked={handleName} onDataFetched={handleDataFetched} productListRef={productListRef} />
        <ProductLists medicineName={medName} products={fetchedData} ref={productListRef}  />
        <About />
        <Contact />
        <Footer />
        {showSignUp && <Signup onClose={closeSignUp} />}
      {showLogin && <Login onClose={closeLogin} />}
    </div>
  )
}

export default App
