import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:ngo_volunteer_app/main.dart';

void main() {
  testWidgets('NGO Volunteer App launches successfully', (
    WidgetTester tester,
  ) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const NGOVolunteerApp());

    // Verify app title is displayed
    expect(
      find.text('NGO Volunteer Connect'),
      findsWidgets,
      reason: 'App title should be displayed somewhere in the app',
    );

    // Verify Material App is rendered
    expect(
      find.byType(MaterialApp),
      findsOneWidget,
      reason: 'MaterialApp should be the root widget',
    );

    // Pump the timer to let the splash screen delay complete (3 seconds + buffer)
    await tester.pumpAndSettle(const Duration(seconds: 5));

    // Verify no errors occurred during app startup
    expect(
      find.byType(Material),
      findsWidgets,
      reason: 'Material design widgets should be present',
    );
  });
}
