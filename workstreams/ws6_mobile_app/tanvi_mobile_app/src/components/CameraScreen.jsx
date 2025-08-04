import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Camera, Sparkles } from 'lucide-react'

export default function CameraScreen({ currentUser }) {
  return (
    <div className="p-4 space-y-6">
      <div className="text-center py-6">
        <Camera className="w-16 h-16 text-purple-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Style Camera</h2>
        <p className="text-gray-600">Capture your outfit for AI styling</p>
      </div>
      
      <Card>
        <CardContent className="pt-6 text-center">
          <p className="text-gray-600 mb-4">Camera functionality coming soon!</p>
          <Button className="bg-gradient-to-r from-purple-500 to-pink-600">
            <Sparkles className="w-4 h-4 mr-2" />
            Enable Camera
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

