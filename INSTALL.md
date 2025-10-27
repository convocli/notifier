# Installation Guide

Quick installation guide for the Claude Code Notifier Plugin.

## Quick Install (5 minutes)

### Step 1: Clone the Repository

```bash
cd ~/code-projects  # Or your preferred directory
git clone https://github.com/convocli/notifier.git
cd notifier
```

### Step 2: Create Plugin Marketplace

```bash
mkdir -p ~/.claude/plugins/marketplaces/local/.claude-plugin
```

### Step 3: Configure Marketplace

Get your plugin path:
```bash
cd ~/code-projects/notifier
pwd
```

Create marketplace.json in **TWO locations** (both required):

1. `~/.claude/plugins/marketplaces/local/marketplace.json` (ROOT)
2. `~/.claude/plugins/marketplaces/local/.claude-plugin/marketplace.json`

**Content for BOTH files:**
```json
{
  "name": "local",
  "owner": {"name": "Local", "url": ""},
  "description": "Local marketplace",
  "plugins": [
    {
      "name": "notifier",
      "source": "PASTE_YOUR_PATH_HERE",
      "version": "1.0.0",
      "description": "Cross-platform notification plugin"
    }
  ]
}
```

Replace `PASTE_YOUR_PATH_HERE` with the output from `pwd` above.

### Step 4: Install in Claude Code

Open Claude Code and run:
```
/plugin install local:notifier
```

### Step 5: Verify

```
/plugin list
```

You should see `notifier` in the installed plugins list.

### Step 6: Test

```
/notifier:preview
```

This will play all 10 sounds! Choose your favorite and configure it:

```bash
export NOTIFIER_SOUND=thock
```

## Termux/Android Quick Install

**Note:** These instructions assume you already have Termux installed on Android.

### Prerequisites (for vibration support)

1. Install the termux-api package in Termux:
   ```bash
   pkg install termux-api
   ```

2. Install the Termux:API companion app from F-Droid: https://f-droid.org/packages/com.termux.api/

3. Grant vibration permission:
   - Android Settings → Apps → Termux:API → Permissions
   - Enable "Vibrate"

### Installation

Follow Steps 1-6 above. The plugin will automatically use vibration on Termux!

Test vibration:
```bash
termux-vibrate -d 200
```

## Configuration

### Available Sounds

- **bell** - Classic bell tone
- **chime** - Pleasant high chime (DEFAULT)
- **subtle** - Very short, quiet pop
- **complete** - Ascending three-note melody
- **click** - Single keyboard click
- **clicks** - Multiple keyboard clicks
- **mech** - Realistic mechanical keyboard
- **mechs** - Multiple mechanical keyboards
- **thock** - Deep bass-heavy keyboard
- **thocks** - Multiple deep bass-heavy keyboards

### Set Your Favorite Sound

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
export NOTIFIER_SOUND=thock
```

Then reload:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

### Termux Configuration

For longer vibration (default is 200ms):
```bash
export NOTIFIER_VIBRATE_DURATION=500
```

### Force Mode

To force sound or vibration mode:
```bash
export NOTIFIER_MODE=sound-only     # Desktop: force sound
export NOTIFIER_MODE=vibrate-only   # Termux: force vibration
export NOTIFIER_MODE=both           # Both if available
export NOTIFIER_MODE=auto           # Default: auto-detect
```

## Troubleshooting

### No sound on Linux

Install PulseAudio utilities:
```bash
sudo apt install pulseaudio-utils  # Debian/Ubuntu
sudo dnf install pulseaudio-utils  # Fedora
```

Test manually:
```bash
paplay ~/code-projects/notifier/sounds/chime.wav
```

### No vibration on Termux

1. Check Termux:API is installed:
   ```bash
   pkg list-installed | grep termux-api
   ```

2. Test vibration directly:
   ```bash
   termux-vibrate -d 500
   ```

3. Check permissions in Android Settings.

### Plugin not found

Make sure the path in `marketplace.json` is **absolute** (starts with `/`), not relative.

Check with:
```bash
cat ~/.claude-code/marketplaces/local/marketplace.json
```

### Sound files missing

If sounds don't play, regenerate them:
```bash
cd ~/code-projects/notifier
python3 scripts/generate-sounds.py
python3 scripts/add-mechanical-sound.py
python3 scripts/add-thock-sounds.py
```

## Uninstallation

To remove the plugin:

```
/plugin uninstall notifier
```

To completely remove:
```bash
rm -rf ~/code-projects/notifier
```

And remove the `notifier` entry from `~/.claude-code/marketplaces/local/marketplace.json`.

## Getting Help

- Report issues: https://github.com/convocli/notifier/issues
- Documentation: https://github.com/convocli/notifier/blob/main/README.md
