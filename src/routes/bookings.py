from flask import Blueprint, jsonify, request
from src.models.user import User, Slot, Booking, db
from src.utils.auth import token_required
from sqlalchemy.exc import IntegrityError

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/book', methods=['POST'])
@token_required
def book_slot(current_user):
    try:
        data = request.json
        
        # Validate required fields
        if not data or not data.get('slotId'):
            return jsonify({
                'error': {
                    'code': 'MISSING_SLOT_ID',
                    'message': 'Slot ID is required'
                }
            }), 400
        
        slot_id = data['slotId']
        
        # Check if slot exists
        slot = Slot.query.get(slot_id)
        if not slot:
            return jsonify({
                'error': {
                    'code': 'SLOT_NOT_FOUND',
                    'message': 'Slot not found'
                }
            }), 404
        
        # Check if slot is already booked
        existing_booking = Booking.query.filter_by(slot_id=slot_id).first()
        if existing_booking:
            return jsonify({
                'error': {
                    'code': 'SLOT_TAKEN',
                    'message': 'This slot is already booked'
                }
            }), 409
        
        # Create new booking
        booking = Booking(
            user_id=current_user.id,
            slot_id=slot_id
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'message': 'Slot booked successfully',
            'booking': booking.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'error': {
                'code': 'SLOT_TAKEN',
                'message': 'This slot is already booked'
            }
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': {
                'code': 'BOOKING_FAILED',
                'message': str(e)
            }
        }), 500

@bookings_bp.route('/my-bookings', methods=['GET'])
@token_required
def get_my_bookings(current_user):
    try:
        # Only patients can access their own bookings
        if current_user.role != 'patient':
            return jsonify({
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'Only patients can access their bookings'
                }
            }), 403
        
        bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
        
        return jsonify([booking.to_dict() for booking in bookings]), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'BOOKINGS_FETCH_FAILED',
                'message': str(e)
            }
        }), 500

@bookings_bp.route('/all-bookings', methods=['GET'])
@token_required
def get_all_bookings(current_user):
    try:
        # Only admins can access all bookings
        if current_user.role != 'admin':
            return jsonify({
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'Only admins can access all bookings'
                }
            }), 403
        
        bookings = Booking.query.order_by(Booking.created_at.desc()).all()
        
        return jsonify([booking.to_dict() for booking in bookings]), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'BOOKINGS_FETCH_FAILED',
                'message': str(e)
            }
        }), 500

