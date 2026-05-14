# Background Remover

A compact GUI application for removing white backgrounds from images while preserving gradients as transparency.

## Features

- **Drag-and-drop** interface for easy image loading
- **Preserves gradients** - converts black-to-white gradients into transparency levels
- **Batch processing** - process multiple images without restarting
- **Compact design** - minimalist 400x400px window
- **Standalone EXE** - no Python installation required to run

## Preview

The application features a simple interface:
- Drag-and-drop area with image preview (350x300px)
- Single "Remove Background" button
- No title bar clutter - just the essentials

## How It Works

1. Converts image to grayscale
2. Inverts brightness to create alpha channel:
   - White (255) → Fully transparent (alpha=0)
   - Gray (128) → Semi-transparent (alpha=127)
   - Black (0) → Fully opaque (alpha=255)
3. Saves as PNG with transparency

**Why PNG?** GIF format doesn't support semi-transparency (gradient alpha), only binary transparency.

## Building for Windows

### Requirements (for building only)

- Windows 10/11
- Python 3.8+ with "Add to PATH" enabled
- **Note:** Python is only needed for building, not for running the EXE!

### Quick Build

1. Copy all project files to Windows PC (including `Mad6d.gif`)
2. Run `build_windows_advanced.bat` (double-click)
3. Wait 2-5 minutes
4. Get your EXE from `dist\BackgroundRemover.exe`

### Manual Build

```cmd
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Create icon (optional - bat script does this)
python create_icon.py Mad6d.gif

# Build standalone EXE
pyinstaller --clean BackgroundRemover.spec
```

Result: `dist\BackgroundRemover.exe` (~20-50 MB)

## Using the Application

1. Launch `BackgroundRemover.exe`
2. Drag and drop an image into the window
3. Click "Remove Background"
4. Find your transparent PNG in the same folder with `_transparent.png` suffix

**You can process multiple images in a row** - just drag the next image after the previous one finishes!

## Application Icon

The project includes `Mad6d.gif` as the application icon. The build scripts automatically convert it to `app_icon.ico` and embed it in the EXE.

### Custom Icon

To use your own icon:

```cmd
python create_icon.py your_image.gif
```

This creates `app_icon.ico` with multiple sizes (16x16, 32x32, 48x48, 64x64, 128x128, 256x256).

## Project Files

**Core Application:**
- `background_remover_gui.py` - Main GUI application
- `BackgroundRemover.spec` - PyInstaller configuration

**Icon Resources:**
- `Mad6d.gif` - Source icon image (166 KB)
- `app_icon.ico` - Compiled icon (136 KB, auto-generated)
- `create_icon.py` - Icon conversion script

**Build Scripts:**
- `build_windows_advanced.bat` - Recommended build script
- `build_windows.bat` - Basic build script
- `requirements.txt` - Python dependencies

**Additional:**
- `remove_white_bg.py` - Console version (no GUI)
- `README.md` - This file

## Technical Details

**Interface:**
- Window size: 400x400 pixels
- No title bar text (only window controls)
- Drag-and-drop zone: 350x300 pixels
- Preview thumbnail: max 320x270 pixels
- Single blue button for processing

**Dependencies:**
- Pillow (PIL) - Image processing
- tkinterdnd2 - Drag-and-drop support
- tkinter - GUI framework (built-in)

**Output:**
- Format: PNG (supports semi-transparency)
- Naming: `original_transparent.png`
- Location: Same folder as source image

## Troubleshooting

**PyInstaller not found:**
```cmd
pip install --upgrade pip
pip install pyinstaller
```

**tkinterdnd2 import error:**
```cmd
pip uninstall tkinterdnd2
pip install tkinterdnd2
```

**EXE doesn't start:**
- Check antivirus (may block PyInstaller apps)
- Run as administrator
- Rebuild with `--debug=all` flag

**Drag-and-drop not working:**
The standalone EXE should work fine. If you're running from source and have issues, ensure tkinterdnd2 is properly installed.

## System Requirements

**For running the EXE:**
- Windows 10/11 (64-bit)
- 100 MB free disk space
- Screen resolution: minimum 800x600

**For building:**
- Python 3.8 or higher
- pip package manager
- Internet connection (for downloading dependencies)

## Best Practices

**Optimal image types:**
- Black illustrations on white background
- Line art and drawings
- Logo designs with gradients
- Any grayscale image where white = unwanted background

**Not recommended for:**
- Color images (converts to grayscale)
- Complex backgrounds (designed for white backgrounds)
- Photos with subtle color gradients

## License

Free to use and modify.

## Notes

- The application is optimized for black-and-white images
- Gradients are preserved as alpha channel transparency
- You can process unlimited images without restarting
- The EXE is completely standalone - no Python installation needed
