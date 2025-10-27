#!/bin/bash
#
# Preview all notification sounds
# Helps users choose their preferred notification sound
#

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the plugin root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Claude Code Notifier - Sound Preview              ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo ""
echo -e "${YELLOW}Playing all notification sounds...${NC}"
echo ""

# Array of sounds with descriptions
declare -A sounds
sounds=(
    ["bell"]="Classic bell tone - bright and attention-getting"
    ["chime"]="Pleasant high chime - gentle and musical (DEFAULT)"
    ["subtle"]="Very short, quiet pop - minimal distraction"
    ["complete"]="Ascending melody - satisfying completion sound"
    ["click"]="Single keyboard key click - mechanical and precise"
    ["clicks"]="Multiple keyboard clicks - rapid typing sound"
    ["mech"]="Realistic mechanical keyboard switch - authentic thock"
    ["mechs"]="Multiple mechanical keyboard switches - satisfying typing"
    ["thock"]="Deep thock-focused keyboard - emphasized low frequency"
    ["thocks"]="Multiple deep thocks - bass-heavy typing sound"
)

# Play each sound
for sound in bell chime subtle complete click clicks mech mechs thock thocks; do
    echo -e "${GREEN}▶${NC} ${sound}.wav - ${sounds[$sound]}"

    # Play the sound using the notification script
    NOTIFIER_SOUND=$sound "$SCRIPT_DIR/play-notification.sh"

    # Wait between sounds
    sleep 1.5
done

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo "To set your preferred sound, use one of these methods:"
echo ""
echo -e "  ${GREEN}1. Using the configuration command:${NC}"
echo "     /notifier:configure"
echo ""
echo -e "  ${GREEN}2. Set environment variable in your shell profile:${NC}"
echo "     export NOTIFIER_SOUND=subtle"
echo ""
echo -e "  ${GREEN}3. Set for current session only:${NC}"
echo "     NOTIFIER_SOUND=subtle"
echo ""
echo "Available sounds: bell, chime, subtle, complete, click, clicks, mech, mechs, thock, thocks"
echo ""
