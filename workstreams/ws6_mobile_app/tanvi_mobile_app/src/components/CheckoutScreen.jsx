import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Input } from '@/components/ui/input.jsx'
import { 
  CreditCard, 
  MapPin, 
  Truck, 
  Shield,
  CheckCircle,
  ArrowLeft,
  Plus,
  Edit,
  Clock,
  Package,
  Star,
  Zap,
  Lock,
  Smartphone,
  Wallet,
  Building,
  Gift,
  Tag,
  AlertCircle,
  Info,
  ChevronRight,
  Calendar,
  User,
  Mail,
  Phone
} from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { EcommerceAPI } from '../services/api'

export default function CheckoutScreen({ currentUser, onBack }) {
  const { user } = useAuth()
  const [currentStep, setCurrentStep] = useState(1) // 1: Address, 2: Payment, 3: Review, 4: Confirmation
  const [cart, setCart] = useState({ items: [], total: 0 })
  const [addresses, setAddresses] = useState([])
  const [selectedAddress, setSelectedAddress] = useState(null)
  const [paymentMethods, setPaymentMethods] = useState([])
  const [selectedPayment, setSelectedPayment] = useState(null)
  const [shippingOptions, setShippingOptions] = useState([])
  const [selectedShipping, setSelectedShipping] = useState(null)
  const [orderSummary, setOrderSummary] = useState(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [orderComplete, setOrderComplete] = useState(false)
  const [orderDetails, setOrderDetails] = useState(null)
  const [promoCode, setPromoCode] = useState('')
  const [promoApplied, setPromoApplied] = useState(null)

  const steps = [
    { id: 1, title: 'Shipping', icon: MapPin },
    { id: 2, title: 'Payment', icon: CreditCard },
    { id: 3, title: 'Review', icon: CheckCircle },
    { id: 4, title: 'Complete', icon: Package }
  ]

  // Load checkout data
  useEffect(() => {
    loadCheckoutData()
  }, [])

  const loadCheckoutData = async () => {
    try {
      // Load cart
      const cartData = await EcommerceAPI.getCart()
      setCart(cartData)

      // Mock addresses for demo
      setAddresses([
        {
          id: 1,
          type: 'home',
          name: 'Home',
          fullName: 'Sarah Johnson',
          street: '123 Fashion Ave',
          city: 'New York',
          state: 'NY',
          zipCode: '10001',
          country: 'USA',
          phone: '+1 (555) 123-4567',
          isDefault: true
        },
        {
          id: 2,
          type: 'work',
          name: 'Office',
          fullName: 'Sarah Johnson',
          street: '456 Business Blvd',
          city: 'New York',
          state: 'NY',
          zipCode: '10002',
          country: 'USA',
          phone: '+1 (555) 987-6543',
          isDefault: false
        }
      ])

      // Mock payment methods for demo
      setPaymentMethods([
        {
          id: 1,
          type: 'card',
          brand: 'visa',
          last4: '4242',
          expiryMonth: 12,
          expiryYear: 2027,
          isDefault: true,
          name: 'Personal Card'
        },
        {
          id: 2,
          type: 'card',
          brand: 'mastercard',
          last4: '8888',
          expiryMonth: 8,
          expiryYear: 2026,
          isDefault: false,
          name: 'Business Card'
        },
        {
          id: 3,
          type: 'paypal',
          email: 'sarah@example.com',
          isDefault: false,
          name: 'PayPal'
        },
        {
          id: 4,
          type: 'apple_pay',
          isDefault: false,
          name: 'Apple Pay'
        }
      ])

      // Mock shipping options for demo
      setShippingOptions([
        {
          id: 1,
          name: 'Standard Shipping',
          description: '5-7 business days',
          price: 0,
          estimatedDays: '5-7',
          icon: Truck
        },
        {
          id: 2,
          name: 'Express Shipping',
          description: '2-3 business days',
          price: 12.99,
          estimatedDays: '2-3',
          icon: Zap
        },
        {
          id: 3,
          name: 'Same Day Delivery',
          description: 'Today before 9 PM',
          price: 19.99,
          estimatedDays: 'Today',
          icon: Clock,
          available: true
        }
      ])

      // Set defaults
      setSelectedAddress(addresses.find(addr => addr.isDefault) || addresses[0])
      setSelectedPayment(paymentMethods.find(pm => pm.isDefault) || paymentMethods[0])
      setSelectedShipping(shippingOptions[0])

    } catch (error) {
      console.error('Failed to load checkout data:', error)
    }
  }

  const applyPromoCode = () => {
    if (promoCode.toLowerCase() === 'welcome10') {
      setPromoApplied({
        code: 'WELCOME10',
        discount: 20.00,
        type: 'fixed'
      })
    } else if (promoCode.toLowerCase() === 'save15') {
      setPromoApplied({
        code: 'SAVE15',
        discount: 15,
        type: 'percentage'
      })
    } else {
      setPromoApplied(null)
    }
  }

  const calculateOrderSummary = () => {
    const subtotal = cart.subtotal || 149.98
    const shipping = selectedShipping?.price || 0
    const tax = subtotal * 0.08 // 8% tax
    let discount = 0

    if (promoApplied) {
      if (promoApplied.type === 'fixed') {
        discount = promoApplied.discount
      } else {
        discount = subtotal * (promoApplied.discount / 100)
      }
    }

    const total = subtotal + shipping + tax - discount

    return {
      subtotal,
      shipping,
      tax: Math.round(tax * 100) / 100,
      discount: Math.round(discount * 100) / 100,
      total: Math.round(total * 100) / 100
    }
  }

  const handleNextStep = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePreviousStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const processOrder = async () => {
    setIsProcessing(true)
    
    try {
      // Simulate order processing
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      const orderSummary = calculateOrderSummary()
      const orderDetails = {
        id: 'ORD-' + Math.random().toString(36).substr(2, 9).toUpperCase(),
        items: cart.items,
        address: selectedAddress,
        payment: selectedPayment,
        shipping: selectedShipping,
        summary: orderSummary,
        estimatedDelivery: getEstimatedDeliveryDate(),
        trackingNumber: 'TRK' + Math.random().toString(36).substr(2, 12).toUpperCase(),
        createdAt: new Date().toISOString()
      }
      
      setOrderDetails(orderDetails)
      setOrderComplete(true)
      setCurrentStep(4)
      
    } catch (error) {
      console.error('Order processing failed:', error)
    } finally {
      setIsProcessing(false)
    }
  }

  const getEstimatedDeliveryDate = () => {
    const days = selectedShipping?.estimatedDays === 'Today' ? 0 : 
                  selectedShipping?.estimatedDays === '2-3' ? 3 : 7
    const deliveryDate = new Date()
    deliveryDate.setDate(deliveryDate.getDate() + days)
    return deliveryDate.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }

  const displayUser = user || currentUser
  const summary = calculateOrderSummary()

  if (orderComplete && orderDetails) {
    return (
      <div className="p-4 space-y-6">
        {/* Success Header */}
        <div className="text-center py-8">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="w-12 h-12 text-green-600" />
          </div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Order Confirmed!</h1>
          <p className="text-gray-600">Thank you for your purchase</p>
        </div>

        {/* Order Details */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Package className="w-5 h-5" />
              <span>Order Details</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Order Number</span>
              <span className="font-medium">{orderDetails.id}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Total Amount</span>
              <span className="font-bold text-lg">${orderDetails.summary.total}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Estimated Delivery</span>
              <span className="font-medium">{orderDetails.estimatedDelivery}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Tracking Number</span>
              <span className="font-medium text-blue-600">{orderDetails.trackingNumber}</span>
            </div>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <div className="space-y-3">
          <Button className="w-full" onClick={() => window.location.href = '/orders'}>
            <Package className="w-4 h-4 mr-2" />
            Track Your Order
          </Button>
          <Button variant="outline" className="w-full" onClick={() => window.location.href = '/shop'}>
            Continue Shopping
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <Button variant="ghost" size="sm" onClick={onBack}>
          <ArrowLeft className="w-4 h-4" />
        </Button>
        <div>
          <h1 className="text-xl font-bold text-gray-800">Checkout</h1>
          <p className="text-sm text-gray-600">Step {currentStep} of 4</p>
        </div>
      </div>

      {/* Progress Steps */}
      <div className="flex items-center justify-between">
        {steps.map((step, index) => {
          const IconComponent = step.icon
          const isActive = currentStep === step.id
          const isCompleted = currentStep > step.id
          
          return (
            <div key={step.id} className="flex items-center">
              <div className={`flex items-center space-x-2 ${
                isActive ? 'text-blue-600' : isCompleted ? 'text-green-600' : 'text-gray-400'
              }`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  isActive ? 'bg-blue-100' : isCompleted ? 'bg-green-100' : 'bg-gray-100'
                }`}>
                  {isCompleted ? (
                    <CheckCircle className="w-4 h-4" />
                  ) : (
                    <IconComponent className="w-4 h-4" />
                  )}
                </div>
                <span className="text-xs font-medium hidden sm:block">{step.title}</span>
              </div>
              {index < steps.length - 1 && (
                <div className={`w-8 h-0.5 mx-2 ${
                  isCompleted ? 'bg-green-600' : 'bg-gray-200'
                }`} />
              )}
            </div>
          )
        })}
      </div>

      {/* Step 1: Shipping Address */}
      {currentStep === 1 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Shipping Address</h2>
          
          {addresses.map((address) => (
            <Card 
              key={address.id} 
              className={`cursor-pointer transition-colors ${
                selectedAddress?.id === address.id ? 'ring-2 ring-blue-500 bg-blue-50' : 'hover:bg-gray-50'
              }`}
              onClick={() => setSelectedAddress(address)}
            >
              <CardContent className="p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <Badge variant={address.type === 'home' ? 'default' : 'secondary'}>
                        {address.name}
                      </Badge>
                      {address.isDefault && (
                        <Badge variant="outline" className="text-xs">Default</Badge>
                      )}
                    </div>
                    <p className="font-medium text-gray-800">{address.fullName}</p>
                    <p className="text-sm text-gray-600">
                      {address.street}<br />
                      {address.city}, {address.state} {address.zipCode}<br />
                      {address.country}
                    </p>
                    <p className="text-sm text-gray-600 mt-1">{address.phone}</p>
                  </div>
                  <Button variant="ghost" size="sm">
                    <Edit className="w-4 h-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}

          <Button variant="outline" className="w-full">
            <Plus className="w-4 h-4 mr-2" />
            Add New Address
          </Button>
        </div>
      )}

      {/* Step 2: Payment Method */}
      {currentStep === 2 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Payment Method</h2>
          
          {paymentMethods.map((payment) => (
            <Card 
              key={payment.id} 
              className={`cursor-pointer transition-colors ${
                selectedPayment?.id === payment.id ? 'ring-2 ring-blue-500 bg-blue-50' : 'hover:bg-gray-50'
              }`}
              onClick={() => setSelectedPayment(payment)}
            >
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-6 bg-gray-200 rounded flex items-center justify-center">
                      {payment.type === 'card' && <CreditCard className="w-4 h-4" />}
                      {payment.type === 'paypal' && <Wallet className="w-4 h-4" />}
                      {payment.type === 'apple_pay' && <Smartphone className="w-4 h-4" />}
                    </div>
                    <div>
                      <p className="font-medium text-gray-800">{payment.name}</p>
                      {payment.type === 'card' && (
                        <p className="text-sm text-gray-600">
                          •••• •••• •••• {payment.last4} • {payment.expiryMonth}/{payment.expiryYear}
                        </p>
                      )}
                      {payment.type === 'paypal' && (
                        <p className="text-sm text-gray-600">{payment.email}</p>
                      )}
                    </div>
                  </div>
                  {payment.isDefault && (
                    <Badge variant="outline" className="text-xs">Default</Badge>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}

          <Button variant="outline" className="w-full">
            <Plus className="w-4 h-4 mr-2" />
            Add New Payment Method
          </Button>

          {/* Shipping Options */}
          <div className="mt-6">
            <h3 className="font-semibold mb-3">Shipping Options</h3>
            {shippingOptions.map((option) => {
              const IconComponent = option.icon
              return (
                <Card 
                  key={option.id} 
                  className={`cursor-pointer transition-colors mb-3 ${
                    selectedShipping?.id === option.id ? 'ring-2 ring-blue-500 bg-blue-50' : 'hover:bg-gray-50'
                  }`}
                  onClick={() => setSelectedShipping(option)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <IconComponent className="w-5 h-5 text-gray-600" />
                        <div>
                          <p className="font-medium text-gray-800">{option.name}</p>
                          <p className="text-sm text-gray-600">{option.description}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-medium text-gray-800">
                          {option.price === 0 ? 'FREE' : `$${option.price}`}
                        </p>
                        {option.estimatedDays === 'Today' && (
                          <Badge className="bg-green-100 text-green-800 text-xs">
                            Available
                          </Badge>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      )}

      {/* Step 3: Review Order */}
      {currentStep === 3 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Review Your Order</h2>
          
          {/* Order Items */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Order Items</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {cart.items.map((item) => (
                <div key={item.id} className="flex items-center space-x-3">
                  <div className="w-12 h-15 bg-gray-100 rounded flex items-center justify-center">
                    <Package className="w-4 h-4 text-gray-400" />
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-sm">{item.product.name}</p>
                    <p className="text-xs text-gray-600">
                      {item.variant.color} • Size {item.variant.size} • Qty {item.quantity}
                    </p>
                  </div>
                  <p className="font-medium">${item.product.price}</p>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Shipping Address */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center justify-between">
                <span>Shipping Address</span>
                <Button variant="ghost" size="sm" onClick={() => setCurrentStep(1)}>
                  <Edit className="w-4 h-4" />
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="font-medium">{selectedAddress?.fullName}</p>
              <p className="text-sm text-gray-600">
                {selectedAddress?.street}<br />
                {selectedAddress?.city}, {selectedAddress?.state} {selectedAddress?.zipCode}
              </p>
            </CardContent>
          </Card>

          {/* Payment & Shipping */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center justify-between">
                <span>Payment & Shipping</span>
                <Button variant="ghost" size="sm" onClick={() => setCurrentStep(2)}>
                  <Edit className="w-4 h-4" />
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Payment</span>
                <span className="text-sm font-medium">
                  {selectedPayment?.type === 'card' ? `•••• ${selectedPayment.last4}` : selectedPayment?.name}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Shipping</span>
                <span className="text-sm font-medium">{selectedShipping?.name}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Estimated Delivery</span>
                <span className="text-sm font-medium">{getEstimatedDeliveryDate()}</span>
              </div>
            </CardContent>
          </Card>

          {/* Promo Code */}
          <Card>
            <CardContent className="p-4">
              <div className="flex space-x-2">
                <Input
                  placeholder="Enter promo code"
                  value={promoCode}
                  onChange={(e) => setPromoCode(e.target.value)}
                  className="flex-1"
                />
                <Button onClick={applyPromoCode} variant="outline">
                  Apply
                </Button>
              </div>
              {promoApplied && (
                <div className="mt-2 flex items-center space-x-2 text-green-600">
                  <CheckCircle className="w-4 h-4" />
                  <span className="text-sm">Promo code {promoApplied.code} applied!</span>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}

      {/* Order Summary (always visible) */}
      <Card className="bg-gray-50">
        <CardHeader>
          <CardTitle className="text-base">Order Summary</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span>Subtotal</span>
            <span>${summary.subtotal}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span>Shipping</span>
            <span className={summary.shipping === 0 ? 'text-green-600' : ''}>
              {summary.shipping === 0 ? 'FREE' : `$${summary.shipping}`}
            </span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span>Tax</span>
            <span>${summary.tax}</span>
          </div>
          {summary.discount > 0 && (
            <div className="flex items-center justify-between text-sm text-green-600">
              <span>Discount</span>
              <span>-${summary.discount}</span>
            </div>
          )}
          <div className="border-t pt-3">
            <div className="flex items-center justify-between font-bold">
              <span>Total</span>
              <span>${summary.total}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex space-x-3">
        {currentStep > 1 && (
          <Button variant="outline" onClick={handlePreviousStep} className="flex-1">
            Back
          </Button>
        )}
        
        {currentStep < 3 ? (
          <Button onClick={handleNextStep} className="flex-1">
            Continue
            <ChevronRight className="w-4 h-4 ml-2" />
          </Button>
        ) : (
          <Button 
            onClick={processOrder} 
            disabled={isProcessing}
            className="flex-1 bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700"
          >
            {isProcessing ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                Processing...
              </>
            ) : (
              <>
                <Lock className="w-4 h-4 mr-2" />
                Place Order
              </>
            )}
          </Button>
        )}
      </div>

      {/* Security Badge */}
      <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
        <Shield className="w-4 h-4" />
        <span>Secure checkout powered by 256-bit SSL encryption</span>
      </div>
    </div>
  )
}

