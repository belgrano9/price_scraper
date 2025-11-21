"""
Advanced DataDome bypass strategies using state-of-the-art anti-detection techniques.

This module implements cutting-edge evasion methods including:
- Bezier curve mouse movements
- Advanced fingerprint spoofing (Canvas, WebGL, Audio)
- Sophisticated behavioral patterns
- TLS fingerprint management
- Cookie and session persistence
"""

import json
import math
import random
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class AdvancedDataDomeBypass:
    """Advanced DataDome detection evasion using latest techniques."""

    def __init__(self, session_dir: Optional[str] = None):
        """
        Initialize advanced DataDome bypass handler.

        Args:
            session_dir: Directory to store session data and cookies
        """
        self.cookies = {}
        self.last_request_time = 0
        self.session_dir = Path(session_dir) if session_dir else Path("data/sessions")
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.mouse_position = (0, 0)

    # ==================== ADVANCED MOUSE MOVEMENTS ====================

    def bezier_curve(self, start: Tuple[int, int], end: Tuple[int, int],
                     control_points: int = 2) -> List[Tuple[int, int]]:
        """
        Generate Bezier curve points for realistic mouse movement.

        Args:
            start: Starting (x, y) position
            end: Ending (x, y) position
            control_points: Number of control points for curve complexity

        Returns:
            List of (x, y) coordinates along the Bezier curve
        """
        # Generate random control points
        controls = []
        for _ in range(control_points):
            x = random.randint(min(start[0], end[0]), max(start[0], end[0]))
            y = random.randint(min(start[1], end[1]), max(start[1], end[1]))
            controls.append((x, y))

        # All points: start + controls + end
        all_points = [start] + controls + [end]

        # Generate curve with 20-40 steps
        steps = random.randint(20, 40)
        curve_points = []

        for i in range(steps + 1):
            t = i / steps
            point = self._bezier_point(all_points, t)
            curve_points.append(point)

        return curve_points

    def _bezier_point(self, points: List[Tuple[int, int]], t: float) -> Tuple[int, int]:
        """
        Calculate point on Bezier curve at parameter t using De Casteljau's algorithm.

        Args:
            points: Control points
            t: Parameter (0 to 1)

        Returns:
            (x, y) coordinate at parameter t
        """
        if len(points) == 1:
            return points[0]

        new_points = []
        for i in range(len(points) - 1):
            x = (1 - t) * points[i][0] + t * points[i + 1][0]
            y = (1 - t) * points[i][1] + t * points[i + 1][1]
            new_points.append((int(x), int(y)))

        return self._bezier_point(new_points, t)

    def human_like_mouse_movement(self, page, target_x: Optional[int] = None,
                                  target_y: Optional[int] = None) -> None:
        """
        Simulate realistic human mouse movement using Bezier curves.

        Args:
            page: Camoufox page object
            target_x: Target X coordinate (random if None)
            target_y: Target Y coordinate (random if None)
        """
        try:
            viewport = page.viewport_size
            if not viewport:
                viewport = {"width": 1920, "height": 1080}

            # Determine target position
            if target_x is None:
                target_x = random.randint(100, viewport["width"] - 100)
            if target_y is None:
                target_y = random.randint(100, viewport["height"] - 100)

            # Generate Bezier curve path
            start = self.mouse_position
            end = (target_x, target_y)
            curve_points = self.bezier_curve(start, end, control_points=random.randint(1, 3))

            # Move mouse along curve with variable speed
            for i, (x, y) in enumerate(curve_points):
                # Variable delay - faster in middle, slower at ends
                progress = i / len(curve_points)
                if progress < 0.2 or progress > 0.8:
                    delay = random.uniform(0.01, 0.03)  # Slower at start/end
                else:
                    delay = random.uniform(0.005, 0.015)  # Faster in middle

                page.mouse.move(x, y)
                time.sleep(delay)

            self.mouse_position = end

        except Exception as e:
            print(f"Advanced mouse movement failed: {e}")

    def random_scroll_with_inertia(self, page) -> None:
        """
        Perform realistic scrolling with inertia simulation.

        Args:
            page: Camoufox page object
        """
        try:
            # Determine scroll direction and distance
            scroll_distance = random.randint(300, 1000)
            direction = random.choice([1, -1])

            # Scroll in steps with decreasing speed (inertia effect)
            steps = random.randint(8, 15)
            for i in range(steps):
                # Deceleration: more distance at start, less at end
                step_distance = int(scroll_distance * (1 - i / steps) / steps * 2)
                page.evaluate(f"window.scrollBy(0, {step_distance * direction})")
                time.sleep(random.uniform(0.02, 0.05))

            # Small random adjustment (human imprecision)
            if random.random() > 0.5:
                adjustment = random.randint(-50, 50)
                page.evaluate(f"window.scrollBy(0, {adjustment})")

            self.gaussian_delay(0.5, 1.5)

        except Exception as e:
            print(f"Scroll simulation failed: {e}")

    # ==================== TIMING PATTERNS ====================

    def gaussian_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
        """
        Introduce delays with Gaussian distribution for more realistic timing.

        Args:
            min_seconds: Minimum delay
            max_seconds: Maximum delay
        """
        mean = (min_seconds + max_seconds) / 2
        std_dev = (max_seconds - min_seconds) / 6

        # Generate delay with Gaussian distribution
        delay = random.gauss(mean, std_dev)
        delay = max(min_seconds, min(max_seconds, delay))  # Clamp to range

        time.sleep(delay)

    def human_typing_delay(self) -> float:
        """
        Generate realistic delay between keystrokes.

        Returns:
            Delay in seconds
        """
        # Most humans type at 40-60 WPM (words per minute)
        # Average ~200-300ms per character with variations
        base_delay = random.uniform(0.08, 0.15)

        # Occasional longer pauses (thinking/hesitation)
        if random.random() < 0.1:
            base_delay += random.uniform(0.3, 0.8)

        return base_delay

    # ==================== FINGERPRINT MANIPULATION ====================

    def inject_fingerprint_spoofing(self, page) -> None:
        """
        Inject JavaScript to spoof browser fingerprints.

        Args:
            page: Camoufox page object
        """
        try:
            # Inject script before page loads
            page.add_init_script("""
                // Canvas fingerprint spoofing
                const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                HTMLCanvasElement.prototype.toDataURL = function() {
                    // Add minimal noise to canvas
                    const context = this.getContext('2d');
                    if (context) {
                        const imageData = context.getImageData(0, 0, this.width, this.height);
                        for (let i = 0; i < imageData.data.length; i += 4) {
                            imageData.data[i] += Math.floor(Math.random() * 3) - 1;
                        }
                        context.putImageData(imageData, 0, 0);
                    }
                    return originalToDataURL.apply(this, arguments);
                };

                // WebGL fingerprint spoofing
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) {  // UNMASKED_VENDOR_WEBGL
                        return 'Intel Inc.';
                    }
                    if (parameter === 37446) {  // UNMASKED_RENDERER_WEBGL
                        return 'Intel Iris OpenGL Engine';
                    }
                    return getParameter.apply(this, arguments);
                };

                // Audio context fingerprint spoofing
                const originalGetChannelData = AudioBuffer.prototype.getChannelData;
                AudioBuffer.prototype.getChannelData = function() {
                    const data = originalGetChannelData.apply(this, arguments);
                    for (let i = 0; i < data.length; i += 100) {
                        data[i] += Math.random() * 0.0001 - 0.00005;
                    }
                    return data;
                };

                // Navigator properties spoofing
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });

                // Battery API spoofing (often used for fingerprinting)
                if (navigator.getBattery) {
                    const originalGetBattery = navigator.getBattery;
                    navigator.getBattery = async function() {
                        const battery = await originalGetBattery.apply(this);
                        Object.defineProperties(battery, {
                            charging: { get: () => Math.random() > 0.5 },
                            chargingTime: { get: () => Math.random() * 3600 },
                            dischargingTime: { get: () => Math.random() * 7200 },
                            level: { get: () => 0.5 + Math.random() * 0.5 }
                        });
                        return battery;
                    };
                }

                // Plugin array spoofing
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {name: 'Chrome PDF Plugin', description: 'Portable Document Format', filename: 'internal-pdf-viewer'},
                        {name: 'Chrome PDF Viewer', description: '', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                        {name: 'Native Client', description: '', filename: 'internal-nacl-plugin'}
                    ]
                });

                // Screen depth and color depth consistency
                Object.defineProperty(screen, 'colorDepth', {
                    get: () => 24
                });
                Object.defineProperty(screen, 'pixelDepth', {
                    get: () => 24
                });

                // Timezone consistency
                const originalDateTimeFormat = Intl.DateTimeFormat.prototype.resolvedOptions;
                Intl.DateTimeFormat.prototype.resolvedOptions = function() {
                    const options = originalDateTimeFormat.call(this);
                    options.timeZone = 'Europe/Paris';  // Match SNCF location
                    return options;
                };

                console.log('[Fingerprint Spoofing] Injected successfully');
            """)

        except Exception as e:
            print(f"Fingerprint spoofing injection failed: {e}")

    def randomize_viewport(self) -> Dict[str, int]:
        """
        Generate realistic randomized viewport dimensions.

        Returns:
            Dictionary with width and height
        """
        # Common real-world screen resolutions
        common_resolutions = [
            (1920, 1080),  # Full HD
            (1366, 768),   # Common laptop
            (1536, 864),   # Scaled HD
            (1440, 900),   # MacBook
            (1920, 1200),  # WUXGA
            (2560, 1440),  # QHD
        ]

        # Pick a resolution and add small random variance
        base_width, base_height = random.choice(common_resolutions)

        # Account for browser chrome (address bar, bookmarks, etc.)
        # Subtract 50-150px from height
        height_reduction = random.randint(50, 150)

        return {
            "width": base_width + random.randint(-10, 10),
            "height": base_height - height_reduction + random.randint(-10, 10)
        }

    # ==================== CHALLENGE DETECTION ====================

    def check_datadome_challenge(self, page) -> bool:
        """
        Advanced DataDome challenge detection.

        Args:
            page: Camoufox page object

        Returns:
            True if challenge detected
        """
        try:
            # Multiple detection methods
            detection_methods = [
                self._check_url_indicators(page),
                self._check_dom_indicators(page),
                self._check_network_indicators(page),
                self._check_javascript_indicators(page)
            ]

            return any(detection_methods)

        except Exception as e:
            print(f"Error checking DataDome challenge: {e}")
            return False

    def _check_url_indicators(self, page) -> bool:
        """Check URL for DataDome indicators."""
        url = page.url
        indicators = ["geo.captcha-delivery.com", "datadome.co", "interstitial"]
        return any(indicator in url for indicator in indicators)

    def _check_dom_indicators(self, page) -> bool:
        """Check DOM for DataDome elements."""
        try:
            # Check for DataDome specific elements
            selectors = [
                "iframe[src*='datadome']",
                "div[id*='datadome']",
                "[class*='dd-']",
                "script[src*='datadome']"
            ]

            for selector in selectors:
                if page.query_selector(selector):
                    return True

            # Check page text
            body_text = page.evaluate("document.body ? document.body.innerText : ''")
            challenge_texts = [
                "checking your browser",
                "please wait",
                "verifying you are human",
                "security check"
            ]

            return any(text in body_text.lower() for text in challenge_texts)

        except:
            return False

    def _check_network_indicators(self, page) -> bool:
        """Check network requests for DataDome."""
        # This would require request interception
        # For now, return False
        return False

    def _check_javascript_indicators(self, page) -> bool:
        """Check for DataDome JavaScript presence."""
        try:
            has_datadome = page.evaluate("""
                () => {
                    // Check for DataDome global objects
                    if (window.ddvs || window.DD || window.dataDomeOptions) {
                        return true;
                    }

                    // Check for DataDome cookies
                    if (document.cookie.includes('datadome')) {
                        return true;
                    }

                    return false;
                }
            """)
            return has_datadome
        except:
            return False

    def handle_datadome_challenge(self, page, max_wait: int = 90) -> bool:
        """
        Advanced challenge handling with sophisticated behavioral patterns.

        Args:
            page: Camoufox page object
            max_wait: Maximum wait time in seconds

        Returns:
            True if challenge resolved
        """
        try:
            print("🤖 DataDome challenge detected - initiating advanced bypass...")

            start_time = time.time()
            check_interval = 0

            while time.time() - start_time < max_wait:
                # Vary behavior patterns
                check_interval += 1

                if check_interval % 3 == 0:
                    # Natural mouse movements
                    self.human_like_mouse_movement(page)

                if check_interval % 4 == 0:
                    # Scrolling with inertia
                    self.random_scroll_with_inertia(page)

                if check_interval % 5 == 0:
                    # Hover over random elements
                    self._hover_random_element(page)

                # Realistic waiting
                self.gaussian_delay(2, 4)

                # Check if challenge resolved
                if not self.check_datadome_challenge(page):
                    print("✓ DataDome challenge resolved successfully!")
                    return True

                if check_interval % 10 == 0:
                    print(f"  Still waiting... ({int(time.time() - start_time)}s)")

            print("✗ Failed to resolve DataDome challenge within timeout")
            return False

        except Exception as e:
            print(f"Error handling challenge: {e}")
            return False

    def _hover_random_element(self, page) -> None:
        """Hover over a random clickable element."""
        try:
            # Find interactive elements
            element = page.query_selector("button, a, input, [role='button']")
            if element:
                box = element.bounding_box()
                if box:
                    target_x = int(box["x"] + box["width"] / 2)
                    target_y = int(box["y"] + box["height"] / 2)
                    self.human_like_mouse_movement(page, target_x, target_y)
        except:
            pass

    # ==================== SESSION MANAGEMENT ====================

    def save_cookies(self, page, session_name: str = "default") -> None:
        """
        Save cookies for session persistence.

        Args:
            page: Camoufox page object
            session_name: Name for this session
        """
        try:
            cookies = page.context.cookies()
            cookie_file = self.session_dir / f"{session_name}_cookies.json"

            with open(cookie_file, 'w') as f:
                json.dump(cookies, f, indent=2)

            print(f"✓ Cookies saved to {cookie_file}")

        except Exception as e:
            print(f"Failed to save cookies: {e}")

    def load_cookies(self, page, session_name: str = "default") -> bool:
        """
        Load cookies from previous session.

        Args:
            page: Camoufox page object
            session_name: Name of session to load

        Returns:
            True if cookies loaded successfully
        """
        try:
            cookie_file = self.session_dir / f"{session_name}_cookies.json"

            if not cookie_file.exists():
                return False

            with open(cookie_file, 'r') as f:
                cookies = json.load(f)

            page.context.add_cookies(cookies)
            print(f"✓ Cookies loaded from {cookie_file}")
            return True

        except Exception as e:
            print(f"Failed to load cookies: {e}")
            return False

    # ==================== ADVANCED CONFIGURATION ====================

    def get_advanced_stealth_config(self) -> dict:
        """
        Get advanced Camoufox configuration with maximum stealth.

        Returns:
            Dictionary of Camoufox configuration options
        """
        return {
            "humanize": True,  # Enable humanization
            "geoip": True,  # Randomize geolocation
            "screen": self.randomize_viewport(),  # Custom viewport
            "os": "windows" if random.random() > 0.3 else "macos",  # OS randomization
            "addons": [],  # No suspicious addons
        }

    def get_realistic_headers(self) -> Dict[str, str]:
        """
        Generate realistic browser headers that match real Firefox traffic.

        Returns:
            Dictionary of HTTP headers
        """
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "TE": "trailers"
        }

    def wait_for_page_load(self, page, timeout: int = 30000) -> bool:
        """
        Advanced page load waiting with challenge detection.

        Args:
            page: Camoufox page object
            timeout: Timeout in milliseconds

        Returns:
            True if page loaded successfully
        """
        try:
            # Wait for network to settle
            page.wait_for_load_state("networkidle", timeout=timeout)

            # Additional wait for dynamic content
            self.gaussian_delay(1, 2)

            # Check for DataDome
            if self.check_datadome_challenge(page):
                return self.handle_datadome_challenge(page)

            return True

        except Exception as e:
            print(f"Page load error: {e}")
            return False
