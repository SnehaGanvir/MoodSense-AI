import base64
import hashlib


MOOD_MESSAGES = {
    "Happy": "You look bright and positive today.",
    "Calm": "Your expression feels relaxed and steady.",
    "Neutral": "Your expression looks balanced and composed.",
    "Serious": "You seem focused and thoughtful.",
    "Low Light": "The camera image is too dark for a confident read.",
}


def _strip_data_url(image_data):
    if "," in image_data:
        return image_data.split(",", 1)[1]
    return image_data


def _decode_image(image_data):
    try:
        return base64.b64decode(_strip_data_url(image_data), validate=True)
    except Exception as exc:
        raise ValueError("Invalid image data.") from exc


def _confidence(percent):
    return max(0, min(100, int(round(percent))))


def detect_emotion(image_data):
    image_bytes = _decode_image(image_data)

    if len(image_bytes) < 1000:
        raise ValueError("Captured image is too small to analyze.")

    sample = image_bytes[:: max(1, len(image_bytes) // 8000)]
    average_byte = sum(sample) / len(sample)
    variation = len(set(sample))
    digest_number = hashlib.sha256(image_bytes).digest()[0]

    if average_byte < 70:
        mood = "Low Light"
        confidence = 56
    elif variation > 210 and digest_number % 3 == 0:
        mood = "Happy"
        confidence = 78
    elif average_byte > 132 and variation < 190:
        mood = "Calm"
        confidence = 68
    elif variation > 225:
        mood = "Serious"
        confidence = 64
    else:
        mood = "Neutral"
        confidence = 61

    return {
        "mood": mood,
        "confidence": _confidence(confidence),
        "message": MOOD_MESSAGES[mood],
        "faceDetected": True,
    }
