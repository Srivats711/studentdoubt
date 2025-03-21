import { initializeApp } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js";
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
} from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";
const firebaseConfig = {
  apiKey: "AIzaSyBqMLARXOZ-p3TzQkgnbaL_2obryxYNhh4",
  authDomain: "login-12042.firebaseapp.com",
  projectId: "login-12042",
  storageBucket: "login-12042.firebasestorage.app",
  messagingSenderId: "305875061986",
  appId: "1:305875061986:web:2a7a2c08ced1f74b4522bb"
};
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Form Elements
const signupForm = document.getElementById("signup-form");
const loginForm = document.getElementById("login-form");

// Tabs
const signupTab = document.getElementById("signup-tab");
const loginTab = document.getElementById("login-tab");

// Tab Switching Functionality
signupTab.addEventListener("click", () => {
  signupTab.classList.add("active");
  loginTab.classList.remove("active");
  signupForm.classList.add("active");
  loginForm.classList.remove("active");
});

loginTab.addEventListener("click", () => {
  loginTab.classList.add("active");
  signupTab.classList.remove("active");
  loginForm.classList.add("active");
  signupForm.classList.remove("active");
});

// Sign Up Functionality
signupForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const email = document.getElementById("signup-email").value;
  const password = document.getElementById("signup-password").value;

  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Successful sign up
      const user = userCredential.user;
      alert(`Sign Up Successful! Welcome, ${user.email}`);
      // Optionally, redirect or update UI
    })
    .catch((error) => {
      console.error("Sign Up Error:", error);
      alert(`Error: ${error.message}`);
    });
});

// Login Functionality
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Successful login
      const user = userCredential.user;
      alert(`Login Successful! Welcome back, ${user.email}`);
      // Optionally, redirect or update UI
    })
    .catch((error) => {
      console.error("Login Error:", error);
      alert(`Error: ${error.message}`);
    });
});

