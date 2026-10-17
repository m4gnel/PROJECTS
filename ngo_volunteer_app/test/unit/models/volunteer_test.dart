import 'package:flutter_test/flutter_test.dart';
import 'package:ngo_volunteer_app/models/volunteer.dart';

void main() {
  group('Volunteer Model Tests', () {
    test('Volunteer creation with required fields', () {
      final volunteer = Volunteer(
        id: 'vol_001',
        fullName: 'John Doe',
        email: 'john@example.com',
        mobileNumber: '9876543210',
        city: 'Mumbai',
        interests: ['Education', 'Healthcare'],
        registrationDate: DateTime.now(),
      );

      expect(volunteer.id, equals('vol_001'));
      expect(volunteer.fullName, equals('John Doe'));
      expect(volunteer.email, equals('john@example.com'));
      expect(volunteer.mobileNumber, equals('9876543210'));
      expect(volunteer.city, equals('Mumbai'));
      expect(volunteer.interests, containsAll(['Education', 'Healthcare']));
    });

    test('Volunteer JSON serialization', () {
      final now = DateTime.now();
      final volunteer = Volunteer(
        id: 'vol_001',
        fullName: 'Jane Smith',
        email: 'jane@example.com',
        mobileNumber: '9876543211',
        city: 'Delhi',
        interests: ['Environment'],
        registrationDate: now,
      );

      final json = volunteer.toJson();

      expect(json['id'], equals('vol_001'));
      expect(json['fullName'], equals('Jane Smith'));
      expect(json['email'], equals('jane@example.com'));
      expect(json['mobileNumber'], equals('9876543211'));
      expect(json['city'], equals('Delhi'));
      expect(json['interests'], equals(['Environment']));
      expect(json['registrationDate'], equals(now.toIso8601String()));
    });

    test('Volunteer JSON deserialization', () {
      final json = {
        'id': 'vol_002',
        'fullName': 'Bob Johnson',
        'email': 'bob@example.com',
        'mobileNumber': '9876543212',
        'city': 'Bangalore',
        'interests': ['Healthcare', 'Community Service'],
        'registrationDate': '2026-06-01T10:30:00.000Z',
      };

      final volunteer = Volunteer.fromJson(json);

      expect(volunteer.id, equals('vol_002'));
      expect(volunteer.fullName, equals('Bob Johnson'));
      expect(volunteer.email, equals('bob@example.com'));
      expect(volunteer.mobileNumber, equals('9876543212'));
      expect(volunteer.city, equals('Bangalore'));
      expect(volunteer.interests.length, equals(2));
    });

    test('Volunteer copyWith creates new instance with updated values', () {
      final original = Volunteer(
        id: 'vol_003',
        fullName: 'Alice Brown',
        email: 'alice@example.com',
        mobileNumber: '9876543213',
        city: 'Chennai',
        interests: ['Education'],
        registrationDate: DateTime.now(),
      );

      final updated = original.copyWith(
        city: 'Pune',
        interests: ['Education', 'Healthcare'],
      );

      expect(updated.id, equals(original.id));
      expect(updated.fullName, equals(original.fullName));
      expect(updated.city, equals('Pune'));
      expect(updated.interests, equals(['Education', 'Healthcare']));
    });

    test('Volunteer round-trip serialization', () {
      final original = Volunteer(
        id: 'vol_004',
        fullName: 'Carol Davis',
        email: 'carol@example.com',
        mobileNumber: '9876543214',
        city: 'Hyderabad',
        interests: ['Environment', 'Disaster Relief'],
        registrationDate: DateTime.now(),
      );

      final json = original.toJson();
      final deserialized = Volunteer.fromJson(json);

      expect(deserialized.id, equals(original.id));
      expect(deserialized.fullName, equals(original.fullName));
      expect(deserialized.email, equals(original.email));
      expect(deserialized.city, equals(original.city));
      expect(deserialized.interests, equals(original.interests));
    });
  });
}
