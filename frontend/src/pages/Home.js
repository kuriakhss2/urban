import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Shirt, Book, Footprints, Zap } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { useCart } from '../context/CartContext';
import { useToast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const { addToCart } = useCart();
  const { toast } = useToast();
  
  const categories = [
    { name: 'Clothes', icon: Shirt, path: '/clothes', color: 'bg-gray-100' },
    { name: 'Socks', icon: Footprints, path: '/socks', color: 'bg-gray-200' },
    { name: 'Books', icon: Book, path: '/books', color: 'bg-gray-300' },
    { name: 'Shoes', icon: Footprints, path: '/shoes', color: 'bg-gray-400' }
  ];

useEffect(() => {
  const fetchProducts = async () => {
    try {
      const response = await axios.get('/.netlify/functions/products');

      console.log("Fetched products:", response.data);

      // ✅ Safe handling of data
      const data = Array.isArray(response.data) ? response.data : [];
      setFeaturedProducts(data.slice(0, 8));

      setLoading(false);
    } catch (error) {
      console.error('Error fetching products:', error);
      toast({
        title: "Error",
        description: "Failed to load products. Please try again.",
        variant: "destructive"
      });
      setLoading(false);
    }
  };

  fetchProducts();
}, []);



  const handleAddToCart = (product) => {
    addToCart(product);
    toast({
      title: "Added to cart!",
      description: `${product.name} has been added to your cart.`,
    });
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative bg-black text-white py-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl lg:text-7xl font-bold mb-6 tracking-tight">
            URBAN THREADS
          </h1>
          <p className="text-xl lg:text-2xl mb-8 text-gray-300 max-w-3xl mx-auto">
            Modern lifestyle essentials for the urban individual. Discover premium clothing, accessories, and curated reads.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button size="lg" className="bg-white text-black hover:bg-gray-200 transition-all duration-300 transform hover:scale-105">
              <Link to="/clothes" className="flex items-center">
                Shop Collection
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              className="border-white text-white hover:bg-white hover:text-black transition-all duration-300"
            >
              <Link to="/custom-design" className="flex items-center">
                <Zap className="mr-2 h-5 w-5" />
                Design Yours
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12 text-black">Shop by Category</h2>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
            {categories.map((category) => {
              const IconComponent = category.icon;
              return (
                <Link key={category.name} to={category.path} className="group">
                  <Card className="border-2 border-gray-200 hover:border-black transition-all duration-300 transform hover:scale-105">
                    <CardContent className="p-8 text-center">
                      <div className={`${category.color} rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 group-hover:bg-black group-hover:text-white transition-all duration-300`}>
                        <IconComponent className="h-8 w-8" />
                      </div>
                      <h3 className="text-xl font-semibold text-black group-hover:text-gray-700 transition-colors">
                        {category.name}
                      </h3>
                    </CardContent>
                  </Card>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12 text-black">Featured Products</h2>
          
          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {[...Array(8)].map((_, i) => (
                <Card key={i} className="border-gray-200">
                  <CardContent className="p-0">
                    <div className="aspect-square bg-gray-200 animate-pulse"></div>
                    <div className="p-4 space-y-2">
                      <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
                      <div className="h-3 bg-gray-200 rounded animate-pulse"></div>
                      <div className="h-6 bg-gray-200 rounded animate-pulse"></div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
             {Array.isArray(featuredProducts) && featuredProducts.map((product) => (
                <Card key={product.id} className="group hover:shadow-lg transition-all duration-300 border-gray-200">
                  <CardContent className="p-0">
                    <div className="aspect-square overflow-hidden">
                      <img
                        src={product.image}
                        alt={product.name}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                      />
                    </div>
                    <div className="p-4">
                      <h3 className="font-semibold text-black mb-2">{product.name}</h3>
                      <p className="text-gray-600 text-sm mb-3">{product.description}</p>
                      <div className="flex justify-between items-center">
                        <span className="text-2xl font-bold text-black">${product.price}</span>
                        <Button 
                          onClick={() => handleAddToCart(product)}
                          size="sm" 
                          className="bg-black text-white hover:bg-gray-800 transition-colors"
                        >
                          Add to Cart
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
          
          <div className="text-center mt-12">
            <Button size="lg" variant="outline" className="border-black text-black hover:bg-black hover:text-white">
              <Link to="/clothes">View All Products</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-black text-white py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">Design Your Own</h2>
          <p className="text-xl text-gray-300 mb-8">
            Create custom t-shirts with your own designs, messages, or images. Express your unique style.
          </p>
          <Button size="lg" className="bg-white text-black hover:bg-gray-200 transition-all duration-300 transform hover:scale-105">
            <Link to="/custom-design" className="flex items-center">
              <Zap className="mr-2 h-5 w-5" />
              Start Designing
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Home;