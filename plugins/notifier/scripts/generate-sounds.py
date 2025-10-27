#!/usr/bin/env python3
"""
Generate notification sound files for the Claude Code Notifier plugin.
Creates simple, pleasant WAV files with sine wave tones.
"""

import math
import struct
import wave
import os
import random

def generate_tone(filename, frequency, duration, volume=0.3):
    """
    Generate a simple sine wave tone and save as WAV file.

    Args:
        filename: Output WAV file path
        frequency: Frequency in Hz
        duration: Duration in seconds
        volume: Volume (0.0 to 1.0)
    """
    sample_rate = 44100
    num_samples = int(sample_rate * duration)

    # Generate sine wave samples
    samples = []
    for i in range(num_samples):
        # Calculate sample value
        sample = volume * math.sin(2 * math.pi * frequency * i / sample_rate)

        # Apply fade out in last 20% to avoid clicks
        if i > num_samples * 0.8:
            fade = 1.0 - ((i - num_samples * 0.8) / (num_samples * 0.2))
            sample *= fade

        # Apply fade in in first 5% to avoid clicks
        if i < num_samples * 0.05:
            fade = i / (num_samples * 0.05)
            sample *= fade

        # Convert to 16-bit integer
        sample_int = int(sample * 32767)
        samples.append(sample_int)

    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        # Set parameters: mono, 16-bit, 44.1kHz
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        # Write samples
        for sample in samples:
            wav_file.writeframes(struct.pack('h', sample))

def generate_chord(filename, frequencies, duration, volume=0.2):
    """
    Generate a chord by mixing multiple frequencies.

    Args:
        filename: Output WAV file path
        frequencies: List of frequencies in Hz
        duration: Duration in seconds
        volume: Volume per frequency (0.0 to 1.0)
    """
    sample_rate = 44100
    num_samples = int(sample_rate * duration)

    # Generate mixed samples
    samples = []
    for i in range(num_samples):
        # Mix multiple frequencies
        sample = 0
        for freq in frequencies:
            sample += volume * math.sin(2 * math.pi * freq * i / sample_rate)

        # Normalize by number of frequencies
        sample /= len(frequencies)

        # Apply fade out in last 20% to avoid clicks
        if i > num_samples * 0.8:
            fade = 1.0 - ((i - num_samples * 0.8) / (num_samples * 0.2))
            sample *= fade

        # Apply fade in in first 5% to avoid clicks
        if i < num_samples * 0.05:
            fade = i / (num_samples * 0.05)
            sample *= fade

        # Convert to 16-bit integer
        sample_int = int(sample * 32767)
        samples.append(sample_int)

    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        for sample in samples:
            wav_file.writeframes(struct.pack('h', sample))

def generate_keyboard_click(filename, num_clicks=1, volume=0.15):
    """
    Generate realistic keyboard click sound(s).

    Args:
        filename: Output WAV file path
        num_clicks: Number of clicks (1 for single, 2-3 for multiple)
        volume: Volume (0.0 to 1.0)
    """
    sample_rate = 44100
    click_duration = 0.025  # 25ms per click
    gap_duration = 0.035    # 35ms gap between clicks

    total_duration = (click_duration * num_clicks) + (gap_duration * (num_clicks - 1))
    num_samples = int(sample_rate * total_duration)

    samples = [0] * num_samples

    for click_num in range(num_clicks):
        # Calculate start position for this click
        start_time = click_num * (click_duration + gap_duration)
        start_sample = int(start_time * sample_rate)
        click_samples = int(click_duration * sample_rate)

        # Slight variation in frequency for realism
        freq_variation = 1.0 + (random.random() - 0.5) * 0.1

        # Keyboard clicks have multiple frequency components
        # High frequency for the "click" sound
        frequencies = [
            3000 * freq_variation,
            4500 * freq_variation,
            6000 * freq_variation
        ]

        for i in range(click_samples):
            if start_sample + i < num_samples:
                # Mix multiple frequencies for realistic click
                sample = 0
                for freq in frequencies:
                    sample += volume * math.sin(2 * math.pi * freq * i / sample_rate)

                # Add slight noise component for realism
                noise = (random.random() - 0.5) * volume * 0.15
                sample += noise

                # Normalize by number of components
                sample /= (len(frequencies) + 1)

                # Very sharp attack (first 10%)
                if i < click_samples * 0.1:
                    attack = i / (click_samples * 0.1)
                    sample *= attack * attack  # Exponential attack

                # Quick decay (after 30%)
                if i > click_samples * 0.3:
                    decay_progress = (i - click_samples * 0.3) / (click_samples * 0.7)
                    decay = 1.0 - (decay_progress * decay_progress)  # Exponential decay
                    sample *= decay

                samples[start_sample + i] += sample

    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        for sample in samples:
            sample_int = int(max(-32767, min(32767, sample * 32767)))
            wav_file.writeframes(struct.pack('h', sample_int))

def main():
    # Get sounds directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_root = os.path.dirname(script_dir)
    sounds_dir = os.path.join(plugin_root, 'sounds')

    print(f"Generating notification sounds in {sounds_dir}...")

    # Create sounds directory if it doesn't exist
    os.makedirs(sounds_dir, exist_ok=True)

    # Generate different notification sounds

    # 1. Bell - Classic bell tone (mix of frequencies)
    print("  Generating bell.wav...")
    generate_chord(
        os.path.join(sounds_dir, 'bell.wav'),
        [800, 1000, 1200],  # Bell-like frequencies
        0.4,
        volume=0.25
    )

    # 2. Chime - Pleasant high chime
    print("  Generating chime.wav...")
    generate_chord(
        os.path.join(sounds_dir, 'chime.wav'),
        [1046.50, 1318.51],  # C6 and E6 (major third)
        0.5,
        volume=0.3
    )

    # 3. Subtle - Very short, quiet pop
    print("  Generating subtle.wav...")
    generate_tone(
        os.path.join(sounds_dir, 'subtle.wav'),
        880,  # A5
        0.15,
        volume=0.2
    )

    # 4. Complete - Ascending notes to indicate completion
    print("  Generating complete.wav...")
    # This one needs a custom approach for ascending tones
    sample_rate = 44100
    duration = 0.6
    num_samples = int(sample_rate * duration)

    # Three ascending tones
    tones = [
        (523.25, 0.0, 0.15),    # C5, start at 0s, duration 0.15s
        (659.25, 0.15, 0.15),   # E5, start at 0.15s, duration 0.15s
        (783.99, 0.3, 0.3),     # G5, start at 0.3s, duration 0.3s
    ]

    samples = [0] * num_samples

    for freq, start_time, tone_duration in tones:
        start_sample = int(start_time * sample_rate)
        tone_samples = int(tone_duration * sample_rate)

        for i in range(tone_samples):
            if start_sample + i < num_samples:
                sample = 0.25 * math.sin(2 * math.pi * freq * i / sample_rate)

                # Fade in first 5%
                if i < tone_samples * 0.05:
                    sample *= i / (tone_samples * 0.05)

                # Fade out last 20%
                if i > tone_samples * 0.8:
                    fade = 1.0 - ((i - tone_samples * 0.8) / (tone_samples * 0.2))
                    sample *= fade

                samples[start_sample + i] += sample

    # Write complete.wav
    with wave.open(os.path.join(sounds_dir, 'complete.wav'), 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        for sample in samples:
            sample_int = int(sample * 32767)
            wav_file.writeframes(struct.pack('h', sample_int))

    # 5. Click - Single keyboard key click
    print("  Generating click.wav...")
    random.seed(42)  # For consistent results
    generate_keyboard_click(
        os.path.join(sounds_dir, 'click.wav'),
        num_clicks=1,
        volume=0.15
    )

    # 6. Clicks - Multiple keyboard key clicks (typing sound)
    print("  Generating clicks.wav...")
    random.seed(43)  # Different seed for variation
    generate_keyboard_click(
        os.path.join(sounds_dir, 'clicks.wav'),
        num_clicks=3,
        volume=0.15
    )

    print("✓ All notification sounds generated successfully!")
    print("\nGenerated sounds:")
    print("  - bell.wav     : Classic bell tone")
    print("  - chime.wav    : Pleasant high chime (default)")
    print("  - subtle.wav   : Very short, quiet pop")
    print("  - complete.wav : Ascending completion melody")
    print("  - click.wav    : Single keyboard key click")
    print("  - clicks.wav   : Multiple keyboard key clicks (typing)")

if __name__ == '__main__':
    main()
