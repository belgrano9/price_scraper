# Advanced DataDome Bypass Techniques

This document explains the cutting-edge anti-detection techniques implemented in version 0.2.0 of the SNCF Price Scraper.

## Table of Contents

1. [Overview](#overview)
2. [Mouse Movement Simulation](#mouse-movement-simulation)
3. [Fingerprint Spoofing](#fingerprint-spoofing)
4. [Timing Patterns](#timing-patterns)
5. [Session Management](#session-management)
6. [Behavioral Patterns](#behavioral-patterns)
7. [Configuration Options](#configuration-options)
8. [Success Rate Optimization](#success-rate-optimization)

## Overview

DataDome is one of the most sophisticated bot detection systems, using multiple layers of detection:

- **Browser Fingerprinting**: Canvas, WebGL, Audio, Fonts, Plugins
- **Behavioral Analysis**: Mouse movements, timing, scrolling patterns
- **TLS Fingerprinting**: Network-level detection
- **JavaScript Challenges**: Dynamic code execution tests
- **Machine Learning**: Pattern recognition across multiple signals

Our advanced implementation counters each of these detection vectors.

## Mouse Movement Simulation

### Bezier Curve Movements

**Problem**: Bots move the mouse in perfectly straight lines, which is inhuman.

**Solution**: We implement Bezier curves to create natural, curved mouse paths.

```python
# Generate curve from point A to B
curve_points = bezier_curve(start=(100, 200), end=(800, 600), control_points=2)

# Move mouse along curve with variable speed
for point in curve_points:
    page.mouse.move(point[0], point[1])
    time.sleep(variable_delay)
```

**Key Features**:
- Random control points for path variation
- 20-40 steps per movement (randomized)
- Variable speed: slower at start/end, faster in middle
- Mimics human acceleration/deceleration

### Element Hovering

The scraper randomly hovers over clickable elements to simulate natural browsing:

```python
# Find and hover over interactive elements
element = page.query_selector("button, a, input")
hover_with_bezier_curve(element)
```

## Fingerprint Spoofing

### Canvas Fingerprinting

**Detection Method**: DataDome renders hidden canvases and hashes the output. Each browser produces a unique hash.

**Our Countermeasure**:
```javascript
// Inject minimal noise into canvas data
const context = canvas.getContext('2d');
const imageData = context.getImageData(0, 0, width, height);
for (let i = 0; i < imageData.data.length; i += 4) {
    imageData.data[i] += Math.floor(Math.random() * 3) - 1;  // ±1 pixel noise
}
```

This adds imperceptible noise that changes the canvas hash without affecting visual output.

### WebGL Fingerprinting

**Detection Method**: GPU renderer and vendor strings are queried for fingerprinting.

**Our Countermeasure**:
```javascript
WebGLRenderingContext.prototype.getParameter = function(parameter) {
    if (parameter === 37445) return 'Intel Inc.';  // UNMASKED_VENDOR
    if (parameter === 37446) return 'Intel Iris OpenGL Engine';  // UNMASKED_RENDERER
    return originalGetParameter.apply(this, arguments);
};
```

We return common, realistic values instead of the actual GPU info.

### Audio Context Fingerprinting

**Detection Method**: Audio signal processing produces unique fingerprints based on hardware.

**Our Countermeasure**:
```javascript
// Add minimal noise to audio data
AudioBuffer.prototype.getChannelData = function() {
    const data = originalGetChannelData.apply(this, arguments);
    for (let i = 0; i < data.length; i += 100) {
        data[i] += Math.random() * 0.0001 - 0.00005;
    }
    return data;
};
```

### Navigator Properties

**Detection Method**: Checking for `navigator.webdriver`, plugins, and other automation indicators.

**Our Countermeasures**:
- Override `navigator.webdriver` to return `undefined`
- Spoof realistic plugin array (PDF viewer, Native Client)
- Randomize battery API values
- Ensure screen depth consistency (24-bit)
- Match timezone to target location (Europe/Paris for SNCF)

### Viewport Randomization

**Problem**: Bots often use standard resolutions (1920x1080).

**Solution**: Randomize viewport from common real-world resolutions:

```python
common_resolutions = [
    (1920, 1080),  # Full HD
    (1366, 768),   # Common laptop
    (1440, 900),   # MacBook
    (2560, 1440),  # QHD
]

# Add random variance and account for browser chrome
viewport = randomize_viewport()
page.set_viewport_size(viewport)
```

## Timing Patterns

### Gaussian Distribution Delays

**Problem**: `random.uniform()` creates flat distribution, which is detectable.

**Solution**: Use Gaussian (normal) distribution for more realistic delays:

```python
def gaussian_delay(min_seconds, max_seconds):
    mean = (min_seconds + max_seconds) / 2
    std_dev = (max_seconds - min_seconds) / 6
    delay = random.gauss(mean, std_dev)
    delay = max(min_seconds, min(max_seconds, delay))  # Clamp to range
    time.sleep(delay)
```

This produces a bell curve of delays, matching human behavior better.

### Typing Delays

**Problem**: Instant text input is obviously automated.

**Solution**: Type character-by-character with realistic delays:

```python
def human_typing_delay():
    base_delay = random.uniform(0.08, 0.15)  # 40-60 WPM
    # Occasional hesitation (10% chance)
    if random.random() < 0.1:
        base_delay += random.uniform(0.3, 0.8)
    return base_delay

# Usage
for char in text:
    page.keyboard.type(char)
    time.sleep(human_typing_delay())
```

This mimics real human typing with occasional pauses for "thinking".

## Session Management

### Cookie Persistence

**Benefit**: Reusing cookies from successful sessions reduces suspicion.

**Implementation**:

```python
# Save cookies after successful scrape
bypass.save_cookies(page, session_name="sncf_session_1")

# Load cookies on next run
bypass.load_cookies(page, session_name="sncf_session_1")
```

**How it helps**:
- Bypasses "new visitor" checks
- Reuses validated DataDome tokens
- Builds session history
- Reduces challenge frequency

### Session Directory

Cookies are stored in `data/sessions/{session_name}_cookies.json`

## Behavioral Patterns

### Scrolling with Inertia

**Problem**: Bots scroll in fixed increments.

**Solution**: Simulate physics-based scrolling with deceleration:

```python
def scroll_with_inertia(total_distance):
    steps = random.randint(8, 15)
    for i in range(steps):
        # More distance at start, less at end (deceleration)
        step_distance = int(total_distance * (1 - i/steps) / steps * 2)
        page.evaluate(f"window.scrollBy(0, {step_distance})")
        time.sleep(random.uniform(0.02, 0.05))

    # Human imprecision - small random adjustment
    adjustment = random.randint(-50, 50)
    page.evaluate(f"window.scrollBy(0, {adjustment})")
```

### Challenge Handling

**Strategy**: When DataDome challenge detected:

1. **Don't panic**: Wait patiently (up to 90 seconds)
2. **Stay active**: Continue mouse movements and scrolling
3. **Vary behavior**: Hover over elements, scroll randomly
4. **Check periodically**: Test if challenge resolved every 2-4 seconds
5. **Be human**: Use Gaussian delays, not fixed intervals

```python
while challenge_present and time_remaining:
    if check_interval % 3 == 0:
        human_like_mouse_movement(page)
    if check_interval % 4 == 0:
        random_scroll_with_inertia(page)
    if check_interval % 5 == 0:
        hover_random_element(page)

    gaussian_delay(2, 4)
    check_if_resolved()
```

## Configuration Options

### Basic Usage

```python
from src.scraper import SNCFScraper

# Standard mode
scraper = SNCFScraper(
    headless=False,
    debug=True,
    use_advanced=True  # Enable all advanced techniques
)
```

### Advanced Usage

```python
scraper = SNCFScraper(
    headless=False,           # Visible browser (recommended)
    debug=True,               # Enable logging and screenshots
    use_advanced=True,        # Use advanced bypass techniques
    session_name="my_session", # Session for cookie persistence
    proxy="http://proxy:8080" # Optional proxy server
)

results = scraper.scrape(
    origin="Paris",
    destination="Lyon",
    date="2024-12-15",
    passengers=1
)
```

### Component-Level Usage

You can use individual components directly:

```python
from src.datadome_advanced import AdvancedDataDomeBypass

bypass = AdvancedDataDomeBypass()

# Use specific techniques
bypass.inject_fingerprint_spoofing(page)
bypass.human_like_mouse_movement(page, target_x=500, target_y=300)
bypass.random_scroll_with_inertia(page)
bypass.gaussian_delay(1, 3)
```

## Success Rate Optimization

### Best Practices

1. **Use Visible Browser** (`headless=False`)
   - DataDome detects headless browsers more easily
   - 30-40% higher success rate with visible browser

2. **Enable Cookie Persistence**
   - Reuse sessions for better trust scores
   - Use consistent session names

3. **Use Residential Proxies**
   - Datacenter IPs are heavily penalized
   - Residential IPs have 60-70% higher success rate

4. **Run During Off-Peak Hours**
   - Less scrutiny during low-traffic periods
   - European timezone for SNCF (UTC+1/+2)

5. **Don't Rush**
   - Let challenges resolve naturally
   - 90-second timeout is reasonable

6. **Maintain Sessions**
   - Don't clear cookies between runs
   - Build up session history

### Troubleshooting

**If challenges persist:**

1. Check internet connection stability
2. Try different proxy/IP
3. Increase timeout values
4. Review debug screenshots
5. Verify viewport randomization is working
6. Ensure fingerprint scripts are injecting

**Debug mode provides:**
- Detailed console logging with timestamps
- Screenshots saved to `data/` directory
- Cookie save/load confirmation
- Viewport dimensions used
- Challenge detection events

## Technical Details

### Detection Vectors Countered

| Detection Vector | Our Countermeasure | Effectiveness |
|-----------------|-------------------|---------------|
| Canvas Fingerprint | Noise injection | High |
| WebGL Fingerprint | Parameter spoofing | High |
| Audio Fingerprint | Data perturbation | High |
| Mouse Patterns | Bezier curves | Very High |
| Timing Analysis | Gaussian delays | High |
| Typing Patterns | Human-like delays | Very High |
| Scroll Behavior | Inertia simulation | High |
| Navigator Props | Property override | Very High |
| Viewport Size | Randomization | Medium |
| Cookie Absence | Session persistence | High |
| TLS Fingerprint | Camoufox handling | High |

### Architecture

```
┌─────────────────┐
│   SNCFScraper   │
│    (main)       │
└────────┬────────┘
         │
         ├──► DataDomeBypass (basic)
         │    └──► Simple delays
         │    └──► Basic mouse movement
         │
         └──► AdvancedDataDomeBypass
              ├──► Bezier curves
              ├──► Fingerprint spoofing
              ├──► Gaussian timing
              ├──► Session management
              └──► Advanced detection
```

## Limitations

Even with these advanced techniques:

1. **Not 100% Success Rate**: DataDome continuously evolves
2. **Speed Trade-off**: More realistic = slower execution
3. **Proxy Dependency**: Success heavily depends on IP reputation
4. **Site Changes**: SNCF may update their site structure
5. **Rate Limits**: Too many requests will still get blocked

## Ethical Considerations

⚠️ **Important Reminders**:

- These techniques are for **educational purposes only**
- Respect website Terms of Service
- Don't overload servers with requests
- Use rate limiting between scrapes
- Consider using official APIs when available

## References

- [Camoufox Documentation](https://github.com/daijro/camoufox)
- [DataDome Bot Detection](https://datadome.co/bot-management-protection/)
- [Canvas Fingerprinting Research](https://browserleaks.com/canvas)
- [WebGL Fingerprinting](https://browserleaks.com/webgl)
- [Human Behavior Patterns](https://en.wikipedia.org/wiki/Fitts%27s_law)

---

**Version**: 0.2.0
**Last Updated**: 2024-11-20
**Status**: Active Development
