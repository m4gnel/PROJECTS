import 'package:flutter_test/flutter_test.dart';
import 'package:ngo_volunteer_app/models/event.dart';

void main() {
  group('Event Model Tests', () {
    test('Event creation with all required fields', () {
      final eventDate = DateTime(2026, 7, 15, 10, 0);
      final event = Event(
        id: 'evt_001',
        name: 'Community Cleanup',
        description: 'Clean up the park',
        location: 'Central Park, Mumbai',
        eventDate: eventDate,
        ngoName: 'Green Earth',
        availableSlots: 50,
        requirements: ['Age 18+', 'Physical fitness'],
        imageUrl: 'https://example.com/event.png',
        latitude: 19.0760,
        longitude: 72.8777,
      );

      expect(event.id, equals('evt_001'));
      expect(event.name, equals('Community Cleanup'));
      expect(event.location, equals('Central Park, Mumbai'));
      expect(event.ngoName, equals('Green Earth'));
      expect(event.availableSlots, equals(50));
      expect(event.requirements.length, equals(2));
    });

    test('Event JSON serialization', () {
      final eventDate = DateTime(2026, 7, 20);
      final event = Event(
        id: 'evt_002',
        name: 'Education Support',
        description: 'Teach underprivileged children',
        location: 'Dharavi, Mumbai',
        eventDate: eventDate,
        ngoName: 'Education First',
        availableSlots: 30,
        requirements: ['Communication skills', 'Patience'],
        imageUrl: 'https://example.com/edu.png',
        latitude: 19.0176,
        longitude: 72.8498,
      );

      final json = event.toJson();

      expect(json['id'], equals('evt_002'));
      expect(json['name'], equals('Education Support'));
      expect(json['ngoName'], equals('Education First'));
      expect(json['availableSlots'], equals(30));
      expect(json['latitude'], equals(19.0176));
      expect(json['longitude'], equals(72.8498));
    });

    test('Event JSON deserialization', () {
      final json = {
        'id': 'evt_003',
        'name': 'Medical Camp',
        'description': 'Free health checkup',
        'location': 'Bangalore',
        'eventDate': '2026-08-01T09:00:00.000Z',
        'ngoName': 'Health Care Mission',
        'availableSlots': 100,
        'requirements': ['Medical training'],
        'imageUrl': 'https://example.com/medical.png',
        'latitude': 12.9716,
        'longitude': 77.5946,
      };

      final event = Event.fromJson(json);

      expect(event.id, equals('evt_003'));
      expect(event.name, equals('Medical Camp'));
      expect(event.availableSlots, equals(100));
      expect(event.requirements.length, equals(1));
    });

    test('Event copyWith updates specific fields', () {
      final original = Event(
        id: 'evt_004',
        name: 'Original Event',
        description: 'Description',
        location: 'Location',
        eventDate: DateTime.now(),
        ngoName: 'NGO Name',
        availableSlots: 50,
        requirements: [],
        imageUrl: 'url',
        latitude: 0.0,
        longitude: 0.0,
      );

      final updated = original.copyWith(
        availableSlots: 45,
        ngoName: 'Updated NGO',
      );

      expect(updated.id, equals(original.id));
      expect(updated.availableSlots, equals(45));
      expect(updated.ngoName, equals('Updated NGO'));
      expect(updated.name, equals(original.name));
    });

    test('Event round-trip serialization maintains data integrity', () {
      final eventDate = DateTime(2026, 8, 10, 14, 30);
      final original = Event(
        id: 'evt_005',
        name: 'Environment Event',
        description: 'Plant trees',
        location: 'Hyderabad',
        eventDate: eventDate,
        ngoName: 'Green Future',
        availableSlots: 75,
        requirements: ['Can work outdoors'],
        imageUrl: 'https://example.com/env.png',
        latitude: 17.3850,
        longitude: 78.4867,
      );

      final json = original.toJson();
      final deserialized = Event.fromJson(json);

      expect(deserialized.id, equals(original.id));
      expect(deserialized.name, equals(original.name));
      expect(deserialized.location, equals(original.location));
      expect(deserialized.availableSlots, equals(original.availableSlots));
      expect(deserialized.requirements, equals(original.requirements));
    });

    test('Event with multiple requirements serialization', () {
      final event = Event(
        id: 'evt_006',
        name: 'Disaster Relief',
        description: 'Help flood victims',
        location: 'Delhi',
        eventDate: DateTime.now(),
        ngoName: 'Relief Force',
        availableSlots: 200,
        requirements: [
          'Physical strength',
          'First aid training',
          'Leadership',
          'Team work',
        ],
        imageUrl: 'https://example.com/disaster.png',
        latitude: 28.7041,
        longitude: 77.1025,
      );

      final json = event.toJson();
      final deserialized = Event.fromJson(json);

      expect(deserialized.requirements.length, equals(4));
      expect(
        deserialized.requirements,
        containsAll([
          'Physical strength',
          'First aid training',
          'Leadership',
          'Team work',
        ]),
      );
    });
  });
}
