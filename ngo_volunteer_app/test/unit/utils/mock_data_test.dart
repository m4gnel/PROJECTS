import 'package:flutter_test/flutter_test.dart';
import 'package:ngo_volunteer_app/utils/mock_data.dart';

void main() {
  group('Mock Data Tests', () {
    test('Mock data contains all required events', () {
      final events = MockData.getAllEvents();
      expect(events, isNotEmpty);
      expect(events.length, greaterThanOrEqualTo(6));
    });

    test('Each mock event has required fields', () {
      final events = MockData.getAllEvents();

      for (var event in events) {
        expect(event.id, isNotEmpty);
        expect(event.name, isNotEmpty);
        expect(event.description, isNotEmpty);
        expect(event.location, isNotEmpty);
        expect(event.ngoName, isNotEmpty);
        expect(event.availableSlots, greaterThan(0));
        expect(event.imageUrl, isNotEmpty);
        expect(event.requirements, isNotEmpty);
        expect(event.latitude, isNotNull);
        expect(event.longitude, isNotNull);
      }
    });

    test('Get event by ID returns correct event', () {
      final events = MockData.getAllEvents();
      final firstEvent = events.first;

      final retrievedEvent = MockData.getEventById(firstEvent.id);

      expect(retrievedEvent, isNotNull);
      expect(retrievedEvent!.id, equals(firstEvent.id));
      expect(retrievedEvent.name, equals(firstEvent.name));
    });

    test('Get event by ID with invalid ID returns null', () {
      final event = MockData.getEventById('invalid_id_12345');
      expect(event, isNull);
    });

    test('Search events by name returns matching results', () {
      final results = MockData.searchEvents('Community');
      expect(results, isNotEmpty);

      for (var event in results) {
        expect(
          event.name.toLowerCase().contains('community') ||
              event.location.toLowerCase().contains('community') ||
              event.ngoName.toLowerCase().contains('community'),
          isTrue,
        );
      }
    });

    test('Search events is case-insensitive', () {
      final resultsLower = MockData.searchEvents('education');
      final resultsUpper = MockData.searchEvents('EDUCATION');
      final resultsMixed = MockData.searchEvents('Education');

      expect(resultsLower.length, equals(resultsUpper.length));
      expect(resultsLower.length, equals(resultsMixed.length));
    });

    test('Search events with empty query returns all events', () {
      final results = MockData.searchEvents('');
      final allEvents = MockData.getAllEvents();

      expect(results.length, equals(allEvents.length));
    });

    test('Filter events by city returns correct results', () {
      final mumbaiEvents = MockData.filterEventsByCity('Mumbai');
      expect(mumbaiEvents, isNotEmpty);

      for (var event in mumbaiEvents) {
        expect(event.location.toLowerCase().contains('mumbai'), isTrue);
      }
    });

    test('Filter events by city is case-insensitive', () {
      final resultsLower = MockData.filterEventsByCity('mumbai');
      final resultsUpper = MockData.filterEventsByCity('MUMBAI');
      final resultsMixed = MockData.filterEventsByCity('Mumbai');

      expect(resultsLower.length, equals(resultsUpper.length));
      expect(resultsLower.length, equals(resultsMixed.length));
    });

    test('Filter events by interest returns matching events', () {
      final educationEvents = MockData.filterEventsByInterest(['Education']);
      expect(educationEvents, isNotEmpty);

      for (var event in educationEvents) {
        expect(event.name, isNotEmpty);
      }
    });

    test('Mock events have valid locations', () {
      final events = MockData.getAllEvents();
      final indianCities = [
        'Mumbai',
        'Delhi',
        'Bangalore',
        'Chennai',
        'Pune',
        'Hyderabad',
        'Kolkata',
        'Ahmedabad',
      ];

      for (var event in events) {
        final isValidCity = indianCities.any(
          (city) => event.location.toLowerCase().contains(city.toLowerCase()),
        );
        expect(
          isValidCity,
          isTrue,
          reason: 'Event location should be in India',
        );
      }
    });

    test('Mock events have realistic NGO names', () {
      final events = MockData.getAllEvents();

      for (var event in events) {
        expect(event.ngoName.length, greaterThan(2));
        expect(event.ngoName.isEmpty, isFalse);
      }
    });
  });
}
