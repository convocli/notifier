# Claude Code Notifier Plugin

> 🔔 Get audio and haptic feedback when Claude Code is ready for your next prompt

A cross-platform notification plugin for Claude Code that provides audio feedback on desktop and haptic feedback on Termux/Android when Claude is awaiting user input or permission.

**Quick Install:** See [INSTALL.md](INSTALL.md) for step-by-step instructions.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Desktop Installation](#option-1-install-from-github-recommended)
  - [Termux/Android Installation](#termuxandroid-installation)
- [Configuration](#configuration)
- [Available Sounds](#sound-options)
- [Usage](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Cross-platform support**: Works on Linux, macOS, and Termux/Android
- **Smart environment detection**: Automatically chooses the best notification method
- **Multiple notification sounds**: 10 built-in pleasant notification sounds
- **Vibration support**: Haptic feedback on Termux/Android devices
- **Highly configurable**: Customize via environment variables
- **Non-blocking**: Notifications play asynchronously without interrupting workflow

## Installation

### Prerequisites

**Desktop (Linux/macOS)**:
- One of the following audio players (usually pre-installed):
  - `paplay` (PulseAudio - most Linux systems)
  - `aplay` (ALSA - Linux)
  - `afplay` (macOS)
  - `ffplay` (FFmpeg)

**Termux/Android** (Termux must already be installed):
- Install termux-api package for vibration support:
  ```bash
  pkg install termux-api
  ```
- Install the [Termux:API companion app](https://f-droid.org/packages/com.termux.api/) from F-Droid

### Installing the Plugin

#### Option 1: Install from GitHub (Recommended)

1. **Clone the repository**:
   ```bash
   cd ~/code-projects  # Or your preferred directory
   git clone https://github.com/convocli/notifier.git
   cd notifier
   ```

2. **Create a plugin marketplace** (if you don't have one already):
   ```bash
   mkdir -p ~/.claude/plugins/marketplaces/local/.claude-plugin
   ```

3. **Add marketplace configuration**:
   First, get your plugin path:
   ```bash
   cd ~/code-projects/notifier
   pwd
   ```

   Then create `~/.claude/plugins/marketplaces/local/.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "local",
     "owner": {
       "name": "Local",
       "url": ""
     },
     "description": "Local marketplace for development and testing",
     "plugins": [
       {
         "name": "notifier",
         "source": "/home/YOUR_USERNAME/code-projects/notifier",
         "version": "1.0.0",
         "description": "Cross-platform notification plugin"
       }
     ]
   }
   ```
   **Important**: Replace `/home/YOUR_USERNAME/code-projects/notifier` with the actual path from the `pwd` command.

4. **Install the plugin in Claude Code**:
   ```
   /plugin install local:notifier
   ```

5. **Verify installation**:
   ```
   /plugin list
   ```
   You should see `notifier` in the list of installed plugins.

6. **Test the plugin**:
   ```
   /notifier:preview
   ```
   This will play all 10 notification sounds so you can choose your favorite!

#### Option 2: Direct GitHub Installation (Future)

Once this plugin is published to a public marketplace, you'll be able to install it directly:
```
/plugin install convocli:notifier
```
(This option will be available after the plugin is published)

### Quick Start

After installation, the plugin works automatically! Claude Code will play the default notification sound (`chime`) whenever it's awaiting your input or permission.

To customize which sound plays:
```bash
export NOTIFIER_SOUND=thock
```

To preview all sounds and choose your favorite:
```
/notifier:preview
```

To configure the plugin interactively:
```
/notifier:configure
```

### Termux/Android Installation

**Note:** These instructions assume you already have Termux installed on Android.

If you're running Claude Code in Termux:

1. **Clone the repository** (same as above):
   ```bash
   cd ~/code-projects  # Or your preferred directory
   git clone https://github.com/convocli/notifier.git
   cd notifier
   ```

2. **Install termux-api for vibration support** (if not already installed):
   ```bash
   pkg install termux-api
   ```
   Also install the [Termux:API companion app](https://f-droid.org/packages/com.termux.api/) from F-Droid.

3. **Grant permissions**: Open Android Settings → Apps → Termux:API → Permissions, and enable all requested permissions (especially "Vibrate").

4. **Follow steps 2-6** from "Option 1" above to configure the plugin marketplace and install.

5. **The plugin will automatically use vibration** on Termux instead of audio (unless you have an audio player installed).

6. **Test vibration**:
   ```bash
   termux-vibrate -d 200
   ```
   If this works, the notifier plugin will work too!

## Configuration

The plugin is configured via environment variables. You can set these in your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) or in Claude Code's session configuration.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NOTIFIER_SOUND` | `chime` | Which sound to play: `bell`, `chime`, `subtle`, `complete`, `click`, `clicks`, `mech`, `mechs`, `thock`, or `thocks` |
| `NOTIFIER_VIBRATE_DURATION` | `200` | Vibration duration in milliseconds (Termux only) |
| `NOTIFIER_MODE` | `auto` | Notification mode: `auto`, `vibrate-only`, `sound-only`, or `both` |

### Sound Options

The plugin includes 10 notification sounds:

- **bell** - Classic bell tone with mixed frequencies
- **chime** - Pleasant high chime (default, recommended)
- **subtle** - Very short, quiet pop (minimal distraction)
- **complete** - Ascending three-note melody (satisfying completion sound)
- **click** - Single keyboard key click (mechanical and precise)
- **clicks** - Multiple keyboard clicks (rapid typing sound)
- **mech** - Realistic mechanical keyboard switch (authentic click-clack-thock)
- **mechs** - Multiple mechanical keyboard switches (satisfying typing sound)
- **thock** - Deep thock-focused keyboard (emphasized low frequency)
- **thocks** - Multiple deep thocks (bass-heavy typing sound)

### Configuration Examples

**Use a different sound**:
```bash
export NOTIFIER_SOUND=subtle
```

**Longer vibration on Termux**:
```bash
export NOTIFIER_VIBRATE_DURATION=500
```

**Force sound-only mode** (disable vibration even on Termux):
```bash
export NOTIFIER_MODE=sound-only
```

**Use both sound and vibration** (if both are available):
```bash
export NOTIFIER_MODE=both
```

### Setting Environment Variables in Claude Code

You can set these variables to persist across Claude Code sessions using the `SessionStart` hook:

1. Create `~/.claude-code/hooks/hooks.json` (or edit if it exists):
   ```json
   {
     "hooks": {
       "SessionStart": [
         {
           "matcher": "",
           "hooks": [
             {
               "type": "command",
               "command": "echo 'export NOTIFIER_SOUND=subtle' >> $CLAUDE_ENV_FILE"
             }
           ]
         }
       ]
     }
   }
   ```

## How It Works

The plugin uses Claude Code's **Notification hook** which triggers whenever Claude is:
- Awaiting user permission to run a command
- Waiting for user input
- Ready for the next prompt

When the hook triggers:

1. **On Desktop**: The script attempts to play the selected sound file using available audio players
2. **On Termux/Android**: The script triggers device vibration using `termux-vibrate`
3. **Fallback**: If no audio player or vibration is available, it falls back to the system bell (beep)

The notification runs asynchronously so it never blocks Claude Code's operation.

## Troubleshooting

### No sound on Linux

1. **Check if an audio player is installed**:
   ```bash
   command -v paplay || command -v aplay
   ```

2. **Install PulseAudio utilities** (recommended):
   ```bash
   sudo apt install pulseaudio-utils  # Debian/Ubuntu
   sudo dnf install pulseaudio-utils  # Fedora
   ```

3. **Test audio playback manually**:
   ```bash
   paplay /path/to/notifier/sounds/chime.wav
   ```

### No vibration on Termux

1. **Verify Termux:API is installed**:
   - Install from [F-Droid](https://f-droid.org/packages/com.termux.api/)
   - Grant all requested permissions in Android settings

2. **Install termux-api package**:
   ```bash
   pkg install termux-api
   ```

3. **Test vibration manually**:
   ```bash
   termux-vibrate -d 500
   ```

4. **Check permissions**: Ensure Termux has permission to vibrate in Android settings

### Sound files missing

If you cloned the repository without sound files, generate them:
```bash
python3 /path/to/notifier/scripts/generate-sounds.py
```

### Plugin not working

1. **Verify plugin is installed and enabled**:
   ```bash
   /plugin list
   ```

2. **Check the notification script is executable**:
   ```bash
   ls -l /path/to/notifier/scripts/play-notification.sh
   ```
   If not executable:
   ```bash
   chmod +x /path/to/notifier/scripts/play-notification.sh
   ```

3. **Test the notification script manually**:
   ```bash
   /path/to/notifier/scripts/play-notification.sh
   ```

## Customization

### Using Your Own Sound Files

You can replace any of the `.wav` files in the `sounds/` directory with your own:

1. Sound files must be in WAV format
2. Keep filenames the same: `bell.wav`, `chime.wav`, `subtle.wav`, `complete.wav`
3. Shorter sounds (&lt;1 second) work best for notifications

### Adding New Sounds

To add a new sound:

1. Add a `.wav` file to the `sounds/` directory (e.g., `sounds/custom.wav`)
2. Set the environment variable:
   ```bash
   export NOTIFIER_SOUND=custom
   ```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to:

- **Report issues**: https://github.com/convocli/notifier/issues
- **Suggest new features**: Open an issue with the "enhancement" label
- **Submit pull requests**: Fork the repo and create a PR
- **Share your custom notification sounds**: Create an issue with your sound file attached

### Development

To regenerate all sound files:

```bash
# Generate basic sounds
python3 scripts/generate-sounds.py

# Generate mechanical keyboard sounds
python3 scripts/add-mechanical-sound.py

# Generate thock sounds
python3 scripts/add-thock-sounds.py
```

To preview all sounds:

```bash
./scripts/preview-sounds.sh
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

Created by Marty for the Claude Code community.

**Repository**: https://github.com/convocli/notifier

---

**Enjoy distraction-free coding with subtle, helpful notifications from Claude Code!** 🔔✨
