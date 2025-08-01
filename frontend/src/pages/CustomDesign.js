import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { Upload, Shirt, Type, Image } from 'lucide-react';
import { useToast } from '../hooks/use-toast';
import { mockCustomOrders } from '../mock';

const CustomDesign = () => {
  const [formData, setFormData] = useState({
    email: '',
    customText: '',
    description: '',
    selectedFile: null
  });
  const [dragActive, setDragActive] = useState(false);
  const { toast } = useToast();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData(prev => ({
        ...prev,
        selectedFile: file
      }));
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFormData(prev => ({
        ...prev,
        selectedFile: e.dataTransfer.files[0]
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!formData.email || (!formData.customText && !formData.selectedFile)) {
      toast({
        title: "Missing Information",
        description: "Please provide your email and either custom text or an image.",
        variant: "destructive"
      });
      return;
    }

    // Mock storing the custom order
    const newOrder = {
      id: Date.now(),
      email: formData.email,
      customText: formData.customText,
      description: formData.description,
      fileName: formData.selectedFile?.name || null,
      createdAt: new Date().toISOString(),
      status: 'pending'
    };

    mockCustomOrders.push(newOrder);

    toast({
      title: "Custom Order Submitted!",
      description: "We've received your custom t-shirt order. We'll contact you within 24 hours with a quote and timeline.",
    });

    // Reset form
    setFormData({
      email: '',
      customText: '',
      description: '',
      selectedFile: null
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-black mb-6">Design Your Own</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Create a custom t-shirt with your own text, images, or designs. Express your unique style and make it truly yours.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Design Options */}
          <div className="space-y-6">
            <Card className="border-gray-200">
              <CardHeader>
                <CardTitle className="flex items-center text-black">
                  <Type className="mr-2 h-5 w-5" />
                  Custom Text
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 text-sm mb-4">
                  Add your own message, quote, or design text to your t-shirt.
                </p>
                <Textarea
                  name="customText"
                  placeholder="Enter your custom text here..."
                  value={formData.customText}
                  onChange={handleInputChange}
                  className="min-h-[100px]"
                />
              </CardContent>
            </Card>

            <Card className="border-gray-200">
              <CardHeader>
                <CardTitle className="flex items-center text-black">
                  <Image className="mr-2 h-5 w-5" />
                  Upload Image
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 text-sm mb-4">
                  Upload your own image or design to print on your t-shirt.
                </p>
                <div
                  className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                    dragActive
                      ? 'border-black bg-gray-100'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="hidden"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload" className="cursor-pointer">
                    <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                    <p className="text-gray-600 mb-2">
                      {formData.selectedFile
                        ? `Selected: ${formData.selectedFile.name}`
                        : 'Click to upload or drag and drop'}
                    </p>
                    <p className="text-sm text-gray-500">PNG, JPG, GIF up to 10MB</p>
                  </label>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Order Form */}
          <div className="space-y-6">
            <Card className="border-gray-200">
              <CardHeader>
                <CardTitle className="flex items-center text-black">
                  <Shirt className="mr-2 h-5 w-5" />
                  Order Details
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="email">Email Address *</Label>
                  <Input
                    type="email"
                    id="email"
                    name="email"
                    placeholder="your@email.com"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div>
                  <Label htmlFor="description">Additional Details</Label>
                  <Textarea
                    id="description"
                    name="description"
                    placeholder="Size preferences, color choices, special instructions..."
                    value={formData.description}
                    onChange={handleInputChange}
                    className="min-h-[100px]"
                  />
                </div>

                <div className="bg-gray-100 p-4 rounded-lg">
                  <h4 className="font-semibold text-black mb-2">Pricing Information</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Text-only designs: Starting at $25</li>
                    <li>• Image prints: Starting at $30</li>
                    <li>• Complex designs: $35-45</li>
                    <li>• We'll provide exact quote via email</li>
                  </ul>
                </div>

                <Button
                  onClick={handleSubmit}
                  className="w-full bg-black text-white hover:bg-gray-800 transition-all duration-300 transform hover:scale-105"
                  size="lg"
                >
                  Submit Custom Order
                </Button>

                <p className="text-xs text-gray-500 text-center">
                  We'll contact you within 24 hours with a quote and production timeline.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomDesign;