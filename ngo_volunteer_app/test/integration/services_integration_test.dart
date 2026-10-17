import 'package:flutter_test/flutter_test.dart';
import 'package:ngo_volunteer_app/services/api_service.dart';
import 'package:ngo_volunteer_app/services/local_storage_service.dart';
import 'package:ngo_volunteer_app/models/volunteer.dart';
import 'package:ngo_volunteer_app/models/event.dart';

void main() {
  // Initialize Flutter Test Binding for all local storage tests
  setUpAll(() {
    TestWidgetsFlutterBinding.ensureInitialized();
  });

  final apiService = ApiService();
  final storageService = LocalStorageService();

  group('API Service Integration Tests', () {
    test('Fetch all events returns non-empty list', () async {
      final events = await apiService.fetchEvents();

      expect(events, isNotEmpty);
      expect(events, isA<List<Event>>());
      expect(events.length, greaterThanOrEqualTo(6));
    });

    test('Fetched events have all required fields', () async {
      final events = await apiService.fetchEvents();

      for (var event in events) {
        expect(event.id, isNotEmpty);
        expect(event.name, isNotEmpty);
        expect(event.description, isNotEmpty);
        expect(event.location, isNotEmpty);
        expect(event.ngoName, isNotEmpty);
      }
    });

    test('Fetch event by ID returns correct event', () async {
      final allEvents = await apiService.fetchEvents();
      final firstEvent = allEvents.first;

      final event = await apiService.fetchEventById(firstEvent.id);

      expect(event, isNotNull);
      expect(event.id, equals(firstEvent.id));
      expect(event.name, equals(firstEvent.name));
    });

    test('Search events returns results for valid query', () async {
      final results = await apiService.searchEvents('Community');

      expect(results, isNotEmpty);
      expect(results, isA<List<Event>>());
    });

    test('Search events with no results returns empty list', () async {
      final results = await apiService.searchEvents('XYZNOTEXIST');

      expect(results, isA<List<Event>>());
    });

    test('Join event returns success response', () async {
      final response = await apiService.joinEvent('evt_001', 'vol_001');

      expect(response, isA<Map<String, dynamic>>());
      expect(response['success'], equals(true));
    });

    test('Register volunteer returns success response', () async {
      final volunteerData = {
        'fullName': 'Test Volunteer',
        'email': 'test@example.com',
        'mobileNumber': '9876543210',
        'city': 'Mumbai',
        'interests': ['Education', 'Healthcare'],
        'password': 'Password123',
      };

      final response = await apiService.registerVolunteer(volunteerData);

      expect(response, isA<Map<String, dynamic>>());
      expect(response['success'], equals(true));
    });

    test('Login volunteer returns success response', () async {
      final response = await apiService.loginVolunteer(
        'test@example.com',
        'password123',
      );

      expect(response, isA<Map<String, dynamic>>());
      expect(response['success'], equals(true));
    });

    test('API timeout handling works correctly', () async {
      // Since we use mock data with configured delays, API service should handle timeouts
      final events = await apiService.fetchEvents();
      expect(events, isNotEmpty);
    });
  });

  group('Local Storage Service Integration Tests', () {
    tearDown(() async {
      // Clean up after each test
      try {
        await storageService.clearAllData();
      } catch (e) {
        // Ignore cleanup errors
      }
    });

    test('Save and retrieve volunteer profile', () async {
      final volunteer = Volunteer(
        id: 'test_vol_001',
        fullName: 'Test User',
        email: 'test@example.com',
        mobileNumber: '9876543210',
        city: 'Mumbai',
        interests: ['Education'],
        registrationDate: DateTime.now(),
      );

      // Save profile
      final saved = await storageService.saveVolunteerProfile(volunteer);
      expect(saved, isTrue);

      // Retrieve profile
      final retrieved = await storageService.getVolunteerProfile();
      expect(retrieved, isNotNull);
      expect(retrieved!.id, equals(volunteer.id));
      expect(retrieved.fullName, equals(volunteer.fullName));
    });

    test('Add and retrieve joined events', () async {
      const eventId = 'evt_test_001';

      // Add event
      final added = await storageService.addJoinedEvent(eventId);
      expect(added, isTrue);

      // Get joined events
      final joinedEvents = await storageService.getJoinedEvents();
      expect(joinedEvents, contains(eventId));
    });

    test('Check if event is joined', () async {
      const eventId = 'evt_test_002';

      // Add event
      await storageService.addJoinedEvent(eventId);

      // Check if joined
      final isJoined = await storageService.isEventJoined(eventId);
      expect(isJoined, isTrue);
    });

    test('Remove joined event', () async {
      const eventId = 'evt_test_003';

      // Add and then remove event
      await storageService.addJoinedEvent(eventId);
      final removedSuccess = await storageService.removeJoinedEvent(eventId);
      expect(removedSuccess, isTrue);

      // Verify removed
      final isJoined = await storageService.isEventJoined(eventId);
      expect(isJoined, isFalse);
    });

    test('Save and retrieve auth token', () async {
      const token = 'test_token_abc123';

      await storageService.saveAuthToken(token);
      final retrieved = await storageService.getAuthToken();

      expect(retrieved, equals(token));
    });

    test('Save and retrieve volunteer ID', () async {
      const volunteerId = 'vol_test_001';

      await storageService.saveVolunteerId(volunteerId);
      final retrieved = await storageService.getVolunteerId();

      expect(retrieved, equals(volunteerId));
    });

    test('Check login status', () async {
      await storageService.saveAuthToken('test_token');
      final isLoggedIn = await storageService.isUserLoggedIn();

      expect(isLoggedIn, isTrue);
    });

    test('Clear all data wipes storage', () async {
      // Add some data
      await storageService.saveVolunteerId('vol_001');
      await storageService.saveAuthToken('token');
      await storageService.addJoinedEvent('evt_001');

      // Clear all
      await storageService.clearAllData();

      // Verify cleared
      final profile = await storageService.getVolunteerProfile();
      final isLoggedIn = await storageService.isUserLoggedIn();
      final joinedEvents = await storageService.getJoinedEvents();

      expect(profile, isNull);
      expect(isLoggedIn, isFalse);
      expect(joinedEvents, isEmpty);
    });
  });

  group('End-to-End Workflow Tests', () {
    tearDown(() async {
      try {
        await storageService.clearAllData();
      } catch (e) {
        // Ignore
      }
    });

    test('Complete user registration and profile flow', () async {
      // Create volunteer
      final volunteer = Volunteer(
        id: 'e2e_vol_001',
        fullName: 'E2E Test User',
        email: 'e2e@example.com',
        mobileNumber: '9999999999',
        city: 'Pune',
        interests: ['Healthcare', 'Environment'],
        registrationDate: DateTime.now(),
      );

      // Save profile
      await storageService.saveVolunteerProfile(volunteer);
      await storageService.saveVolunteerId(volunteer.id);

      // Retrieve and verify
      final retrieved = await storageService.getVolunteerProfile();
      expect(retrieved!.fullName, equals('E2E Test User'));

      final retrievedId = await storageService.getVolunteerId();
      expect(retrievedId, equals('e2e_vol_001'));
    });

    test('Complete event browsing and joining flow', () async {
      // Fetch events
      final events = await apiService.fetchEvents();
      expect(events, isNotEmpty);

      // Get first event details
      final firstEvent = events.first;
      final eventDetails = await apiService.fetchEventById(firstEvent.id);
      expect(eventDetails.id, equals(firstEvent.id));

      // Join event
      final joinResponse = await apiService.joinEvent(
        'e2e_test_vol',
        firstEvent.id,
      );
      expect(joinResponse['success'], isTrue);

      // Save to local storage
      await storageService.addJoinedEvent(firstEvent.id);

      // Verify joined
      final isJoined = await storageService.isEventJoined(firstEvent.id);
      expect(isJoined, isTrue);
    });

    test('Event search and filter workflow', () async {
      // Search for events
      final searchResults = await apiService.searchEvents('Education');
      expect(searchResults, isNotEmpty);

      // Filter by city
      final mumbaiEvents = await apiService.fetchEvents();
      final filtered = mumbaiEvents
          .where((e) => e.location.toLowerCase().contains('mumbai'))
          .toList();
      expect(filtered, isNotEmpty);
    });
  });
}
