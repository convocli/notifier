---
description: Configure notification sound and vibration settings for the Notifier plugin
---

# Configure Notifier Sound

Interactive configuration for the Claude Code Notifier plugin.

This command helps you:
- Choose your preferred notification sound
- Set vibration duration (for Termux/Android)
- Configure notification mode
- Test your settings immediately

**Available Sounds:**
- **bell** - Classic bell tone (bright, attention-getting)
- **chime** - Pleasant high chime (gentle, musical) - DEFAULT
- **subtle** - Very short, quiet pop (minimal distraction)
- **complete** - Ascending melody (satisfying completion sound)
- **click** - Single keyboard key click (mechanical and precise)
- **clicks** - Multiple keyboard clicks (rapid typing sound)
- **mech** - Realistic mechanical keyboard switch (authentic click-clack-thock)
- **mechs** - Multiple mechanical keyboard switches (satisfying typing sound)
- **thock** - Deep thock-focused keyboard (emphasized low frequency)
- **thocks** - Multiple deep thocks (bass-heavy typing sound)

**Configuration Options:**
- `NOTIFIER_SOUND` - Which sound to play
- `NOTIFIER_VIBRATE_DURATION` - Vibration duration in milliseconds (default: 200)
- `NOTIFIER_MODE` - auto, vibrate-only, sound-only, or both

## Interactive Setup

First, let's preview all sounds so you can choose:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/preview-sounds.sh
```

Now, please tell me:
1. Which sound would you like to use? (bell/chime/subtle/complete/click/clicks/mech/mechs/thock/thocks)
2. Are you using Termux/Android? (yes/no)
3. If yes, what vibration duration would you like? (milliseconds, default 200)

Based on your answers, I'll provide the exact commands to configure your notifier plugin, including:
- Adding the configuration to your shell profile (~/.bashrc or ~/.zshrc)
- Testing the configuration immediately
- Verifying it works with Claude Code

**Quick Set Commands:**

To set a specific sound immediately:
```bash
export NOTIFIER_SOUND=subtle
```

To make it permanent, add to your ~/.bashrc or ~/.zshrc:
```bash
echo 'export NOTIFIER_SOUND=subtle' >> ~/.bashrc
source ~/.bashrc
```

**Test Your Configuration:**
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/play-notification.sh
```
