
# 🎙️ OffScribe

### *Powerful Offline Speech-to-Text for macOS*

<p align="center">
  <em>Transform your voice into text instantly with complete privacy</em>
</p>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
![Apple Silicon](https://img.shields.io/badge/Apple%20Silicon-000000?style=for-the-badge&logo=apple&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

[![GitHub stars](https://img.shields.io/github/stars/vatsalkul/offscribe?style=for-the-badge)](https://github.com/yourusername/offscribe/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/vatsalkul/offscribe?style=for-the-badge)](https://github.com/yourusername/offscribe/network)
[![GitHub issues](https://img.shields.io/github/issues/vatsalkul/offscribe?style=for-the-badge)](https://github.com/yourusername/offscribe/issues)

</div>

---

## ✨ Features

<table>
<tr>
<td>

**🔒 Complete Privacy**
- 100% offline processing
- No internet required
- Your audio never leaves your device

</td>
<td>

**⚡ Lightning Fast**
- Optimized for Apple Silicon
- MLX Whisper integration
- Real-time transcription

</td>
</tr>
<tr>
<td>

**🎯 Smart Integration**
- Global hotkey support
- Auto-paste to any app
- Works with VS Code, Terminal, etc.

</td>
<td>

**🔊 Audio Feedback**
- Clear sound cues
- Recording status indicators
- Error notifications

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- 🍎 **macOS 13+** (Apple Silicon recommended)
- 🐍 **Python 3.8+**
- 🎤 **Microphone access**


## 📦 Installation

```bash
git clone https://github.com/yourusername/offscribe.git
cd offscribe

python3 -m venv transcriber
source transcriber/bin/activate  # On macOS/Linux

pip install -r requirements.txt

```

## Usage

1. Activate your virtual environment (if not already active):
```bash
source transcriber/bin/activate  # On macOS/Linux
```

2. Start the application:
```bash
python3 main.py
```

3. **Grant accessibility permissions** when prompted:
   - **Required for keyboard monitoring and auto-paste functionality**
   - You'll need to add your terminal app (Terminal, iTerm2, etc.) to accessibility permissions
   - **For VS Code users**: Also add VS Code to accessibility permissions for seamless pasting
   - Go to: System Settings → Privacy & Security → Accessibility

4. Use the transcriptor:
   - Click on any text field where you want to transcribe
   - **Double-click Left Ctrl** to start recording (you'll hear a "Pop" sound)
   - Speak clearly into your microphone
   - **Double-click Left Ctrl** again to stop recording (you'll hear a "Blow" sound)
   - Wait for transcription (you'll hear a "Glass" sound when complete)
   - The transcribed text will be automatically pasted into your text field

### Alternative Mode (No Accessibility Permissions)

If you prefer not to grant accessibility permissions, the app will run in simple mode:
- Type `s` and press Enter to start recording
- Type `q` and press Enter to stop recording
- The transcribed text will be copied to your clipboard

## How It Works

1. **Audio Capture**: Records audio at 16kHz using your default microphone
2. **Local Processing**: Uses MLX Whisper (large-v3-turbo) model for transcription
3. **Smart Integration**: Automatically pastes transcribed text into the active application
4. **Feedback System**: Provides audio cues for each stage of the process

## Audio Feedback Sounds

- 🔵 **Pop**: Recording started
- 🌬️ **Blow**: Recording stopped
- 🥂 **Glass**: Transcription successful
- 📢 **Basso**: Error occurred

## Troubleshooting

### Accessibility Permissions
If the hotkeys aren't working or auto-paste isn't functioning:
1. Go to System Settings > Privacy & Security > Accessibility
2. Add the following apps to the allowed list:
   - **Terminal** (or iTerm2, Warp, etc. - whatever you're running Python from)
   - **VS Code** (if you're coding - essential for pasting transcribed text)
   - **Any other apps** where you want to use transcription
3. **Important**: You may need to toggle the permissions off and back on
4. Restart the application after granting permissions

**Note**: Without accessibility permissions, the app will fall back to simple clipboard mode (no auto-paste).

### Audio Issues
- Ensure your microphone is properly connected
- Check System Settings > Sound > Input to verify your microphone is selected
- The app uses your system's default audio input device

### Performance
- First transcription may be slower as the model loads
- Subsequent transcriptions will be faster
- For best performance, use an Apple Silicon Mac

## Configuration

Currently, the application uses default settings optimized for general use:
- Model: `mlx-community/whisper-large-v3-turbo`
- Sample Rate: 16kHz
- Auto-paste: Enabled
- Hotkey: Double-click Left Ctrl

## Privacy

This application is completely offline:
- No internet connection required
- Audio is processed locally on your device
- No data is sent to external servers
- Temporary audio files are automatically deleted after transcription

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [MLX Whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper)
- Uses Apple's MLX framework for optimized performance
- Audio feedback using macOS system sounds
