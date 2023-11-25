from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app = Flask(__name__)
# password = 'password'
# db_name = "as_db2"
# db_username = "root"
# db_link = "localhost:3306"
mysql_url = os.environ.get('mysql_url')
# MySQL database connection URL
# database_url = f'mysql+mysqlconnector://{db_username}:{password}@{db_link}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the models
class User(db.Model):
    __tablename__ = "USER"
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    given_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50))
    phone_number = db.Column(db.String(15))
    profile_description = db.Column(db.Text)
    password = db.Column(db.String(255), nullable=False)

class Caregiver(db.Model):
    __tablename__ = "CAREGIVER"
    caregiver_user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), primary_key=True)
    photo = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.String(10))
    caregiving_type = db.Column(db.String(50))
    hourly_rate = db.Column(db.Float)

class Member(db.Model):
    __tablename__ = "MEMBER"
    member_user_id = db.Column(db.Integer, db.ForeignKey('MEMBER.member_user_id'), primary_key=True)
    house_rules = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)

class Address(db.Model):
    __tablename__ = "ADDRESS"
    member_user_id = db.Column(db.Integer, db.ForeignKey('MEMBER.member_user_id'), primary_key=True)
    house_number = db.Column(db.String(50))
    street = db.Column(db.String(50))
    town = db.Column(db.String(50))

class Job(db.Model):
    __tablename__ = "JOB"
    job_id = db.Column(db.Integer, primary_key=True)
    member_user_id = db.Column(db.Integer, db.ForeignKey('MEMBER.member_user_id'), nullable=False)
    required_caregiving_type = db.Column(db.String(50))
    other_requirements = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

class JobApplication(db.Model):
    __tablename__ = "JOB_APPLICATION"
    caregiver_user_id = db.Column(db.Integer, db.ForeignKey('CAREGIVER.caregiver_user_id'), primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'), primary_key=True)
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    __tablename__ = "APPOINTMENT"
    appointment_id = db.Column(db.Integer, primary_key=True)
    caregiver_user_id = db.Column(db.Integer, db.ForeignKey('CAREGIVER.caregiver_user_id'), nullable=False)
    member_user_id = db.Column(db.Integer, db.ForeignKey('member.member_user_id'), nullable=False)
    appointment_date = db.Column(db.Date)
    appointment_time = db.Column(db.Time)
    work_hours = db.Column(db.Float)
    status = db.Column(db.String(20))

# CRUD operations routes

# Create operations
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        email=data['email'],
        given_name=data['given_name'],
        surname=data['surname'],
        city=data['city'],
        phone_number=data['phone_number'],
        profile_description=data['profile_description'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/caregivers', methods=['POST'])
def create_caregiver():
    data = request.json
    new_caregiver = Caregiver(
        photo=data['photo'],
        gender=data['gender'],
        caregiving_type=data['caregiving_type'],
        hourly_rate=data['hourly_rate'],
        user_id=data['user_id']
    )
    db.session.add(new_caregiver)
    db.session.commit()
    return jsonify({'message': 'Caregiver created successfully'})

@app.route('/members', methods=['POST'])
def create_member():
    data = request.json
    new_member = Member(
        house_rules=data['house_rules'],
        member_user_id=data['member_user_id']
    )
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'Member created successfully'})

@app.route('/addresses', methods=['POST'])
def create_address():
    data = request.json
    new_address = Address(
        member_user_id=data['member_user_id'],
        house_number=data['house_number'],
        street=data['street'],
        town=data['town']
    )
    db.session.add(new_address)
    db.session.commit()
    return jsonify({'message': 'Address created successfully'})

@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.json
    new_job = Job(
        member_user_id=data['member_user_id'],
        required_caregiving_type=data['required_caregiving_type'],
        other_requirements=data['other_requirements']
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify({'message': 'Job created successfully'})

@app.route('/job_applications', methods=['POST'])
def create_job_application():
    data = request.json
    new_job_application = JobApplication(
        caregiver_user_id=data['caregiver_user_id'],
        job_id=data['job_id']
    )
    db.session.add(new_job_application)
    db.session.commit()
    return jsonify({'message': 'Job application created successfully'})

@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    new_appointment = Appointment(
        caregiver_user_id=data['caregiver_user_id'],
        member_user_id=data['member_user_id'],
        appointment_date=data['appointment_date'],
        appointment_time=data['appointment_time'],
        work_hours=data['work_hours'],
        status=data['status']
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment created successfully'})



#Read operations
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'user_id': user.user_id, 'email': user.email, 'given_name': user.given_name,
                  'surname': user.surname, 'city': user.city, 'phone_number': user.phone_number,
                  'profile_description': user.profile_description, 'password': user.password}
                 for user in users]
    return jsonify(user_list)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {'user_id': user.user_id, 'email': user.email, 'given_name': user.given_name,
                     'surname': user.surname, 'city': user.city, 'phone_number': user.phone_number,
                     'profile_description': user.profile_description, 'password': user.password}
        return jsonify(user_data)
    return jsonify({'message': 'User not found'}), 404

@app.route('/caregivers', methods=['GET'])
def get_caregivers():
    caregivers = Caregiver.query.all()
    caregiver_list = [{'caregiver_user_id': caregiver.caregiver_user_id, 'photo': caregiver.photo,
                       'gender': caregiver.gender, 'caregiving_type': caregiver.caregiving_type,
                       'hourly_rate': caregiver.hourly_rate}
                      for caregiver in caregivers]
    return jsonify(caregiver_list)

@app.route('/caregivers/<int:caregiver_user_id>', methods=['GET'])
def get_caregiver(caregiver_user_id):
    caregiver = Caregiver.query.get(caregiver_user_id)
    if caregiver:
        caregiver_data = {'caregiver_user_id': caregiver.caregiver_user_id, 'photo': caregiver.photo,
                          'gender': caregiver.gender, 'caregiving_type': caregiver.caregiving_type,
                          'hourly_rate': caregiver.hourly_rate, 'user_id': caregiver.user_id}
        return jsonify(caregiver_data)
    return jsonify({'message': 'Caregiver not found'}), 404

@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    member_list = [{'member_user_id': member.member_user_id, 'house_rules': member.house_rules,
                    'user_id': member.user_id} for member in members]
    return jsonify(member_list)

@app.route('/members/<int:member_user_id>', methods=['GET'])
def get_member(member_user_id):
    member = Member.query.get(member_user_id)
    if member:
        member_data = {'member_user_id': member.member_user_id, 'house_rules': member.house_rules,
                       'user_id': member.user_id}
        return jsonify(member_data)
    return jsonify({'message': 'Member not found'}), 404

@app.route('/addresses', methods=['GET'])
def get_addresses():
    addresses = Address.query.all()
    address_list = [{'member_user_id': address.member_user_id, 'house_number': address.house_number,
                      'street': address.street, 'town': address.town} for address in addresses]
    return jsonify(address_list)

@app.route('/addresses/<int:member_user_id>', methods=['GET'])
def get_address(member_user_id):
    address = Address.query.get(member_user_id)
    if address:
        address_data = {'member_user_id': address.member_user_id, 'house_number': address.house_number,
                        'street': address.street, 'town': address.town}
        return jsonify(address_data)
    return jsonify({'message': 'Address not found'}), 404

@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    job_list = [{'job_id': job.job_id, 'member_user_id': job.member_user_id,
                  'required_caregiving_type': job.required_caregiving_type,
                  'other_requirements': job.other_requirements, 'date_posted': job.date_posted}
                 for job in jobs]
    return jsonify(job_list)

@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get(job_id)
    if job:
        job_data = {'job_id': job.job_id, 'member_user_id': job.member_user_id,
                    'required_caregiving_type': job.required_caregiving_type,
                    'other_requirements': job.other_requirements, 'date_posted': job.date_posted}
        return jsonify(job_data)
    return jsonify({'message': 'Job not found'}), 404

@app.route('/job_applications', methods=['GET'])
def get_job_applications():
    job_applications = JobApplication.query.all()
    job_application_list = [{'caregiver_user_id': ja.caregiver_user_id, 'job_id': ja.job_id,
                              'date_applied': ja.date_applied} for ja in job_applications]
    return jsonify(job_application_list)

@app.route('/job_applications/<int:caregiver_user_id>/<int:job_id>', methods=['GET'])
def get_job_application(caregiver_user_id, job_id):
    job_application = JobApplication.query.get((caregiver_user_id, job_id))
    if job_application:
        job_application_data = {'caregiver_user_id': job_application.caregiver_user_id,
                                 'job_id': job_application.job_id, 'date_applied': job_application.date_applied}
        return jsonify(job_application_data)
    return jsonify({'message': 'Job Application not found'}), 404

@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    appointment_list = [{'appointment_id': a.appointment_id, 'caregiver_user_id': a.caregiver_user_id,
                          'member_user_id': a.member_user_id, 'appointment_date': a.appointment_date,
                          'appointment_time': a.appointment_time, 'work_hours': a.work_hours,
                          'status': a.status} for a in appointments]
    return jsonify(appointment_list)

@app.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        appointment_data = {'appointment_id': appointment.appointment_id,
                             'caregiver_user_id': appointment.caregiver_user_id,
                             'member_user_id': appointment.member_user_id,
                             'appointment_date': appointment.appointment_date,
                             'appointment_time': appointment.appointment_time,
                             'work_hours': appointment.work_hours, 'status': appointment.status}
        return jsonify(appointment_data)
    return jsonify({'message': 'Appointment not found'}), 404

# Update operations
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.json
        user.email = data['email']
        user.given_name = data['given_name']
        user.surname = data['surname']
        user.city = data['city']
        user.phone_number = data['phone_number']
        user.profile_description = data['profile_description']
        user.password = data['password']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    return jsonify({'message': 'User not found'}), 404

@app.route('/caregivers/<int:caregiver_user_id>', methods=['PUT'])
def update_caregiver(caregiver_user_id):
    caregiver = Caregiver.query.get(caregiver_user_id)
    if caregiver:
        data = request.json
        caregiver.photo = data['photo']
        caregiver.gender = data['gender']
        caregiver.caregiving_type = data['caregiving_type']
        caregiver.hourly_rate = data['hourly_rate']
        caregiver.user_id = data['user_id']
        db.session.commit()
        return jsonify({'message': 'Caregiver updated successfully'})
    return jsonify({'message': 'Caregiver not found'}), 404

@app.route('/members/<int:member_user_id>', methods=['PUT'])
def update_member(member_user_id):
    member = Member.query.get(member_user_id)
    if member:
        data = request.json
        member.house_rules = data['house_rules']
        member.user_id = data['user_id']
        db.session.commit()
        return jsonify({'message': 'Member updated successfully'})
    return jsonify({'message': 'Member not found'}), 404

@app.route('/addresses/<int:member_user_id>', methods=['PUT'])
def update_address(member_user_id):
    address = Address.query.get(member_user_id)
    if address:
        data = request.json
        address.house_number = data['house_number']
        address.street = data['street']
        address.town = data['town']
        db.session.commit()
        return jsonify({'message': 'Address updated successfully'})
    return jsonify({'message': 'Address not found'}), 404

@app.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get(job_id)
    if job:
        data = request.json
        job.member_user_id = data['member_user_id']
        job.required_caregiving_type = data['required_caregiving_type']
        job.other_requirements = data['other_requirements']
        db.session.commit()
        return jsonify({'message': 'Job updated successfully'})
    return jsonify({'message': 'Job not found'}), 404

@app.route('/job_applications/<int:caregiver_user_id>/<int:job_id>', methods=['PUT'])
def update_job_application(caregiver_user_id, job_id):
    job_application = JobApplication.query.get((caregiver_user_id, job_id))
    if job_application:
        data = request.json
        job_application.date_applied = data['date_applied']
        db.session.commit()
        return jsonify({'message': 'Job application updated successfully'})
    return jsonify({'message': 'Job application not found'}), 404

@app.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        data = request.json
        appointment.caregiver_user_id = data['caregiver_user_id']
        appointment.member_user_id = data['member_user_id']
        appointment.appointment_date = data['appointment_date']
        appointment.appointment_time = data['appointment_time']
        appointment.work_hours = data['work_hours']
        appointment.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Appointment updated successfully'})
    return jsonify({'message': 'Appointment not found'}), 404

# Delete operations
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'message': 'User not found'}), 404

@app.route('/caregivers/<int:caregiver_user_id>', methods=['DELETE'])
def delete_caregiver(caregiver_user_id):
    caregiver = Caregiver.query.get(caregiver_user_id)
    if caregiver:
        db.session.delete(caregiver)
        db.session.commit()
        return jsonify({'message': 'Caregiver deleted successfully'})
    return jsonify({'message': 'Caregiver not found'}), 404

@app.route('/members/<int:member_user_id>', methods=['DELETE'])
def delete_member(member_user_id):
    member = Member.query.get(member_user_id)
    if member:
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Member deleted successfully'})
    return jsonify({'message': 'Member not found'}), 404

@app.route('/addresses/<int:member_user_id>', methods=['DELETE'])
def delete_address(member_user_id):
    address = Address.query.get(member_user_id)
    if address:
        db.session.delete(address)
        db.session.commit()
        return jsonify({'message': 'Address deleted successfully'})
    return jsonify({'message': 'Address not found'}), 404

@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if job:
        db.session.delete(job)
        db.session.commit()
        return jsonify({'message': 'Job deleted successfully'})
    return jsonify({'message': 'Job not found'}), 404

@app.route('/job_applications/<int:caregiver_user_id>/<int:job_id>', methods=['DELETE'])
def delete_job_application(caregiver_user_id, job_id):
    job_application = JobApplication.query.get((caregiver_user_id, job_id))
    if job_application:
        db.session.delete(job_application)
        db.session.commit()
        return jsonify({'message': 'Job application deleted successfully'})
    return jsonify({'message': 'Job application not found'}), 404

@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted successfully'})
    return jsonify({'message': 'Appointment not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
