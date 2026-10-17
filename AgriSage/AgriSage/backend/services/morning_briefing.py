from typing import Dict, Any, List
from datetime import datetime


class MorningBriefingService:
    """Service assembling daily morning briefings for smallholder farmers."""

    def generate_briefing(
        self,
        farmer_name: str,
        crop: str,
        weather_data: Dict[str, Any],
        risk_data: Dict[str, Any],
        language: str = "ml"
    ) -> Dict[str, Any]:
        temp = weather_data.get("temp_c", 28.0)
        humidity = weather_data.get("humidity_pct", 75.0)
        wind = weather_data.get("wind_speed_kmh", 10.0)
        dfi = risk_data.get("dfi", 0.3)

        # Evaluate morning spray window (Wind < 15 km/h, Temp < 32°C, Rain < 2mm)
        spray_window_open = wind < 15.0 and temp < 32.0 and weather_data.get("rainfall_mm", 0.0) < 2.0

        if language == "ml":
            headline = f"നമസ്കാരം {farmer_name}, ഇന്നത്തെ കാർഷിക വിവരങ്ങൾ ({crop.capitalize()})"
            summary = (
                f"ഇന്നത്തെ താപനില {temp}°C, ഈർപ്പം {humidity}%. "
                f"{'ഇന്ന് രാവിലത്തെ മരുന്ന് തളിക്കൽ അനുയോജ്യമാണ് (കാറ്റ് കുറവാണ്).' if spray_window_open else 'ഇന്ന് കാറ്റുള്ളതിനാൽ മരുന്ന് തളിക്കുന്നത് ഒഴിവാക്കുക.'}"
            )
        else:
            headline = f"Good morning {farmer_name}, Daily briefing for {crop.capitalize()}"
            summary = (
                f"Today's temp: {temp}°C, Humidity: {humidity}%. "
                f"{'Morning spray window is OPEN (favorable wind conditions).' if spray_window_open else 'Spray window CLOSED due to wind/weather.'}"
            )

        return {
            "farmer_name": farmer_name,
            "crop": crop,
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "headline": headline,
            "summary": summary,
            "spray_window_open": spray_window_open,
            "temperature_c": temp,
            "humidity_pct": humidity,
            "wind_speed_kmh": wind,
            "disease_risk_dfi": dfi,
            "language": language,
            "audio_available": True
        }
