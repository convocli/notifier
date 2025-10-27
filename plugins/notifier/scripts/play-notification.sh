#!/bin/bash
#
# Claude Code Notifier - Cross-platform notification script
# Supports audio on desktop and vibration on Termux/Android
#

# Debug logging
LOG_FILE="${HOME}/.config/claude-notifier/debug.log"
mkdir -p "$(dirname "$LOG_FILE")"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Hook triggered" >> "$LOG_FILE"

# Load config file if it exists
CONFIG_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/claude-notifier/config"
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
fi

# Configuration via environment variables (config file takes precedence)
SOUND="${NOTIFIER_SOUND:-chime}"              # Sound to play: bell, chime, subtle, complete
VIBRATE_DURATION="${NOTIFIER_VIBRATE_DURATION:-200}"  # Vibration duration in milliseconds
MODE="${NOTIFIER_MODE:-auto}"                  # Mode: auto, vibrate-only, sound-only, both

# Get the plugin root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOUNDS_DIR="$PLUGIN_ROOT/sounds"

# Function to detect if we're in Termux
is_termux() {
    [[ -n "$TERMUX_VERSION" ]] || [[ -d "/data/data/com.termux" ]]
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to play vibration (Termux)
play_vibration() {
    if command_exists termux-vibrate; then
        termux-vibrate -d "$VIBRATE_DURATION" 2>/dev/null &
        return 0
    fi
    return 1
}

# Function to play sound (Desktop)
play_sound() {
    local sound_file="$SOUNDS_DIR/${SOUND}.wav"

    # Check if sound file exists
    if [[ ! -f "$sound_file" ]]; then
        # Try fallback to chime if specified sound doesn't exist
        sound_file="$SOUNDS_DIR/chime.wav"
        if [[ ! -f "$sound_file" ]]; then
            return 1
        fi
    fi

    # Try different audio players in order of preference
    if command_exists paplay; then
        paplay "$sound_file" 2>/dev/null &
        return 0
    elif command_exists aplay; then
        aplay -q "$sound_file" 2>/dev/null &
        return 0
    elif command_exists afplay; then
        afplay "$sound_file" 2>/dev/null &
        return 0
    elif command_exists ffplay; then
        ffplay -nodisp -autoexit -v 0 "$sound_file" 2>/dev/null &
        return 0
    fi

    return 1
}

# Function to play system beep as last resort
play_beep() {
    if command_exists tput; then
        tput bel 2>/dev/null
        return 0
    elif command_exists printf; then
        printf '\a'
        return 0
    fi
    return 1
}

# Main notification logic
notify() {
    local vibrate_played=false
    local sound_played=false

    case "$MODE" in
        vibrate-only)
            play_vibration && vibrate_played=true
            ;;
        sound-only)
            play_sound && sound_played=true
            ;;
        both)
            play_vibration && vibrate_played=true
            play_sound && sound_played=true
            ;;
        auto|*)
            # Auto-detect best notification method
            if is_termux; then
                # Prefer vibration on Termux
                if play_vibration; then
                    vibrate_played=true
                else
                    # Fallback to sound if vibration not available
                    play_sound && sound_played=true
                fi
            else
                # Prefer sound on desktop
                if play_sound; then
                    sound_played=true
                else
                    # Try vibration (unlikely on desktop, but who knows)
                    play_vibration && vibrate_played=true
                fi
            fi
            ;;
    esac

    # Fallback to system beep if nothing worked
    if ! $vibrate_played && ! $sound_played; then
        play_beep
    fi
}

# Run notification in background to not block Claude
notify &

# Exit successfully
exit 0
