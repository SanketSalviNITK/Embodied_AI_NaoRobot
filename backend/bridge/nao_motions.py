import time

def parse_and_execute_mood(mood_tag, animation_proxy, leds_proxy):
    """
    Executes physical gestures and LED animations based on the mood tag.
    """
    if not animation_proxy or not leds_proxy:
        return

    mood_tag = mood_tag.upper().strip()

    # Define color tuples (R, G, B)
    colors = {
        "HAPPY": (0.0, 1.0, 0.0),       # Green
        "SAD": (0.0, 0.0, 1.0),         # Blue
        "SURPRISED": (1.0, 1.0, 0.0),   # Yellow
        "CURIOUS": (1.0, 1.0, 1.0),     # White
        "NEUTRAL": (1.0, 1.0, 1.0)      # Default
    }

    # Define standard animation paths for NAO
    animations = {
        "HAPPY": "animations/Stand/Gestures/Joy_1",
        "SAD": "animations/Stand/Gestures/Despair_1",
        "SURPRISED": "animations/Stand/Gestures/Surprised_1",
        "CURIOUS": "animations/Stand/Gestures/Thinking_1",
        "NEUTRAL": "animations/Stand/Gestures/Explain_1"
    }

    # Extract just the mood name from the tag (e.g. "[MOOD: HAPPY]" -> "HAPPY")
    clean_mood = "NEUTRAL"
    for mood in colors.keys():
        if mood in mood_tag:
            clean_mood = mood
            break

    # 1. Set LED Colors
    r, g, b = colors[clean_mood]
    leds_proxy.fadeRGB("FaceLeds", r, g, b, 0.5)

    # 2. Execute Gesture asynchronously so it doesn't block
    anim_path = animations[clean_mood]
    try:
        animation_proxy.post.run(anim_path)
    except Exception as e:
        print("Could not run animation: {}".format(e))
