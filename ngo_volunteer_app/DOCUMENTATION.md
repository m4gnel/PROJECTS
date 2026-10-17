# NGO Volunteer Connect Mobile Application

## Overview

**NGO Volunteer Connect** is a mobile application built with Flutter that helps NGOs manage volunteers and community service events. The app bridges the gap between NGOs and volunteers by making it easy to discover upcoming events, understand volunteer requirements, and manage registrations.

## Problem Statement

Many NGOs struggle to:
- Organize volunteers efficiently
- Communicate upcoming events to interested volunteers
- Track event locations and volunteer requirements
- Manage volunteer registrations and participation status

This application solves these problems by providing a centralized platform for event discovery and volunteer management.

## Key Features

✅ **Volunteer Registration** - Complete profile creation with interests and location
✅ **Event Discovery** - Browse all upcoming volunteer events with detailed information
✅ **Smart Search & Filtering** - Find events by name, location, or NGO
✅ **Event Details** - View comprehensive event information including requirements
✅ **Join Events** - Register for events with confirmation
✅ **Profile Management** - View and edit volunteer profile information
✅ **Local Storage** - Save profile and event preferences offline
✅ **Responsive Design** - Works seamlessly on all screen sizes
✅ **Error Handling** - Graceful error states with retry functionality
✅ **Loading States** - Professional loading indicators during data fetch

## Technical Architecture

### Layers

```
┌─────────────────────────────────────┐
│     Flutter UI Screens              │
├─────────────────────────────────────┤
│     Services Layer                  │
│  (API, Storage, Business Logic)     │
├─────────────────────────────────────┤
│     Models Layer                    │
│  (Data structures)                  │
├─────────────────────────────────────┤
│     Local Storage (SharedPreferences)
│     & Mock Data                     │
└─────────────────────────────────────┘
```

### Technology Stack

- **Framework**: Flutter 3.x
- **Language**: Dart
- **State Management**: StatefulWidget with setState()
- **Networking**: HTTP package (with mock data support)
- **Storage**: SharedPreferences
- **UI**: Material Design 3

## Project Structure

```
lib/
├── config/
│   └── app_config.dart              # App constants and configuration
│
├── models/
│   ├── volunteer.dart               # Volunteer data model
│   └── event.dart                   # Event data model
│
├── services/
│   ├── api_service.dart             # API integration (mock & real)
│   └── local_storage_service.dart   # SharedPreferences wrapper
│
├── screens/
│   ├── splash_screen.dart           # App startup screen
│   ├── login_screen.dart            # User login
│   ├── register_screen.dart         # Volunteer registration
│   ├── home_screen.dart             # Events listing with search
│   ├── event_details_screen.dart    # Event details and join
│   ├── profile_screen.dart          # Volunteer profile
│   └── edit_profile_screen.dart     # Edit profile information
│
├── widgets/
│   ├── event_card.dart              # Event list item widget
│   └── loading_widget.dart          # Loading/Error/Skeleton widgets
│
├── utils/
│   └── mock_data.dart               # Mock events for testing
│
└── main.dart                        # App entry point and routing
```

## Learning Objectives

By completing this application, you'll understand:

### Flutter Fundamentals
- StatefulWidget vs StatelessWidget
- Widget composition and reusability
- Build methods and rendering

### Navigation & Routing
- Named routes in Flutter
- Passing data between screens via ModalRoute
- Navigation stack management (pushNamed, pushReplacementNamed)

### Form Management
- TextFormField widgets
- Form validation with validators
- Form state management

### State Management
- setState() for local state
- FutureBuilder for async operations
- State persistence across app lifecycle

### API Integration
- HTTP requests (GET, POST)
- JSON parsing and serialization
- Error handling and timeouts
- Mock data for testing

### Local Storage
- SharedPreferences for key-value storage
- Serialization/Deserialization
- Persistence patterns

### UI/UX Patterns
- Loading states and spinners
- Error states with retry
- Empty states
- Search and filtering

## Application Flow

```
┌──────────────────┐
│  Splash Screen   │  (3 second delay)
│  ↓               │
├──────────────────┤
│  Login/Register  │  (Authentication)
│  ↓               │
├──────────────────┤
│  Events Listing  │  (Browse & Search)
│  ↓               │
├──────────────────┤
│  Event Details   │  (View & Join)
│  ↓               │
├──────────────────┤
│  Profile Mgmt    │  (View Joined Events)
└──────────────────┘
```

## How to Use

### 1. Register as a Volunteer

1. Launch the app → Login Screen appears
2. Click "Sign Up" to register
3. Fill in your details:
   - Full Name
   - Email Address
   - Mobile Number (10 digits)
   - City
   - Select at least 2 interests
4. Click "Register"
5. Automatically logged in and taken to Events screen

### 2. Browse & Search Events

1. From Home Screen, view all available events
2. Use search bar to find events by:
   - Event name
   - Location
   - NGO name
3. Scroll to see more events

### 3. View Event Details

1. Tap any event card
2. See complete event information:
   - Event description
   - Date & time
   - Location with coordinates
   - NGO name
   - Available slots
   - Requirements checklist
3. Click "Join Event" to register

### 4. Manage Profile

1. Tap profile icon (top-right in Home Screen)
2. View all profile information
3. Click "Edit Profile" to update details
4. View list of events you've joined

## Form Validation Rules

### Registration Form
- **Full Name**: Minimum 3 characters
- **Email**: Valid email format (RFC 5322)
- **Mobile**: Exactly 10 digits
- **City**: Required, non-empty
- **Interests**: At least 1 required
- **Password**: Minimum 6 characters
- **Confirm Password**: Must match password

### Login Form
- **Email**: Valid email format
- **Password**: Non-empty

### Profile Edit Form
- Same validation rules as registration

## Local Storage

### Data Stored

1. **Volunteer Profile**
   - Full name, email, phone
   - City, interests
   - Registration date

2. **Authentication**
   - Auth token
   - Volunteer ID

3. **Event Participation**
   - List of joined event IDs

### Storage Methods

- **Key**: `volunteer_profile` → Volunteer JSON
- **Key**: `events_joined` → List of event IDs
- **Key**: `auth_token` → Authentication token
- **Key**: `volunteer_id` → Current user ID

## API Integration

### Base URL
```
https://api.ngo-volunteer.com/api
```

### Endpoints (Currently using mock data)

1. **GET /events** - List all events
2. **GET /events/:id** - Get event details
3. **POST /events/:id/join** - Join an event
4. **POST /volunteers/register** - Register volunteer
5. **POST /volunteers/login** - Login volunteer
6. **GET /events/search?query=** - Search events

### Mock Data

Currently using 6 hardcoded events with:
- Event titles, descriptions
- Actual city locations
- Variable date/times
- NGO names
- Requirements lists
- Placeholder images

**To switch to real API**: Change `useMockData = false` in `app_config.dart`

## Error Handling

### Implemented Patterns

1. **Try-Catch Blocks**
   ```dart
   try {
     final data = await apiService.fetchData();
   } catch (e) {
     setState(() => _error = e.toString());
   }
   ```

2. **Mounted Check**
   ```dart
   if (mounted) {
     setState(() { ... });
   }
   ```

3. **User Feedback**
   - SnackBars for alerts
   - Dialog boxes for confirmations
   - Error screens with retry buttons

### Error Scenarios

- Network timeouts (10 second timeout)
- Invalid form input (validation feedback)
- Missing authentication (redirect to login)
- Event not found (display error message)
- Storage failures (exception handling)

## Code Quality Standards

### Applied Best Practices

1. **Naming Conventions**
   - PascalCase for classes and files
   - camelCase for variables and functions
   - Private members with underscore prefix

2. **Code Organization**
   - Single responsibility per class
   - Clear separation of concerns
   - Reusable widgets

3. **Widget Patterns**
   - StatelessWidget for UI-only widgets
   - StatefulWidget for stateful features
   - Proper lifecycle management (initState, dispose)

4. **Comments & Documentation**
   - Descriptive variable names
   - Method documentation
   - Inline comments for complex logic

## Deployment

### Building APK

```bash
# For debug APK
flutter build apk --debug

# For release APK
flutter build apk --release
```

### Building for Other Platforms

```bash
# iOS
flutter build ios

# Web
flutter build web

# Windows
flutter build windows
```

## Testing the Application

### Test Scenarios

1. **Authentication Flow**
   - Register with new account
   - Login with credentials
   - Verify profile persistence

2. **Event Discovery**
   - Search events by name
   - Search events by location
   - Verify event count

3. **Event Participation**
   - Join multiple events
   - Verify joined events in profile
   - Attempt to join same event twice

4. **Data Persistence**
   - Register and close app
   - Reopen app and verify profile
   - Joined events should persist

5. **Error Scenarios**
   - Invalid email format
   - Invalid mobile number
   - Password mismatch
   - Network timeout

## Dependencies

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0              # Network requests
  shared_preferences: ^2.2.2 # Local storage
  cupertino_icons: ^1.0.8   # iOS icons
```

## Future Enhancements

1. **Advanced State Management**
   - Provider package integration
   - BLoC pattern implementation
   - Riverpod for reactive programming

2. **Database**
   - Hive for structured local storage
   - SQLite for complex queries
   - Cloud Firestore integration

3. **Features**
   - Push notifications for events
   - Event ratings and reviews
   - Volunteer hours tracking
   - Event maps with location tracking
   - Payment integration
   - Volunteer certificates

4. **Performance**
   - Image caching
   - Lazy loading
   - Database indexing
   - Code splitting

5. **Security**
   - JWT token refresh
   - End-to-end encryption
   - Secure storage
   - Biometric authentication

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Null pointer exceptions | Use null coalescing operator (??) and null safety checks |
| State not updating | Ensure setState() is called and mounted check is used |
| Navigation errors | Verify route names and arguments types |
| SharedPreferences not working | Ensure try-catch is implemented for all storage operations |
| Network timeouts | Increase timeout duration or check network connectivity |

## Support & Resources

- **Flutter Docs**: https://flutter.dev/docs
- **Dart Docs**: https://dart.dev/guides
- **Material Design**: https://material.io/design
- **Community**: https://www.flutter.dev/community

## License

This project is for educational purposes as part of the NGO Volunteer Management task.

---

**Version**: 1.0.0
**Last Updated**: 2026-06-09
**Status**: ✅ Complete and Ready for Testing
