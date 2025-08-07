from flask import Blueprint, jsonify, request
from src.models.user import Slot, Booking, db
from datetime import datetime, timedelta

slots_bp = Blueprint('slots', __name__)

def generate_slots_for_date_range(start_date, end_date):
    """Generate 30-minute slots between 9:00-17:00 for the given date range"""
    slots = []
    current_date = start_date
    
    while current_date <= end_date:
        # Generate slots from 9:00 to 17:00 (30-minute intervals)
        for hour in range(9, 17):
            for minute in [0, 30]:
                slot_start = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                slot_end = slot_start + timedelta(minutes=30)
                
                # Check if slot already exists
                existing_slot = Slot.query.filter_by(start_at=slot_start).first()
                if not existing_slot:
                    slot = Slot(start_at=slot_start, end_at=slot_end)
                    slots.append(slot)
        
        current_date += timedelta(days=1)
    
    return slots

@slots_bp.route('/slots', methods=['GET'])
def get_slots():
    try:
        # Get query parameters
        from_date_str = request.args.get('from')
        to_date_str = request.args.get('to')
        
        # Default to next 7 days if no parameters provided
        if not from_date_str or not to_date_str:
            from_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = from_date + timedelta(days=7)
        else:
            try:
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
            except ValueError:
                return jsonify({
                    'error': {
                        'code': 'INVALID_DATE_FORMAT',
                        'message': 'Date format should be YYYY-MM-DD'
                    }
                }), 400
        
        # Generate slots if they don't exist
        new_slots = generate_slots_for_date_range(from_date, to_date)
        if new_slots:
            db.session.add_all(new_slots)
            db.session.commit()
        
        # Query available slots (not booked)
        slots = db.session.query(Slot).outerjoin(Booking).filter(
            Slot.start_at >= from_date,
            Slot.start_at <= to_date + timedelta(days=1),
            Booking.id.is_(None)  # Only slots without bookings
        ).order_by(Slot.start_at).all()
        
        return jsonify([slot.to_dict() for slot in slots]), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'SLOTS_FETCH_FAILED',
                'message': str(e)
            }
        }), 500

