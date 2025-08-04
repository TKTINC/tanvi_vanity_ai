import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Shirt, Sparkles } from 'lucide-react'

export default function WardrobeScreen({ currentUser }) {
  return (
    <div className="p-4 space-y-6">
      <div className="text-center py-6">
        <Shirt className="w-16 h-16 text-purple-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800 mb-2">My Wardrobe</h2>
        <p className="text-gray-600">Manage your digital closet</p>
      </div>
      
      <Card>
        <CardContent className="pt-6 text-center">
          <p className="text-gray-600 mb-4">Wardrobe management coming soon!</p>
          <Button className="bg-gradient-to-r from-purple-500 to-pink-600">
            <Sparkles className="w-4 h-4 mr-2" />
            Add Items
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

