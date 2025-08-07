import { useState, useEffect } from 'react'

const PatientDashboard = ({ user, onLogout }) => {
  const [slots, setSlots] = useState([])
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const fetchSlots = async () => {
    try {
      const response = await fetch('/api/slots')
      const data = await response.json()
      
      if (response.ok) {
        setSlots(data)
      } else {
        setError(data.error?.message || 'Failed to fetch slots')
      }
    } catch (error) {
      setError('Network error. Please try again.')
    }
  }

  const fetchBookings = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/my-bookings', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      const data = await response.json()
      
      if (response.ok) {
        setBookings(data)
      } else {
        setError(data.error?.message || 'Failed to fetch bookings')
      }
    } catch (error) {
      setError('Network error. Please try again.')
    }
  }

  useEffect(() => {
    fetchSlots()
    fetchBookings()
  }, [])

    const handleBookSlot = async (slotId) => {
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ slotId })
      })

      const data = await response.json()

      if (response.ok) {
        setSuccess('Slot booked successfully!')
        fetchSlots() // Refresh available slots
        fetchBookings() // Refresh user bookings
      } else {
        setError(data.error?.message || 'Failed to book slot')
      }
    } catch (error) {
      setError('Network error. Please try again.')
    }

    setLoading(false)
  }

  const handleCancelBooking = async (bookingId) => {
    if (!window.confirm('Are you sure you want to cancel this booking?')) {
      return
    }

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`/api/cancel/${bookingId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      const data = await response.json()

      if (response.ok) {
        setSuccess('Booking cancelled successfully!')
        fetchSlots() // Refresh available slots
        fetchBookings() // Refresh user bookings
      } else {
        setError(data.error?.message || 'Failed to cancel booking')
      }
    } catch (error) {
      setError('Network error. Please try again.')
    }

    setLoading(false)
  }

  const formatDateTime = (dateString) => {
    const date = new Date(dateString)
    return {
      date: date.toLocaleDateString(),
      time: date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="h-8 w-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                P
              </div>
              <div>
                <h1 className="text-xl font-semibold">Patient Dashboard</h1>
                <p className="text-sm text-gray-600">Welcome, {user.name}</p>
              </div>
            </div>
            <button
              onClick={onLogout}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Alerts */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}
        
        {success && (
          <div className="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
            {success}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Available Slots */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="p-6 border-b">
              <h2 className="text-lg font-semibold flex items-center space-x-2">
                <span>📅</span>
                <span>Available Slots</span>
              </h2>
              <p className="text-gray-600 mt-1">
                Book an appointment for the next 7 days
              </p>
            </div>
            <div className="p-6">
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {slots.length === 0 ? (
                  <p className="text-gray-500 text-center py-4">No available slots</p>
                ) : (
                  slots.map((slot) => {
                    const { date, time } = formatDateTime(slot.start_at)
                    return (
                      <div key={slot.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div className="flex items-center space-x-3">
                          <span className="text-gray-400">🕐</span>
                          <div>
                            <p className="font-medium">{date}</p>
                            <p className="text-sm text-gray-600">{time}</p>
                          </div>
                        </div>
                        <button
                          onClick={() => handleBookSlot(slot.id)}
                          disabled={loading}
                          className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 disabled:opacity-50"
                        >
                          Book
                        </button>
                      </div>
                    )
                  })
                )}
              </div>
            </div>
          </div>

          {/* My Bookings */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="p-6 border-b">
              <h2 className="text-lg font-semibold flex items-center space-x-2">
                <span>📅</span>
                <span>My Bookings</span>
              </h2>
              <p className="text-gray-600 mt-1">
                Your upcoming appointments
              </p>
            </div>
            <div className="p-6">
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {bookings.length === 0 ? (
                  <p className="text-gray-500 text-center py-4">No bookings yet</p>
                ) : (
                  bookings.map((booking) => {
                    const { date, time } = formatDateTime(booking.slot_start)
                    const isUpcoming = new Date(booking.slot_start) > new Date()
                    return (
                      <div key={booking.id} className="flex items-center justify-between p-3 border rounded-lg bg-blue-50">
                        <div className="flex items-center space-x-3">
                          <span className="text-blue-600">🕐</span>
                          <div>
                            <p className="font-medium">{date}</p>
                            <p className="text-sm text-gray-600">{time}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="px-2 py-1 bg-gray-200 text-gray-700 rounded text-xs">
                            {isUpcoming ? 'Booked' : 'Completed'}
                          </span>
                          {isUpcoming && (
                            <button
                              onClick={() => handleCancelBooking(booking.id)}
                              disabled={loading}
                              className="px-2 py-1 bg-red-600 text-white rounded text-xs hover:bg-red-700 disabled:opacity-50"
                            >
                              Cancel
                            </button>
                          )}
                        </div>
                      </div>
                    )
                  })
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PatientDashboard

