import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { CheckCircle, Clock, XCircle, ShoppingBag } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CheckoutSuccess = () => {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get('session_id');
  const [paymentStatus, setPaymentStatus] = useState('checking');
  const [paymentData, setPaymentData] = useState(null);
  const [error, setError] = useState(null);

  // Polling function to check payment status
  const pollPaymentStatus = async (attempts = 0) => {
    const maxAttempts = 5;
    const pollInterval = 2000; // 2 seconds

    if (attempts >= maxAttempts) {
      setPaymentStatus('timeout');
      setError('Payment status check timed out. Please check your email for confirmation.');
      return;
    }

    try {
      const response = await axios.get(`${API}/checkout/status/${sessionId}`);
      const data = response.data;
      
      if (data.payment_status === 'paid') {
        setPaymentStatus('success');
        setPaymentData(data);
        return;
      } else if (data.status === 'expired') {
        setPaymentStatus('expired');
        setError('Payment session expired. Please try again.');
        return;
      }

      // If payment is still pending, continue polling
      setPaymentStatus('pending');
      setTimeout(() => pollPaymentStatus(attempts + 1), pollInterval);
    } catch (error) {
      console.error('Error checking payment status:', error);
      setPaymentStatus('error');
      setError('Error checking payment status. Please try again.');
    }
  };

  useEffect(() => {
    if (sessionId) {
      pollPaymentStatus();
    } else {
      setPaymentStatus('error');
      setError('No session ID found in URL');
    }
  }, [sessionId]);

  const getStatusIcon = () => {
    switch (paymentStatus) {
      case 'success':
        return <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />;
      case 'pending':
      case 'checking':
        return <Clock className="h-16 w-16 text-yellow-500 mx-auto mb-4 animate-spin" />;
      case 'expired':
      case 'error':
      case 'timeout':
        return <XCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />;
      default:
        return <Clock className="h-16 w-16 text-gray-400 mx-auto mb-4" />;
    }
  };

  const getStatusMessage = () => {
    switch (paymentStatus) {
      case 'success':
        return {
          title: 'Payment Successful!',
          description: 'Thank you for your purchase from Urban Threads. Your order has been confirmed and you will receive an email confirmation shortly.',
          variant: 'success'
        };
      case 'pending':
        return {
          title: 'Payment Processing...',
          description: 'We are verifying your payment. Please wait a moment.',
          variant: 'pending'
        };
      case 'checking':
        return {
          title: 'Checking Payment Status...',
          description: 'Please wait while we verify your payment.',
          variant: 'pending'
        };
      case 'expired':
        return {
          title: 'Payment Session Expired',
          description: error || 'Your payment session has expired. Please try again.',
          variant: 'error'
        };
      case 'timeout':
        return {
          title: 'Status Check Timeout',
          description: error || 'Payment status check timed out. Please check your email for confirmation.',
          variant: 'error'
        };
      case 'error':
        return {
          title: 'Payment Error',
          description: error || 'There was an error processing your payment. Please contact support.',
          variant: 'error'
        };
      default:
        return {
          title: 'Processing...',
          description: 'Please wait while we process your request.',
          variant: 'pending'
        };
    }
  };

  const status = getStatusMessage();

  return (
    <div className="min-h-screen bg-gray-50 py-16 px-4">
      <div className="max-w-2xl mx-auto">
        <Card className="border-gray-200">
          <CardContent className="p-8 text-center">
            {getStatusIcon()}
            
            <h1 className={`text-3xl font-bold mb-4 ${
              status.variant === 'success' ? 'text-green-600' :
              status.variant === 'error' ? 'text-red-600' :
              'text-yellow-600'
            }`}>
              {status.title}
            </h1>
            
            <p className="text-gray-600 text-lg mb-8">
              {status.description}
            </p>

            {paymentData && (
              <div className="bg-gray-100 p-4 rounded-lg mb-6 text-left">
                <h3 className="font-semibold text-black mb-2">Payment Details</h3>
                <div className="space-y-1 text-sm text-gray-600">
                  <p><strong>Session ID:</strong> {paymentData.session_id?.slice(0, 20)}...</p>
                  <p><strong>Amount:</strong> ${(paymentData.amount_total / 100).toFixed(2)} {paymentData.currency?.toUpperCase()}</p>
                  <p><strong>Status:</strong> {paymentData.payment_status}</p>
                </div>
              </div>
            )}

            <div className="space-y-4">
              {paymentStatus === 'success' && (
                <Button 
                  size="lg" 
                  className="bg-black text-white hover:bg-gray-800"
                >
                  <Link to="/" className="flex items-center">
                    <ShoppingBag className="mr-2 h-5 w-5" />
                    Continue Shopping
                  </Link>
                </Button>
              )}
              
              {(paymentStatus === 'expired' || paymentStatus === 'error' || paymentStatus === 'timeout') && (
                <div className="space-y-2">
                  <Button 
                    size="lg" 
                    className="bg-black text-white hover:bg-gray-800 w-full"
                  >
                    <Link to="/cart">Try Again</Link>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="border-black text-black hover:bg-black hover:text-white w-full"
                  >
                    <Link to="/">Continue Shopping</Link>
                  </Button>
                </div>
              )}
            </div>

            {sessionId && (
              <p className="text-xs text-gray-400 mt-6">
                Session ID: {sessionId}
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default CheckoutSuccess;