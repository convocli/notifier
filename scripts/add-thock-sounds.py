#!/usr/bin/env python3
"""
Generate low-frequency "thock" keyboard sounds for the notifier plugin.
Emphasizes the deep, satisfying thock sound over high-frequency clicks.
"""

import math
import struct
import wave
import os
import random

def generate_thock_click(filename, volume=0.15):
    """
    Generate a thock-focused mechanical keyboard click sound.
    Emphasizes low-frequency "thock" over high-frequency "click".

    Args:
        filename: Output WAV file path
        volume: Volume (0.0 to 1.0)
    """
    sample_rate = 44100
    duration = 0.08  # Slightly longer for thock to resonate
    num_samples = int(sample_rate * duration)

    samples = [0.0] * num_samples

    # Component 1: Reduced high-frequency click (just a hint)
    click_duration = 0.006  # Shorter
    click_samples = int(click_duration * sample_rate)
    click_freq = 4000  # Slightly lower

    for i in range(min(click_samples, num_samples)):
        t = i / sample_rate
        envelope = math.exp(-t * 200)  # Faster decay

        sample = 0
        sample += math.sin(2 * math.pi * click_freq * t) * envelope
        sample += 0.3 * math.sin(2 * math.pi * click_freq * 2 * t) * envelope

        samples[i] += sample * 0.3  # Reduced volume

    # Component 2: Moderate mid-frequency clack
    clack_start = 0.003
    clack_duration = 0.012
    clack_start_sample = int(clack_start * sample_rate)
    clack_samples = int(clack_duration * sample_rate)
    clack_freq = 1800

    for i in range(clack_samples):
        sample_idx = clack_start_sample + i
        if sample_idx < num_samples:
            t = i / sample_rate
            envelope = math.exp(-t * 90)

            sample = math.sin(2 * math.pi * clack_freq * t) * envelope
            sample += 0.3 * math.sin(2 * math.pi * clack_freq * 1.5 * t) * envelope

            samples[sample_idx] += sample * 0.4  # Moderate

    # Component 3: EMPHASIZED low-frequency thock (the star of the show!)
    thock_start = 0.004
    thock_duration = 0.05  # Longer thock
    thock_start_sample = int(thock_start * sample_rate)
    thock_samples = int(thock_duration * sample_rate)
    thock_freq = 350  # Deep thock

    for i in range(thock_samples):
        sample_idx = thock_start_sample + i
        if sample_idx < num_samples:
            t = i / sample_rate
            envelope = math.exp(-t * 35)  # Slower decay for longer resonance

            # Rich low-frequency harmonics
            sample = math.sin(2 * math.pi * thock_freq * t) * envelope
            sample += 0.5 * math.sin(2 * math.pi * thock_freq * 2 * t) * envelope
            sample += 0.3 * math.sin(2 * math.pi * thock_freq * 3 * t) * envelope

            samples[sample_idx] += sample * 0.9  # EMPHASIZED!

    # Component 4: Minimal noise
    noise_duration = 0.008
    noise_samples = int(noise_duration * sample_rate)

    random.seed(45)
    for i in range(min(noise_samples, num_samples)):
        t = i / sample_rate
        envelope = math.exp(-t * 170)

        noise = (random.random() - 0.5) * 2.0
        samples[i] += noise * envelope * 0.08  # Very subtle

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

def generate_multiple_thock_clicks(filename, num_clicks=3, volume=0.15):
    """
    Generate multiple thock-focused keyboard clicks (typing sound).

    Args:
        filename: Output WAV file path
        num_clicks: Number of clicks to generate
        volume: Volume (0.0 to 1.0)
    """
    sample_rate = 44100
    click_base_duration = 0.08
    gap_duration = 0.045

    random.seed(46)
    gap_variations = [gap_duration + (random.random() - 0.5) * 0.02 for _ in range(num_clicks - 1)]

    total_duration = (click_base_duration * num_clicks) + sum(gap_variations)
    num_samples = int(sample_rate * total_duration)

    samples = [0.0] * num_samples

    current_position = 0
    for click_num in range(num_clicks):
        start_sample = int(current_position * sample_rate)

        freq_variation = 1.0 + (random.random() - 0.5) * 0.08

        # Reduced high-frequency click
        click_duration = 0.006
        click_sample_count = int(click_duration * sample_rate)
        click_freq = 4000 * freq_variation

        for i in range(click_sample_count):
            if start_sample + i < num_samples:
                t = i / sample_rate
                envelope = math.exp(-t * 200)

                sample = 0
                sample += math.sin(2 * math.pi * click_freq * t) * envelope
                sample += 0.3 * math.sin(2 * math.pi * click_freq * 2 * t) * envelope

                samples[start_sample + i] += sample * 0.3

        # Moderate mid-frequency clack
        clack_start = 0.003
        clack_duration = 0.012
        clack_start_sample = int(clack_start * sample_rate)
        clack_sample_count = int(clack_duration * sample_rate)
        clack_freq = 1800 * freq_variation

        for i in range(clack_sample_count):
            sample_idx = start_sample + clack_start_sample + i
            if sample_idx < num_samples:
                t = i / sample_rate
                envelope = math.exp(-t * 90)

                sample = math.sin(2 * math.pi * clack_freq * t) * envelope
                sample += 0.3 * math.sin(2 * math.pi * clack_freq * 1.5 * t) * envelope

                samples[sample_idx] += sample * 0.4

        # EMPHASIZED low-frequency thock
        thock_start = 0.004
        thock_duration = 0.05
        thock_start_sample = int(thock_start * sample_rate)
        thock_sample_count = int(thock_duration * sample_rate)
        thock_freq = 350 * freq_variation

        for i in range(thock_sample_count):
            sample_idx = start_sample + thock_start_sample + i
            if sample_idx < num_samples:
                t = i / sample_rate
                envelope = math.exp(-t * 35)

                sample = math.sin(2 * math.pi * thock_freq * t) * envelope
                sample += 0.5 * math.sin(2 * math.pi * thock_freq * 2 * t) * envelope
                sample += 0.3 * math.sin(2 * math.pi * thock_freq * 3 * t) * envelope

                samples[sample_idx] += sample * 0.9

        # Minimal noise
        noise_duration = 0.008
        noise_sample_count = int(noise_duration * sample_rate)

        for i in range(noise_sample_count):
            if start_sample + i < num_samples:
                t = i / sample_rate
                envelope = math.exp(-t * 170)
                noise = (random.random() - 0.5) * 2.0
                samples[start_sample + i] += noise * envelope * 0.08

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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_root = os.path.dirname(script_dir)
    sounds_dir = os.path.join(plugin_root, 'sounds')

    print(f"Generating thock-focused keyboard sounds...")

    os.makedirs(sounds_dir, exist_ok=True)

    # Generate single thock sound
    output_file = os.path.join(sounds_dir, 'thock.wav')
    generate_thock_click(output_file, volume=0.15)
    print(f"✓ Generated {output_file}")

    # Generate multiple thock sounds
    output_file_multi = os.path.join(sounds_dir, 'thocks.wav')
    generate_multiple_thock_clicks(output_file_multi, num_clicks=3, volume=0.15)
    print(f"✓ Generated {output_file_multi}")

    print("\nThese sounds emphasize the deep, satisfying THOCK:")
    print("  - Reduced high-frequency click")
    print("  - Moderate mid-frequency clack")
    print("  - EMPHASIZED low-frequency thock (the star!)")
    print("  - Minimal noise")
    print("\nUse them with:")
    print("  NOTIFIER_SOUND=thock   (single thock)")
    print("  NOTIFIER_SOUND=thocks  (multiple thocks)")

if __name__ == '__main__':
    main()
