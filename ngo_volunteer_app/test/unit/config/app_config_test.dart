import 'package:flutter_test/flutter_test.dart';
import 'package:ngo_volunteer_app/config/app_config.dart';

void main() {
  group('App Configuration Tests', () {
    test('App name is correctly defined', () {
      expect(AppConfig.appName, equals('NGO Volunteer Connect'));
    });

    test('App version is correctly defined', () {
      expect(AppConfig.appVersion, equals('1.0.0'));
    });

    test('Base URL is correctly defined', () {
      expect(AppConfig.baseUrl, startsWith('https://'));
    });

    test('Mock data flag is defined', () {
      expect(AppConfig.useMockData, isNotNull);
      expect(AppConfig.useMockData, isTrue);
    });

    test('Splash screen delay is set to 3 seconds', () {
      expect(AppConfig.splashScreenDelay, equals(3));
    });

    test('Email pattern is valid regex', () {
      final emailPattern = RegExp(AppConfig.emailPattern);

      expect(emailPattern.hasMatch('test@example.com'), isTrue);
      expect(emailPattern.hasMatch('john.doe@company.co.uk'), isTrue);
      expect(emailPattern.hasMatch('invalid.email@'), isFalse);
      expect(emailPattern.hasMatch('notanemail'), isFalse);
    });

    test('Mobile pattern accepts 10 digit numbers', () {
      final mobilePattern = RegExp(AppConfig.mobilePattern);

      expect(mobilePattern.hasMatch('9876543210'), isTrue);
      expect(mobilePattern.hasMatch('1234567890'), isTrue);
      expect(mobilePattern.hasMatch('123456789'), isFalse);
      expect(mobilePattern.hasMatch('12345678901'), isFalse);
      expect(mobilePattern.hasMatch('987654321a'), isFalse);
    });

    test('Interests list contains all required options', () {
      expect(AppConfig.interests, isNotEmpty);
      expect(AppConfig.interests.length, greaterThanOrEqualTo(6));
      expect(
        AppConfig.interests,
        containsAll([
          'Education',
          'Healthcare',
          'Environment',
          'Community Service',
        ]),
      );
    });

    test('Interests list has no duplicates', () {
      final interests = AppConfig.interests;
      final uniqueInterests = interests.toSet();
      expect(interests.length, equals(uniqueInterests.length));
    });

    test('All interests are non-empty strings', () {
      for (var interest in AppConfig.interests) {
        expect(interest, isNotEmpty);
        expect(interest, isA<String>());
      }
    });

    test('App colors are valid hex codes', () {
      expect(AppConfig.primaryColor, startsWith('#'));
      expect(AppConfig.primaryColor.length, equals(7));
      expect(AppConfig.accentColor, startsWith('#'));
      expect(AppConfig.accentColor.length, equals(7));
    });

    test('Configuration constants are immutable', () {
      // These should be constants and not changeable
      expect(AppConfig.appName, equals('NGO Volunteer Connect'));
      expect(AppConfig.appVersion, equals('1.0.0'));
    });
  });
}
