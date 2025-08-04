import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Package, Sparkles } from 'lucide-react'

export default function OrdersScreen({ currentUser }) {
  return (
    <div className="p-4 space-y-6">
      <div className="text-center py-6">
        <Package className="w-16 h-16 text-purple-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800 mb-2">My Orders</h2>
        <p className="text-gray-600">Track your purchases</p>
      </div>
      
      <Card>
        <CardContent className="pt-6 text-center">
          <p className="text-gray-600 mb-4">Order tracking coming soon!</p>
          <Button className="bg-gradient-to-r from-purple-500 to-pink-600">
            <Sparkles className="w-4 h-4 mr-2" />
            View Orders
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

