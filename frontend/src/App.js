import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { CartProvider } from "./context/CartContext";
import { Toaster } from "./components/ui/toaster";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import ProductCategory from "./pages/ProductCategory";
import Cart from "./pages/Cart";
import CustomDesign from "./pages/CustomDesign";
import About from "./pages/About";

function App() {
  return (
    <div className="App min-h-screen flex flex-col">
      <CartProvider>
        <BrowserRouter>
          <Header />
          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/clothes" element={<ProductCategory category="clothes" />} />
              <Route path="/socks" element={<ProductCategory category="socks" />} />
              <Route path="/books" element={<ProductCategory category="books" />} />
              <Route path="/shoes" element={<ProductCategory category="shoes" />} />
              <Route path="/cart" element={<Cart />} />
              <Route path="/custom-design" element={<CustomDesign />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </main>
          <Footer />
          <Toaster />
        </BrowserRouter>
      </CartProvider>
    </div>
  );
}