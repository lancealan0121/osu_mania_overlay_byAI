# osu! OL Mode - Keyboard Visualizer
A beautiful osu!mania keyboard press visualizer with customizable styles, particle effects, KPS display, song tracking, and more.

## 🆕 Updates

### Version 1.1 (February 2, 2026)

#### **New Features**
- ✨ **osu! Song Tracker Integration**
  - Real-time song information display (artist, title, difficulty)
  - Customizable colors for song name and difficulty
  - Adjustable position and font size for song info
  - Custom "no song playing" message
  - Toggle to enable/disable song tracking

- 🎨 **Enhanced Window Customization**
  - Manual window size control (custom width and height)
  - Toggle between automatic and manual window sizing
  - "Center Window" button to quickly center the overlay on screen
  - Suggested window height display based on visualization settings

- 🎯 **Individual Key Positioning**
  - Right-click and drag individual keys to reposition them
  - "Reset Key Positions" button to restore default layout
  - Custom positions persist across sessions

#### **Improvements**
- ✅ Fixed visual display rendering issues
- ✅ Removed unnecessary UI elements for cleaner interface
- ✅ Updated all language translation files with new features
- ✅ Improved settings GUI layout and organization
- ✅ Optimized internal logic for better performance
- ✅ Enhanced window position management

#### **Technical Changes**
- Added `OsuTrackerThread` for background song detection via Windows API
- Implemented `win32gui` integration for osu! window title parsing
- Enhanced configuration system with new settings:
  - `enable_osu_tracker`, `show_song_info`
  - `song_info_color`, `song_difficulty_color`, `song_no_playing_text`
  - `custom_window_size`, `window_width`, `window_height`
  - `use_custom_positions`, `key_custom_positions`

---

## ✨ Features

### Visual Effects
- 🎵 Real-time key press visualization with smooth animations
- 📊 KPS (Keys Per Second) display with MAX KPS tracking
- ✨ Multiple particle effects (circles, squares, stars)
- 🌈 Rainbow mode with adjustable speed
- 💫 Glow effects with customizable colors and intensity
- 🌊 Trail effects for enhanced visual feedback

### Customization
- 🎨 Comprehensive settings interface with tabbed layout
- 🌍 Multi-language support
- 🎮 Combo counter with customizable reset time
- 📈 Statistics tracking (total presses, session time)
- 🔧 Customizable key shapes (rounded, square, circle, hexagon)
- 🎭 Multiple animation styles (default, wave, pulse, bounce, elastic)

### osu! Integration
- 🎵 Automatic song detection from osu! client
- 📝 Display artist, song title, and difficulty
- 🎨 Customizable song info colors and position
- 🔄 Real-time updates while playing

### Interface
- 🖥️ Transparent overlay with adjustable opacity
- 🎯 Draggable window and individual key positioning
- ⚡ Real-time settings preview
- 💾 Persistent configuration across sessions
- ⌨️ Customizable hotkey to toggle settings window

---

## 📋 Requirements

- **Python** 3.8 or higher
- **Operating System:** Windows (required for keyboard hooks and osu! integration)
- **Dependencies:**
  - PySide6 (Qt6 bindings)
  - keyboard (for key press detection)
  - pywin32 (for osu! window detection)

---

## 🚀 Installation

1. **Install Python dependencies:**
   ```bash
   pip install PySide6 keyboard pywin32
   ```

2. **Run the program:**
   ```bash
   python main.py
   ```

3. **Optional - Create standalone executable:**
   ```bash
   pyinstaller --onefile --windowed --add-data "languages;languages" main.py
   ```

---

## 📖 How to Use

### First Launch
1. Launch the program - the splash screen will appear, followed by the settings window
2. Configure your monitored keys in the **"Key Settings"** tab
3. Adjust visual effects and display options as desired
4. Click **"Save Settings"** to apply changes
5. The overlay window will appear - position it where you want
6. Start playing and enjoy the visual effects!

### Window Controls
- **Left-click and drag** the overlay to move it
- **Right-click and drag** individual keys to reposition them
- Press **F1** (or your configured hotkey) to toggle the settings window
- Use the **"Center Window"** button to quickly center the overlay

### osu! Song Tracker Setup
1. Go to the **"Combo & Stats"** tab
2. Check **"Enable osu! Song Tracker"**
3. Customize song info display settings:
   - Adjust position with X/Y offset sliders
   - Change font size
   - Select colors for song name and difficulty
   - Set custom "no song playing" message
4. Launch osu! and start playing - song info will appear automatically

---

## ⚙️ Main Settings

### Layout Tab
- **Key Dimensions:** Width, height, spacing
- **Background:** Opacity control
- **Window Size:** Auto/manual sizing, custom dimensions
- **Positioning:** Reset key positions, center window

### KPS Settings Tab
- **Display Options:** Toggle KPS display, font size, position offsets
- **Color Mode:** Dynamic color change or custom static color
- **MAX KPS:** Toggle MAX display, auto-switch after idle time
- **Reset Button:** Clear MAX KPS record

### Effects Options Tab
- **Physics:** Spring stiffness, press scale
- **Animation Style:** Default, wave, pulse, bounce, elastic
- **Key Shape:** Rounded, square, circle, hexagon
- **Borders:** Width, glow on press, rotation effects
- **Particles:** Count, gravity, explosion force, decay speed, size range, shapes

### Visual Effects Tab
- **Glow:** Spread, intensity, cooldown, color modes (key color, white, rainbow, custom)
- **Visualization:** Note height, scroll speed, opacity, gradient effects
- **Trails:** Toggle and length adjustment
- **Rainbow Mode:** Enable and adjust speed
- **Shake Effects:** Toggle and intensity

### Combo & Stats Tab
- **Combo Counter:** Enable and adjust reset time
- **Statistics:** Total presses, session time, reset button
- **osu! Tracker:** Enable song detection, customize display
- **Key Count Display:** Show individual key press counts, font size, color

### Key Settings Tab
- **Key Count:** Set number of monitored keys (1-20)
- **Key Bindings:** Click buttons to set keybinds
- **Colors:** Customize individual key colors

### Window Settings Tab
- **Performance:** FPS limit (30-500)
- **Hotkeys:** Configure settings toggle key
- **Language:** Select interface language

---

## 🎨 Customization Options

### Animation Styles
- **Default:** Smooth scaling animation
- **Wave:** Sinusoidal wave effect
- **Pulse:** Pulsating press effect
- **Bounce:** Bouncy press animation
- **Elastic:** Spring-like elastic effect

### Key Shapes
- **Rounded Rectangle:** Default smooth corners
- **Square:** Sharp 90-degree corners
- **Circle:** Perfect circular keys
- **Hexagon:** Six-sided polygon keys

### Particle Shapes
- **Circle:** Round particles
- **Square:** Rectangular particles with rotation
- **Star:** Five-pointed star particles

### Glow Color Modes
- **Key Color:** Match the key's assigned color
- **White:** Pure white glow
- **Rainbow:** Cycling rainbow colors
- **Custom:** Choose any color

---

## 🔧 Configuration

All settings are automatically saved in `osu_OL_v1_config.json` and persist between sessions. You can manually edit this file if needed, but it's recommended to use the settings interface.

### Language Files
Place custom language JSON files in the `languages/` folder. Format:
```json
{
  "window_title": "Your Translation",
  "save_button": "Your Translation",
  ...
}
```

---

## 📸 Screenshots

### Settings Interface
![Settings Window](screenshots/setting.png)

### Live Preview
![Display](screenshots/preview.png)

---

## 🐛 Troubleshooting

**Keys not responding:**
- Check that the correct keys are configured
- Ensure the program has keyboard input permissions
- Try running as administrator

**osu! song info not showing:**
- Make sure osu! is running
- Make sure osu! version is "stable"
- Check that "Enable osu! Song Tracker" is enabled
- Verify you're actively playing a song (not in menu)

**Performance issues:**
- Lower the FPS limit in Window Settings
- Reduce particle count in Effects Options
- Disable some visual effects

**Settings not saving:**
- Check file permissions in the program directory
- Ensure `osu_OL_v1_config.json` is not read-only

---

## 📝 License

Made by yulun with ❤️ (yulun loves AI generated)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Create language translation files

---

## 🔮 Planned Features

- Audio visualizer integration
- More particle effects
- Custom themes system
- Profile system for quick setting switches
- Replay file visualization
- Performance optimizations
