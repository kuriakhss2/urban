import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, Instagram, Twitter, Facebook } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { useToast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Footer = () => {
  const [email, setEmail] = useState('');
  const [isSubscribing, setIsSubscribing] = useState(false);
  const { toast } = useToast();

  const handleNewsletterSubmit = async (e) => {
    e.preventDefault();
    if (!email) return;

    setIsSubscribing(true);

    try {
      await axios.post(`${API}/newsletter/subscribe`, { email });
      
      toast({
        title: "Subscribed!",
        description: "Thank you for subscribing to our newsletter.",
      });
      setEmail('');
    } catch (error) {
      console.error('Newsletter subscription error:', error);
      if (error.response?.status === 400) {
        toast({
          title: "Already Subscribed",
          description: "This email is already subscribed to our newsletter.",
          variant: "destructive"
        });
      } else {
        toast({
          title: "Subscription Failed",
          description: "There was an error subscribing to the newsletter. Please try again.",
          variant: "destructive"
        });
      }
    } finally {
      setIsSubscribing(false);
    }
  };

  return (
    <footer className="bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <h3 className="text-2xl font-bold tracking-wider">URBAN THREADS</h3>
            <p className="text-gray-400 text-sm">
              Modern lifestyle brand offering premium clothing, accessories, and curated books for the urban individual.
            </p>
            <div className="flex space-x-4">
              <Instagram className="h-5 w-5 cursor-pointer hover:text-gray-300 transition-colors" />
              <Twitter className="h-5 w-5 cursor-pointer hover:text-gray-300 transition-colors" />
              <Facebook className="h-5 w-5 cursor-pointer hover:text-gray-300 transition-colors" />
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold">Shop</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link to="/clothes" className="hover:text-white transition-colors">Clothes</Link></li>
              <li><Link to="/socks" className="hover:text-white transition-colors">Socks</Link></li>
              <li><Link to="/books" className="hover:text-white transition-colors">Books</Link></li>
              <li><Link to="/shoes" className="hover:text-white transition-colors">Shoes</Link></li>
              <li><Link to="/custom-design" className="hover:text-white transition-colors">Custom Design</Link></li>
            </ul>
          </div>

          {/* Customer Service */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold">Support</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link to="/about" className="hover:text-white transition-colors">About Us</Link></li>
              <li><Link to="#" className="hover:text-white transition-colors">Shipping Info</Link></li>
              <li><Link to="#" className="hover:text-white transition-colors">Returns</Link></li>
              <li><Link to="#" className="hover:text-white transition-colors">Size Guide</Link></li>
              <li><Link to="#" className="hover:text-white transition-colors">Contact</Link></li>
            </ul>
          </div>

          {/* Newsletter */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold">Stay Updated</h4>
            <p className="text-gray-400 text-sm">
              Subscribe to get special offers, free giveaways, and new arrivals.
            </p>
            <form onSubmit={handleNewsletterSubmit} className="space-y-2">
              <Input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="bg-gray-900 border-gray-700 text-white placeholder-gray-400"
                required
              />
              <Button 
                type="submit" 
                disabled={isSubscribing}
                className="w-full bg-white text-black hover:bg-gray-200 transition-colors"
              >
                <Mail className="h-4 w-4 mr-2" />
                {isSubscribing ? 'Subscribing...' : 'Subscribe'}
              </Button>
            </form>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400 text-sm">
          <p>&copy; 2025 Urban Threads. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;