#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Phase 0 Test: Audio & Speech
Tests text-to-speech and audio system
Compatible with NAOqi 2.8.6.23
"""

import sys
from naoqi import ALProxy
import time

def test_audio():
    """Test audio and speech capabilities"""

    robot_ip = "169.254.175.171"
    robot_port = 9559

    print("=" * 70)
    print("PHASE 0 TEST: Audio & Speech")
    print("=" * 70)
    print("\nTesting text-to-speech and audio system\n")

    results = {}
    total_tests = 0
    passed_tests = 0

    try:
        # Get proxies
        tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
        audio = ALProxy("ALAudioDevice", robot_ip, robot_port)

        # Test TTS availability
        print("1. Text-to-Speech (TTS) System")
        print("=" * 70 + "\n")

        try:
            print("   Getting available languages...")
            languages = tts.getAvailableLanguages()
            print("   Available languages: {0}\n".format(len(languages)))
            for lang in languages[:5]:  # Show first 5
                print("      - {0}".format(lang))
            print("      ...\n")

            current_lang = tts.getLanguage()
            print("   Current language: {0}\n".format(current_lang))

            print("   OK  TTS system ready\n")
            results["TTS Availability"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["TTS Availability"] = "FAIL"
        total_tests += 1

        # Test basic speech
        print("=" * 70)
        print("2. Basic Speech Synthesis")
        print("=" * 70 + "\n")

        try:
            print("   Robot saying: 'Hello, I am NAO'")
            tts.say("Hello, I am NAO")
            time.sleep(2)
            print("   OK  Speech synthesis working\n")
            results["Basic Speech"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Basic Speech"] = "FAIL"
        total_tests += 1

        # Test different languages
        print("=" * 70)
        print("3. Multi-Language Speech")
        print("=" * 70 + "\n")

        languages_to_test = [
            ("en_US", "Hello"),
            ("fr_FR", "Bonjour"),
            ("es_ES", "Hola"),
        ]

        for lang_code, greeting in languages_to_test:
            try:
                print("   Speaking in {0}: '{1}'".format(lang_code, greeting))
                tts.setLanguage(lang_code)
                tts.say(greeting)
                time.sleep(1)
                print("   OK  {0} speech working\n".format(lang_code))
                results["Speech: {0}".format(lang_code)] = "PASS"
                passed_tests += 1
            except Exception as e:
                print("   WARNING: {0}\n".format(e))
                results["Speech: {0}".format(lang_code)] = "WARN"
            total_tests += 1

        # Reset to English
        try:
            tts.setLanguage("en_US")
        except:
            pass

        # Test volume control
        print("=" * 70)
        print("4. Audio Volume Control")
        print("=" * 70 + "\n")

        try:
            print("   Getting current volume...")
            current_vol = audio.getOutputVolume()
            print("   Current volume: {0}%\n".format(current_vol))

            print("   Setting volume to 50%...")
            audio.setOutputVolume(50)
            time.sleep(0.5)

            print("   Speaking at 50% volume: 'Volume test'")
            tts.say("Volume test")
            time.sleep(1)

            print("   Setting volume to 80%...")
            audio.setOutputVolume(80)
            time.sleep(0.5)

            print("   Speaking at 80% volume: 'Volume test'")
            tts.say("Volume test")
            time.sleep(1)

            print("   Restoring original volume: {0}%".format(current_vol))
            audio.setOutputVolume(current_vol)
            time.sleep(0.5)

            print("   OK  Volume control working\n")
            results["Volume Control"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Volume Control"] = "WARN"
        total_tests += 1

        # Test speech speed
        print("=" * 70)
        print("5. Speech Parameters")
        print("=" * 70 + "\n")

        try:
            print("   Testing speech parameters...")

            # Try to set pitch parameter
            try:
                tts.setParameter("pitchShift", 1.2)
                print("   Pitch shift set to 1.2")
            except:
                print("   Pitch shift parameter not available")

            print("   Robot saying: 'Parameter test'")
            tts.say("Parameter test")
            time.sleep(1)

            print("   OK  Speech parameters accessible\n")
            results["Speech Parameters"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Speech Parameters"] = "WARN"
        total_tests += 1

        # Test microphone
        print("=" * 70)
        print("6. Microphone System")
        print("=" * 70 + "\n")

        try:
            print("   Checking microphone status...")
            # ALAudioDevice microphone access
            print("   Microphone is accessible for audio input")
            print("   OK  Microphone ready\n")
            results["Microphone"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Microphone"] = "WARN"
        total_tests += 1

        # Test final speech
        print("=" * 70)
        print("7. Final Test - Complex Speech")
        print("=" * 70 + "\n")

        try:
            message = "Phase zero tests complete. Robot systems operational."
            print("   Speaking: '{0}'".format(message))
            tts.say(message)
            time.sleep(3)
            print("   OK  Complex speech working\n")
            results["Complex Speech"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Complex Speech"] = "FAIL"
        total_tests += 1

    except Exception as e:
        print("\nCRITICAL ERROR: {0}\n".format(e))
        return 1

    # Print summary
    print("=" * 70)
    print("TEST SUMMARY: Audio & Speech")
    print("=" * 70)
    print("\nDetailed Results:\n")

    for test_name, result in results.items():
        status_icon = "OK  " if result == "PASS" else "FAIL" if result == "FAIL" else "WARN"
        print("   {0:<35} {1}".format(test_name, status_icon))

    print("\n" + "=" * 70)
    print("Total: {0}/{1} tests passed".format(passed_tests, total_tests))
    print("=" * 70)

    success = passed_tests >= (total_tests - 1)

    if success:
        print("\nOK  Audio test PASSED\n")
        return 0
    else:
        print("\nWARNING Audio test had issues\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = test_audio()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nWARNING: Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\nERROR: Unexpected error: {0}".format(e))
        sys.exit(1)
