#!/usr/bin/env python3
"""
Add a realistic mechanical keyboard click sound to the notifier plugin.
Uses advanced synthesis to create an authentic mechanical switch sound.
"""

import math
import struct
import wave
import os
import random

def generate_mechanical_keyboard_click(filename, volume=0.2):
    """
    Generate a highly realistic mechanical keyboard click sound.

    Mechanical keyboards have several sound components:
    1. High-frequency "click" from switch activation
    2. Mid-frequency "clack" from keycap impact
    3. Low-frequency "thock" from housing resonance
    4. Some subtle noise for texture

    Args:
        filename: Output WAV file path
        volume: Volume (0.0 to 1.0)
    """
    sample_rate = 44100
    duration = 0.06  # 60ms total
    num_samples = int(sample_rate * duration)

    samples = [0.0] * num_samples

    # Component 1: Sharp high-frequency click (switch activation)
    # This is the characteristic "click" of a mechanical switch
    click_duration = 0.008  # 8ms
    click_samples = int(click_duration * sample_rate)
    click_freq = 4500  # High pitched click

    for i in range(min(click_samples, num_samples)):
        # Sharp sine wave with very fast decay
        t = i / sample_rate
        envelope = math.exp(-t * 180)  # Very fast exponential decay

        # Add some harmonics for richness
        sample = 0
        sample += math.sin(2 * math.pi * click_freq * t) * envelope
        sample += 0.5 * math.sin(2 * math.pi * click_freq * 2 * t) * envelope  # 2nd harmonic
        sample += 0.3 * math.sin(2 * math.pi * click_freq * 3 * t) * envelope  # 3rd harmonic

        samples[i] += sample * 0.6

    # Component 2: Mid-frequency clack (keycap impact)
    # Starts slightly after the click
    clack_start = 0.003  # 3ms delay
    clack_duration = 0.015  # 15ms
    clack_start_sample = int(clack_start * sample_rate)
    clack_samples = int(clack_duration * sample_rate)
    clack_freq = 2000  # Mid-range clack

    for i in range(clack_samples):
        sample_idx = clack_start_sample + i
        if sample_idx < num_samples:
            t = i / sample_rate
            envelope = math.exp(-t * 100)  # Fast decay

            sample = math.sin(2 * math.pi * clack_freq * t) * envelope
            sample += 0.4 * math.sin(2 * math.pi * clack_freq * 1.5 * t) * envelope

            samples[sample_idx] += sample * 0.5

    # Component 3: Low-frequency thock (housing resonance)
    # This gives the "body" to the sound
    thock_start = 0.005  # 5ms delay
    thock_duration = 0.03  # 30ms
    thock_start_sample = int(thock_start * sample_rate)
    thock_samples = int(thock_duration * sample_rate)
    thock_freq = 400  # Low thock

    for i in range(thock_samples):
        sample_idx = thock_start_sample + i
        if sample_idx < num_samples:
            t = i / sample_rate
            envelope = math.exp(-t * 50)  # Slower decay for low frequencies

            sample = math.sin(2 * math.pi * thock_freq * t) * envelope
            sample += 0.3 * math.sin(2 * math.pi * thock_freq * 2 * t) * envelope

            samples[sample_idx] += sample * 0.4

    # Component 4: Broadband noise burst (spring/mechanism noise)
    noise_duration = 0.012  # 12ms
    noise_samples = int(noise_duration * sample_rate)

    random.seed(42)  # Consistent noise pattern
    for i in range(min(noise_samples, num_samples)):
        t = i / sample_rate
        envelope = math.exp(-t * 150)  # Very fast decay

        # Band-limited noise (high frequency)
        noise = (random.random() - 0.5) * 2.0
        samples[i] += noise * envelope * 0.15

    # Final pass: normalize first, then apply volume
    max_sample = max(abs(s) for s in samples)
    if max_sample > 0:
        # Normalize to full range first
        normalization = 1.0 / max_sample
        samples = [s * normalization for s in samples]

    # Now apply the actual volume control
    samples = [s * volume for s in samples]

    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        for sample in samples:
            sample_int = int(max(-32767, min(32767, sample * 32767)))
            wav_file.writeframes(struct.pack('h', sample_int))

def generate_multiple_mechanical_clicks(filename, num_clicks=3, volume=0.15):
    """
    Generate multiple mechanical keyboard clicks (typing sound).

    Args:
        filename: Output WAV file path
        num_clicks: Number of clicks to generate
        volume: Volume (0.0 to 1.0)
    """
    sample_rate = 44100
    click_base_duration = 0.06  # 60ms per click
    gap_duration = 0.04  # 40ms gap between clicks

    # Add slight variation to gaps for natural typing rhythm
    random.seed(44)  # Different seed than click/clicks
    gap_variations = [gap_duration + (random.random() - 0.5) * 0.02 for _ in range(num_clicks - 1)]

    # Calculate total duration
    total_duration = (click_base_duration * num_clicks) + sum(gap_variations)
    num_samples = int(sample_rate * total_duration)

    samples = [0.0] * num_samples

    current_position = 0
    for click_num in range(num_clicks):
        start_sample = int(current_position * sample_rate)
        click_samples_count = int(click_base_duration * sample_rate)

        # Slight frequency variation for each click for realism
        freq_variation = 1.0 + (random.random() - 0.5) * 0.08

        # Generate one mechanical click at this position
        # Component 1: High-frequency click
        click_duration = 0.008
        click_sample_count = int(click_duration * sample_rate)
        click_freq = 4500 * freq_variation

        for i in range(click_sample_count):
            if start_sample + i < num_samples:
                t = i / sample_rate
                envelope = math.exp(-t * 180)

                sample = 0
                sample += math.sin(2 * math.pi * click_freq * t) * envelope
                sample += 0.5 * math.sin(2 * math.pi * click_freq * 2 * t) * envelope
                sample += 0.3 * math.sin(2 * math.pi * click_freq * 3 * t) * envelope

                samples[start_sample + i] += sample * 0.6

        # Component 2: Mid-frequency clack
        clack_start = 0.003
        clack_duration = 0.015
        clack_start_sample = int(clack_start * sample_rate)
        clack_sample_count = int(clack_duration * sample_rate)
        clack_freq = 2000 * freq_variation

        for i in range(clack_sample_count):
            sample_idx = start_sample + clack_start_sample + i
            if sample_idx < num_samples:
                t = i / sample_rate
                envelope = math.exp(-t * 100)

                sample = math.sin(2 * math.pi * clack_freq * t) * envelope
                sample += 0.4 * math.sin(2 * math.pi * clack_freq * 1.5 * t) * envelope

                samples[sample_idx] += sample * 0.5

        # Component 3: Low-frequency thock
        thock_start = 0.005
        thock_duration = 0.03
        thock_start_sample = int(thock_start * sample_rate)
        thock_sample_count = int(thock_duration * sample_rate)
        thock_freq = 400 * freq_variation

        for i in range(thock_sample_count):
            sample_idx = start_sample + thock_start_sample + i
            if sample_idx < num_samples:
                t = i / sample_rate
                envelope = math.exp(-t * 50)

                sample = math.sin(2 * math.pi * thock_freq * t) * envelope
                sample += 0.3 * math.sin(2 * math.pi * thock_freq * 2 * t) * envelope

                samples[sample_idx] += sample * 0.4

        # Component 4: Noise
        noise_duration = 0.012
        noise_sample_count = int(noise_duration * sample_rate)

        for i in range(noise_sample_count):
            if start_sample + i < num_samples:
                t = i / sample_rate
                envelope = math.exp(-t * 150)
                noise = (random.random() - 0.5) * 2.0
                samples[start_sample + i] += noise * envelope * 0.15

        # Move to next click position
        current_position += click_base_duration
        if click_num < len(gap_variations):
            current_position += gap_variations[click_num]

    # Normalize and apply volume
    max_sample = max(abs(s) for s in samples)
    if max_sample > 0:
        normalization = 1.0 / max_sample
        samples = [s * normalization for s in samples]

    samples = [s * volume for s in samples]

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

    print(f"Generating realistic mechanical keyboard sounds...")

    # Create sounds directory if it doesn't exist
    os.makedirs(sounds_dir, exist_ok=True)

    # Generate single mechanical keyboard sound
    output_file = os.path.join(sounds_dir, 'mech.wav')
    generate_mechanical_keyboard_click(output_file, volume=0.15)
    print(f"✓ Generated {output_file}")

    # Generate multiple mechanical keyboard sounds (typing)
    output_file_multi = os.path.join(sounds_dir, 'mechs.wav')
    generate_multiple_mechanical_clicks(output_file_multi, num_clicks=3, volume=0.15)
    print(f"✓ Generated {output_file_multi}")

    print("\nThese sounds simulate mechanical keyboard switches with:")
    print("  - High-frequency click (switch activation)")
    print("  - Mid-frequency clack (keycap impact)")
    print("  - Low-frequency thock (housing resonance)")
    print("  - Subtle noise texture (spring/mechanism)")
    print("\nUse them with:")
    print("  NOTIFIER_SOUND=mech   (single click)")
    print("  NOTIFIER_SOUND=mechs  (multiple clicks)")

if __name__ == '__main__':
    main()
