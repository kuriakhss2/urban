import React from 'react';
import { Card, CardContent } from '../components/ui/card';
import { Heart, Users, Zap, Award } from 'lucide-react';

const About = () => {
  const values = [
    {
      icon: Heart,
      title: 'Quality First',
      description: 'We believe in creating products that last, using premium materials and ethical manufacturing processes.'
    },
    {
      icon: Users,
      title: 'Community Focused',
      description: 'Building a community of urban individuals who appreciate style, comfort, and authentic expression.'
    },
    {
      icon: Zap,
      title: 'Innovation',
      description: 'Constantly evolving our designs and processes to bring you the latest in urban fashion and lifestyle.'
    },
    {
      icon: Award,
      title: 'Sustainability',
      description: 'Committed to sustainable practices and reducing our environmental impact through conscious choices.'
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-black text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl lg:text-6xl font-bold mb-6">About Urban Threads</h1>
          <p className="text-xl lg:text-2xl text-gray-300 leading-relaxed">
            Born from the streets, crafted for the modern individual. We're more than a brand – we're a lifestyle.
          </p>
        </div>
      </section>

      {/* Story Section */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-black mb-6">Our Story</h2>
              <p className="text-gray-600 text-lg leading-relaxed mb-6">
                Urban Threads was founded in 2025 with a simple mission: to create premium lifestyle products that reflect the energy and authenticity of urban culture. What started as a small collection of essential clothing has grown into a comprehensive lifestyle brand.
              </p>
              <p className="text-gray-600 text-lg leading-relaxed mb-6">
                We understand that style is personal, which is why we offer not just carefully curated ready-to-wear pieces, but also the opportunity to create something uniquely yours through our custom design service.
              </p>
              <p className="text-gray-600 text-lg leading-relaxed">
                From comfortable socks to thought-provoking books, from essential clothing to statement shoes – every item in our collection is chosen or created with the modern urban individual in mind.
              </p>
            </div>
            <div className="relative">
              <div className="bg-gray-100 aspect-square rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <div className="text-6xl font-bold text-black mb-4">2025</div>
                  <p className="text-gray-600 text-lg">Founded</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center text-black mb-12">What We Stand For</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => {
              const IconComponent = value.icon;
              return (
                <Card key={index} className="border-gray-200 hover:shadow-lg transition-all duration-300">
                  <CardContent className="p-6 text-center">
                    <div className="bg-black text-white rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <IconComponent className="h-8 w-8" />
                    </div>
                    <h3 className="text-xl font-semibold text-black mb-3">{value.title}</h3>
                    <p className="text-gray-600 leading-relaxed">{value.description}</p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-black mb-8">Our Mission</h2>
          <p className="text-xl text-gray-600 leading-relaxed mb-8">
            To empower urban individuals with products that enhance their lifestyle, express their personality, and connect them with a community of like-minded people who value quality, authenticity, and conscious living.
          </p>
          <div className="bg-black text-white p-8 rounded-lg">
            <h3 className="text-2xl font-bold mb-4">Join the Urban Threads Community</h3>
            <p className="text-lg text-gray-300">
              Whether you're here for our curated collections or looking to create something custom, you're part of a community that values individuality, quality, and authentic expression.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;