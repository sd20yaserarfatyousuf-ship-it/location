# # import webbrowser
# # import threading
# # import json
# # from http.server import BaseHTTPRequestHandler, HTTPServer
# # import time
# # from threading import Event

# # # Shared data and event
# # result = {"lat": None, "lon": None, "accuracy": None}
# # received_event = Event()

# # PAGE = """<!doctype html>
# # <html>
# <head>
#   <meta charset="utf-8">
#   <title>Share your location</title>
#   <meta name="viewport" content="width=device-width,initial-scale=1">
#   <style>
#       body{font-family:sans-serif;text-align:center;padding:40px;}
#       .debug{background:#f0f0f0;padding:10px;margin:10px;font-family:monospace;}
#   </style>
# </head>
# <body>
#   <h2>Please allow access to your location</h2>
#   <p id="msg">Waiting for browser permission…</p>
#   <div id="debug" class="debug"></div>

# <script>
# function log(text) {
#     console.log(text);
#     document.getElementById("debug").innerHTML += text + "<br>";
# }

# function sendPosition(pos){
#     log("✅ Got location: " + pos.coords.latitude + ", " + pos.coords.longitude);
    
#     fetch("/submit_location",{
#         method:"POST",
#         headers:{"Content-Type":"application/json"},
#         body:JSON.stringify({
#             lat:pos.coords.latitude,
#             lon:pos.coords.longitude,
#             accuracy:pos.coords.accuracy
#         })
#     })
#     .then(response => {
#         log("📡 Server responded: " + response.status);
#         return response.text();
#     })
#     .then(data => {
#         log("✅ Server data: " + data);
#         document.getElementById("msg").textContent="Location sent ✓";
#         setTimeout(()=>window.close(),2000);
#     })
#     .catch(error => {
#         log("❌ Fetch error: " + error);
#         document.getElementById("msg").textContent="Send failed: " + error;
#     });
# }

# function handleError(err){
#     log("❌ Geolocation error: " + err.message);
#     document.getElementById("msg").textContent="Error: "+err.message;
# }

# log("🔍 Starting geolocation request...");
# navigator.geolocation.getCurrentPosition(sendPosition,handleError,
#                                          {enableHighAccuracy:true,timeout:15000,maximumAge:0});
# </script>
# </body>
# </html>"""

# class LocationHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         print(f"📥 GET request: {self.path}")
#         if self.path == "/":
#             self.send_response(200)
#             self.send_header("Content-Type", "text/html; charset=utf-8")
#             self.send_header("Content-Length", str(len(PAGE.encode())))
#             self.end_headers()
#             self.wfile.write(PAGE.encode())
#         else:
#             self.send_error(404)

#     def do_POST(self):
#         print(f"📨 POST request: {self.path}")
#         if self.path == "/submit_location":
#             try:
#                 content_length = int(self.headers.get("Content-Length", 0))
#                 body = self.rfile.read(content_length)
#                 print(f"📦 Received data: {body.decode()}")
                
#                 data = json.loads(body.decode())
#                 result.update(data)
#                 received_event.set()
                
#                 self.send_response(200)
#                 self.send_header("Content-Type", "application/json")
#                 self.send_header("Access-Control-Allow-Origin", "*")  # Add CORS
#                 self.end_headers()
#                 response = b'{"status":"success"}'
#                 self.wfile.write(response)
                
#                 print(f"✅ Location saved: {data['lat']}, {data['lon']}")
#             except Exception as e:
#                 print(f"❌ Error processing POST: {e}")
#                 self.send_error(500)
#         else:
#             self.send_error(404)

# def get_lat_lon(timeout=60, port=5055):  # Increased timeout
#     # Reset
#     result.update({"lat": None, "lon": None, "accuracy": None})
#     received_event.clear()

#     try:
#         # Start server in background
#         server = HTTPServer(("127.0.0.1", port), LocationHandler)
#         thread = threading.Thread(target=server.serve_forever)
#         thread.daemon = True
#         thread.start()

#         # Wait for server to be ready
#         time.sleep(1)
#         print(f"🖥️  Server started on http://127.0.0.1:{port}")

#         # Open browser
#         webbrowser.open(f"http://127.0.0.1:{port}/")
#         print("🌐 Browser opened – grant location permission…")
#         print("💡 Check browser console (F12) for debug messages")

#         if received_event.wait(timeout):
#             print(f"✅ Location received: {result['lat']}, {result['lon']}")
#         else:
#             print("❌ Timeout – no location received")
#             print("🔍 Check if you allowed location permission in browser")

#         server.shutdown()
#         server.server_close()

#     except Exception as e:
#         print(f"❌ Server error: {e}")

#     return result["lat"], result["lon"], result["accuracy"]

# # Example usage
# if __name__ == "__main__":
#     print("🚀 Starting location capture...")
#     lat, lon, acc = get_lat_lon()
    
#     if lat and lon:
#         print(f"\n📍 SUCCESS!")
#         print(f"📍 Latitude: {lat}")
#         print(f"📍 Longitude: {lon}")
#         print(f"📍 Accuracy: ±{acc} meters")
#     else:
#         print("\n❌ FAILED to get location")
#         print("💡 Common causes:")
#         print("   • Location permission denied")
#         print("   • Browser doesn't support geolocation")
#         print("   • Network/firewall blocking localhost")




# import webbrowser
# import threading
# import json
# from http.server import BaseHTTPRequestHandler, HTTPServer
# from threading import Event

# # Shared data and event
# result = {"lat": None, "lon": None, "accuracy": None}
# received_event = Event()

# HTML_PAGE = """<!DOCTYPE html>
# <html>
# <head>
#     <title>Get Location</title>
#     <style>body{font-family:sans-serif;text-align:center;padding:40px;}</style>
# </head>
# <body>
#     <h2>Getting your location...</h2>
#     <p id="status">Please allow location access when prompted</p>
#     <script>
#     function sendLocation(lat, lon, accuracy) {
#         fetch(window.location.origin + '/location', {
#             method: 'POST',
#             headers: {'Content-Type': 'application/json'},
#             body: JSON.stringify({lat, lon, accuracy})
#         }).then(() => {
#             document.getElementById('status').innerHTML =
#                 `✅ Location sent to Python!<br>
#                  Lat: ${lat.toFixed(6)}<br>
#                  Lon: ${lon.toFixed(6)}<br>
#                  Accuracy: ±${accuracy}m<br>
#                  <small>You can close this tab.</small>`;
#         }).catch(err => {
#             document.getElementById('status').innerHTML = "❌ Error sending location: " + err;
#         });
#     }

#     navigator.geolocation.getCurrentPosition(
#         pos => sendLocation(pos.coords.latitude, pos.coords.longitude, pos.coords.accuracy),
#         err => document.getElementById('status').innerHTML = `❌ Error: ${err.message}`,
#         {enableHighAccuracy: true, timeout: 10000}
#     );
#     </script>
# </body>
# </html>"""

# class LocationHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == "/":
#             print("[SERVER] Browser connected, serving HTML page")
#             self.send_response(200)
#             self.send_header("Content-Type", "text/html; charset=utf-8")
#             self.send_header("Content-Length", str(len(HTML_PAGE)))
#             self.end_headers()
#             self.wfile.write(HTML_PAGE)
#         else:
#             self.send_error(404)

#     def do_POST(self):
#         if self.path == "/location":
#             print("[SERVER] Location data received from browser")
#             content_length = int(self.headers.get("Content-Length", 0))
#             body = self.rfile.read(content_length)
#             data = json.loads(body.decode())
#             result.update(data)
#             received_event.set()
#             self.send_response(200)
#             self.end_headers()
#             self.wfile.write(b"OK")
#         else:
#             self.send_error(404)

# def get_lat_lon(port=5055):
#     result.update({"lat": None, "lon": None, "accuracy": None})
#     received_event.clear()

#     server = HTTPServer(("127.0.0.1", port), LocationHandler)
#     thread = threading.Thread(target=server.serve_forever)
#     thread.daemon = True
#     thread.start()

#     webbrowser.open(f"http://127.0.0.1:{port}/")
#     print("🌐 Browser opened – grant location permission…")
#     print("[WAITING] Waiting until browser sends location...")

#     received_event.wait()  # No timeout for testing
#     print("[DONE] Location received")

#     server.shutdown()
#     server.server_close()

#     return result["lat"], result["lon"], result["accuracy"]

# # Test run
# if __name__ == "__main__":
#     lat, lon, acc = get_lat_lon()
#     print(f"Latitude: {lat}")
#     print(f"Longitude: {lon}")
#     print(f"Accuracy: {acc} meters")
# Install: pip install selenium
# Download ChromeDriver from https://chromedriver.chromium.org/
# import webview
# import json
# import threading

# class LocationAPI:
#     def __init__(self):
#         self.location = None
#         self.event = threading.Event()
    
#     def save_location(self, lat, lon, accuracy):
#         self.location = {'lat': lat, 'lon': lon, 'accuracy': accuracy}
#         self.event.set()
#         return "Location saved!"

# def get_location_webview():
#     api = LocationAPI()
    
#     html_content = '''
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Location</title>
#         <style>body{font-family:Arial;text-align:center;padding:40px;}</style>
#     </head>
#     <body>
#         <h2>📍 Getting Location</h2>
#         <p id="status">Requesting location...</p>
        
#         <script>
#         navigator.geolocation.getCurrentPosition(
#             function(pos) {
#                 const lat = pos.coords.latitude;
#                 const lon = pos.coords.longitude;
#                 const acc = pos.coords.accuracy;
                
#                 // Call Python function directly
#                 pywebview.api.save_location(lat, lon, acc).then(result => {
#                     document.getElementById('status').innerHTML = 
#                         `✅ ${result}<br>Lat: ${lat.toFixed(6)}<br>Lon: ${lon.toFixed(6)}`;
#                 });
#             },
#             function(error) {
#                 document.getElementById('status').innerHTML = '❌ Error: ' + error.message;
#             },
#             {enableHighAccuracy: true, timeout: 10000}
#         );
#         </script>
#     </body>
#     </html>
#     '''
    
#     # Create window
#     window = webview.create_window('Location Finder', html=html_content, js_api=api)
#     webview.start(debug=False)
    
#     # Wait for location
#     api.event.wait()
    
#     return api.location['lat'], api.location['lon'], api.location['accuracy']

# # Usage
# if __name__ == "__main__":
#     try:
#         lat, lon, acc = get_location_webview()
#         print(f"📍 Latitude: {lat}")
#         print(f"📍 Longitude: {lon}")  
#         print(f"📍 Accuracy: ±{acc}m")
#     except ImportError:
#         print("❌ Install webview: pip install webview")

# import webbrowser
# import threading
# import json
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import time
# from threading import Event
# import subprocess
# import sys
# import os

# # Shared data and event
# result = {"lat": None, "lon": None, "accuracy": None}
# received_event = Event()

# PAGE = """<!doctype html>
# <html>
# <head>
#   <meta charset="utf-8">
#   <title>Share your location</title>
#   <meta name="viewport" content="width=device-width,initial-scale=1">
#   <style>
#       body{font-family:sans-serif;text-align:center;padding:40px;}
#       .debug{background:#f0f0f0;padding:10px;margin:10px;font-family:monospace;}
#   </style>
# </head>
# <body>
#   <h2>Please allow access to your location</h2>
#   <p id="msg">Waiting for browser permission…</p>
#   <div id="debug" class="debug"></div>

# <script>
# function log(text) {
#     console.log(text);
#     document.getElementById("debug").innerHTML += text + "<br>";
# }

# function sendPosition(pos){
#     log("✅ Got location: " + pos.coords.latitude + ", " + pos.coords.longitude);
    
#     fetch("/submit_location",{
#         method:"POST",
#         headers:{"Content-Type":"application/json"},
#         body:JSON.stringify({
#             lat:pos.coords.latitude,
#             lon:pos.coords.longitude,
#             accuracy:pos.coords.accuracy
#         })
#     })
#     .then(response => {
#         log("📡 Server responded: " + response.status);
#         return response.text();
#     })
#     .then(data => {
#         log("✅ Server data: " + data);
#         document.getElementById("msg").textContent="Location sent ✓";
#         setTimeout(()=>window.close(),2000);
#     })
#     .catch(error => {
#         log("❌ Fetch error: " + error);
#         document.getElementById("msg").textContent="Send failed: " + error;
#     });
# }

# function handleError(err){
#     log("❌ Geolocation error: " + err.message);
#     document.getElementById("msg").textContent="Error: "+err.message;
# }

# log("🔍 Starting geolocation request...");
# navigator.geolocation.getCurrentPosition(sendPosition,handleError,
#                                          {enableHighAccuracy:true,timeout:15000,maximumAge:0});
# </script>
# </body>
# </html>"""

# class LocationHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         print(f"📥 GET request: {self.path}")
#         if self.path == "/":
#             self.send_response(200)
#             self.send_header("Content-Type", "text/html; charset=utf-8")
#             self.send_header("Content-Length", str(len(PAGE.encode())))
#             self.end_headers()
#             self.wfile.write(PAGE.encode())
#         else:
#             self.send_error(404)

#     def do_POST(self):
#         print(f"📨 POST request: {self.path}")
#         if self.path == "/submit_location":
#             try:
#                 content_length = int(self.headers.get("Content-Length", 0))
#                 body = self.rfile.read(content_length)
#                 print(f"📦 Received data: {body.decode()}")
                
#                 data = json.loads(body.decode())
#                 result.update(data)
#                 received_event.set()
                
#                 self.send_response(200)
#                 self.send_header("Content-Type", "application/json")
#                 self.send_header("Access-Control-Allow-Origin", "*")
#                 self.end_headers()
#                 response = b'{"status":"success"}'
#                 self.wfile.write(response)
                
#                 print(f"✅ Location saved: {data['lat']}, {data['lon']}")
#             except Exception as e:
#                 print(f"❌ Error processing POST: {e}")
#                 self.send_error(500)
#         else:
#             self.send_error(404)
    
#     def log_message(self, format, *args):
#         pass  # Suppress HTTP server logs

# def is_admin():
#     """Check if running as administrator"""
#     try:
#         return os.getuid() == 0
#     except AttributeError:
#         import ctypes
#         try:
#             return ctypes.windll.shell32.IsUserAnAdmin()
#         except:
#             return False

# def disable_firewall():
#     """Disable Windows Firewall temporarily"""
#     try:
#         print("🔥 Disabling Windows Firewall temporarily...")
        
#         # Disable firewall for all profiles
#         commands = [
#             'netsh advfirewall set allprofiles state off'
#         ]
        
#         for cmd in commands:
#             result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             if result.returncode == 0:
#                 print("✅ Firewall disabled successfully")
#                 return True
#             else:
#                 print(f"⚠️  Firewall command failed: {result.stderr}")
#                 return False
                
#     except Exception as e:
#         print(f"❌ Error disabling firewall: {e}")
#         return False

# def enable_firewall():
#     """Re-enable Windows Firewall"""
#     try:
#         print("🔒 Re-enabling Windows Firewall...")
        
#         # Re-enable firewall for all profiles
#         commands = [
#             'netsh advfirewall set allprofiles state on'
#         ]
        
#         for cmd in commands:
#             result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             if result.returncode == 0:
#                 print("✅ Firewall re-enabled successfully")
#                 return True
#             else:
#                 print(f"⚠️  Firewall re-enable failed: {result.stderr}")
#                 return False
                
#     except Exception as e:
#         print(f"❌ Error re-enabling firewall: {e}")
#         return False

# def add_firewall_rule(port):
#     """Add specific firewall rule for the port"""
#     try:
#         print(f"🔧 Adding firewall rule for port {port}...")
        
#         rule_name = f"Python_Location_Server_{port}"
        
#         # Delete existing rule if it exists
#         subprocess.run(f'netsh advfirewall firewall delete rule name="{rule_name}"', 
#                       shell=True, capture_output=True)
        
#         # Add new rule
#         cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow protocol=TCP localport={port}'
#         result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
#         if result.returncode == 0:
#             print(f"✅ Firewall rule added for port {port}")
#             return True
#         else:
#             print(f"⚠️  Failed to add firewall rule: {result.stderr}")
#             return False
            
#     except Exception as e:
#         print(f"❌ Error adding firewall rule: {e}")
#         return False

# def remove_firewall_rule(port):
#     """Remove the specific firewall rule"""
#     try:
#         rule_name = f"Python_Location_Server_{port}"
#         cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
#         subprocess.run(cmd, shell=True, capture_output=True)
#         print(f"✅ Firewall rule removed for port {port}")
#     except:
#         pass

# def get_lat_lon(timeout=60, port=5055):
#     """Get location with automatic firewall handling"""
    
#     # Reset
#     result.update({"lat": None, "lon": None, "accuracy": None})
#     received_event.clear()
    
#     firewall_disabled = False
#     firewall_rule_added = False
    
#     try:
#         # Check if running as admin
#         if not is_admin():
#             print("⚠️  Running without administrator privileges")
#             print("💡 For automatic firewall management, run as administrator")
#             print("🔄 Trying to add firewall rule instead...")
            
#             # Try to add specific rule (doesn't require admin in some cases)
#             firewall_rule_added = add_firewall_rule(port)
#         else:
#             print("✅ Running as administrator")
#             # Try adding specific rule first (less disruptive)
#             firewall_rule_added = add_firewall_rule(port)
            
#             if not firewall_rule_added:
#                 print("🔄 Firewall rule failed, temporarily disabling firewall...")
#                 firewall_disabled = disable_firewall()
        
#         # Start server
#         server = HTTPServer(("127.0.0.1", port), LocationHandler)
#         thread = threading.Thread(target=server.serve_forever)
#         thread.daemon = True
#         thread.start()

#         # Wait for server to be ready
#         time.sleep(1)
#         print(f"🖥️  Server started on http://127.0.0.1:{port}")

#         # Open browser
#         webbrowser.open(f"http://127.0.0.1:{port}/")
#         print("🌐 Browser opened – grant location permission…")
#         print("💡 Check browser console (F12) for debug messages")

#         if received_event.wait(timeout):
#             print(f"✅ Location received: {result['lat']}, {result['lon']}")
#         else:
#             print("❌ Timeout – no location received")
#             print("🔍 Check if you allowed location permission in browser")

#         server.shutdown()
#         server.server_close()

#     except Exception as e:
#         print(f"❌ Server error: {e}")
    
#     finally:
#         # Always restore firewall settings
#         if firewall_disabled:
#             enable_firewall()
        
#         if firewall_rule_added:
#             remove_firewall_rule(port)
        
#         print("🔒 Firewall settings restored")

#     return result["lat"], result["lon"], result["accuracy"]

# def run_as_admin():
#     """Restart the script as administrator"""
#     try:
#         import ctypes
#         if ctypes.windll.shell32.IsUserAnAdmin():
#             return True  # Already admin
#         else:
#             print("🔄 Requesting administrator privileges...")
#             ctypes.windll.shell32.ShellExecuteW(
#                 None, "runas", sys.executable, 
#                 f'"{__file__}"', None, 1
#             )
#             return False  # Will restart as admin
#     except:
#         return True  # Continue anyway

# # Example usage
# if __name__ == "__main__":
#     print("🚀 Starting location capture with automatic firewall management...")
    
#     # Option to run as admin for better firewall control
#     choice = input("Run as administrator for automatic firewall management? (y/n): ").lower().strip()
    
#     if choice == 'y' and not is_admin():
#         if not run_as_admin():
#             print("🔄 Restarting as administrator...")
#             sys.exit()
    
#     lat, lon, acc = get_lat_lon()
    
#     if lat and lon:
#         print(f"\n📍 SUCCESS!")
#         print(f"📍 Latitude: {lat}")
#         print(f"📍 Longitude: {lon}")
#         print(f"📍 Accuracy: ±{acc} meters")
        
#         # Optional: Get address from coordinates
#         try:
#             from geopy.geocoders import Nominatim
#             geolocator = Nominatim(user_agent="location_finder")
#             location = geolocator.reverse(f"{lat}, {lon}")
#             print(f"🏠 Address: {location.address}")
#         except ImportError:
#             print("💡 Install geopy for address lookup: pip install geopy")
#         except:
#             pass
            
#     else:
#         print("\n❌ FAILED to get location")
#         print("💡 Common causes:")
#         print("   • Location permission denied in browser")
#         print("   • Browser doesn't support geolocation")
#         print("   • Still blocked by security software")
#         print("\n🔧 Manual solutions:")
#         print("   • Try running as administrator")
#         print("   • Temporarily disable antivirus")
#         print("   • Use a different browser")


# import webbrowser
# import threading
# import json
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import time
# from threading import Event
# import subprocess
# import sys
# import os

# # Shared data and event
# result = {"lat": None, "lon": None, "accuracy": None}
# received_event = Event()

# PAGE = """<!doctype html>
# <html>
# <head>
#   <meta charset="utf-8">
#   <title>Share your location</title>
#   <meta name="viewport" content="width=device-width,initial-scale=1">
#   <style>
#       body{font-family:sans-serif;text-align:center;padding:40px;}
#       .debug{background:#f0f0f0;padding:10px;margin:10px;font-family:monospace;}
#   </style>
# </head>
# <body>
#   <h2>Please allow access to your location</h2>
#   <p id="msg">Waiting for browser permission…</p>
#   <div id="debug" class="debug"></div>

# <script>
# function log(text) {
#     console.log(text);
#     document.getElementById("debug").innerHTML += text + "<br>";
# }

# function sendPosition(pos){
#     log("✅ Got location: " + pos.coords.latitude + ", " + pos.coords.longitude);
    
#     fetch("/submit_location",{
#         method:"POST",
#         headers:{"Content-Type":"application/json"},
#         body:JSON.stringify({
#             lat:pos.coords.latitude,
#             lon:pos.coords.longitude,
#             accuracy:pos.coords.accuracy
#         })
#     })
#     .then(response => {
#         log("📡 Server responded: " + response.status);
#         return response.text();
#     })
#     .then(data => {
#         log("✅ Server data: " + data);
#         document.getElementById("msg").textContent="Location sent ✓";
#         setTimeout(()=>window.close(),2000);
#     })
#     .catch(error => {
#         log("❌ Fetch error: " + error);
#         document.getElementById("msg").textContent="Send failed: " + error;
#     });
# }

# function handleError(err){
#     log("❌ Geolocation error: " + err.message);
#     document.getElementById("msg").textContent="Error: "+err.message;
# }

# log("🔍 Starting geolocation request...");
# navigator.geolocation.getCurrentPosition(sendPosition,handleError,
#                                          {enableHighAccuracy:true,timeout:15000,maximumAge:0});
# </script>
# </body>
# </html>"""

# class LocationHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         print(f"📥 GET request: {self.path}")
#         if self.path == "/":
#             self.send_response(200)
#             self.send_header("Content-Type", "text/html; charset=utf-8")
#             self.send_header("Content-Length", str(len(PAGE.encode())))
#             self.end_headers()
#             self.wfile.write(PAGE.encode())
#         else:
#             self.send_error(404)

#     def do_POST(self):
#         print(f"📨 POST request: {self.path}")
#         if self.path == "/submit_location":
#             try:
#                 content_length = int(self.headers.get("Content-Length", 0))
#                 body = self.rfile.read(content_length)
#                 print(f"📦 Received data: {body.decode()}")
                
#                 data = json.loads(body.decode())
#                 result.update(data)
#                 received_event.set()
                
#                 self.send_response(200)
#                 self.send_header("Content-Type", "application/json")
#                 self.send_header("Access-Control-Allow-Origin", "*")
#                 self.end_headers()
#                 response = b'{"status":"success"}'
#                 self.wfile.write(response)
                
#                 print(f"✅ Location saved: {data['lat']}, {data['lon']}")
#             except Exception as e:
#                 print(f"❌ Error processing POST: {e}")
#                 self.send_error(500)
#         else:
#             self.send_error(404)
    
#     def log_message(self, format, *args):
#         pass  # Suppress HTTP server logs

# def is_admin():
#     """Check if running as administrator"""
#     try:
#         return os.getuid() == 0
#     except AttributeError:
#         import ctypes
#         try:
#             return ctypes.windll.shell32.IsUserAnAdmin()
#         except:
#             return False

# def disable_firewall():
#     """Disable Windows Firewall temporarily"""
#     try:
#         print("🔥 Disabling Windows Firewall temporarily...")
        
#         # Disable firewall for all profiles
#         commands = [
#             'netsh advfirewall set allprofiles state off'
#         ]
        
#         for cmd in commands:
#             result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             if result.returncode == 0:
#                 print("✅ Firewall disabled successfully")
#                 return True
#             else:
#                 print(f"⚠️  Firewall command failed: {result.stderr}")
#                 return False
                
#     except Exception as e:
#         print(f"❌ Error disabling firewall: {e}")
#         return False

# def enable_firewall():
#     """Re-enable Windows Firewall"""
#     try:
#         print("🔒 Re-enabling Windows Firewall...")
        
#         # Re-enable firewall for all profiles
#         commands = [
#             'netsh advfirewall set allprofiles state on'
#         ]
        
#         for cmd in commands:
#             result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             if result.returncode == 0:
#                 print("✅ Firewall re-enabled successfully")
#                 return True
#             else:
#                 print(f"⚠️  Firewall re-enable failed: {result.stderr}")
#                 return False
                
#     except Exception as e:
#         print(f"❌ Error re-enabling firewall: {e}")
#         return False

# def add_firewall_rule(port):
#     """Add specific firewall rule for the port"""
#     try:
#         print(f"🔧 Adding firewall rule for port {port}...")
        
#         rule_name = f"Python_Location_Server_{port}"
        
#         # Delete existing rule if it exists
#         subprocess.run(f'netsh advfirewall firewall delete rule name="{rule_name}"', 
#                       shell=True, capture_output=True)
        
#         # Add new rule
#         cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow protocol=TCP localport={port}'
#         result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
#         if result.returncode == 0:
#             print(f"✅ Firewall rule added for port {port}")
#             return True
#         else:
#             print(f"⚠️  Failed to add firewall rule: {result.stderr}")
#             return False
            
#     except Exception as e:
#         print(f"❌ Error adding firewall rule: {e}")
#         return False

# def remove_firewall_rule(port):
#     """Remove the specific firewall rule"""
#     try:
#         rule_name = f"Python_Location_Server_{port}"
#         cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
#         subprocess.run(cmd, shell=True, capture_output=True)
#         print(f"✅ Firewall rule removed for port {port}")
#     except:
#         pass

# def get_lat_lon(timeout=60, port=5055):
#     """Get location with automatic firewall handling"""
    
#     # Reset
#     result.update({"lat": None, "lon": None, "accuracy": None})
#     received_event.clear()
    
#     firewall_disabled = False
#     firewall_rule_added = False
    
#     try:
#         # Check if running as admin
#         if not is_admin():
#             print("⚠️  Running without administrator privileges")
#             print("💡 For automatic firewall management, run as administrator")
#             print("🔄 Trying to add firewall rule instead...")
            
#             # Try to add specific rule (doesn't require admin in some cases)
#             firewall_rule_added = add_firewall_rule(port)
#         else:
#             print("✅ Running as administrator")
#             # Try adding specific rule first (less disruptive)
#             firewall_rule_added = add_firewall_rule(port)
            
#             if not firewall_rule_added:
#                 print("🔄 Firewall rule failed, temporarily disabling firewall...")
#                 firewall_disabled = disable_firewall()
        
#         # Start server
#         server = HTTPServer(("127.0.0.1", port), LocationHandler)
#         thread = threading.Thread(target=server.serve_forever)
#         thread.daemon = True
#         thread.start()

#         # Wait for server to be ready
#         time.sleep(1)
#         print(f"🖥️  Server started on http://127.0.0.1:{port}")

#         # Open browser
#         webbrowser.open(f"http://127.0.0.1:{port}/")
#         print("🌐 Browser opened – grant location permission…")
#         print("💡 Check browser console (F12) for debug messages")

#         if received_event.wait(timeout):
#             print(f"✅ Location received: {result['lat']}, {result['lon']}")
#         else:
#             print("❌ Timeout – no location received")
#             print("🔍 Check if you allowed location permission in browser")

#         server.shutdown()
#         server.server_close()

#     except Exception as e:
#         print(f"❌ Server error: {e}")
    
#     finally:
#         # Always restore firewall settings
#         if firewall_disabled:
#             enable_firewall()
        
#         if firewall_rule_added:
#             remove_firewall_rule(port)
        
#         print("🔒 Firewall settings restored")

#     return result["lat"], result["lon"], result["accuracy"]

# def run_as_admin():
#     """Restart the script as administrator"""
#     try:
#         import ctypes
#         if ctypes.windll.shell32.IsUserAnAdmin():
#             return True  # Already admin
#         else:
#             print("🔄 Requesting administrator privileges...")
#             ctypes.windll.shell32.ShellExecuteW(
#                 None, "runas", sys.executable, 
#                 f'"{__file__}"', None, 1
#             )
#             return False  # Will restart as admin
#     except:
#         return True  # Continue anyway

# # Example usage
# if __name__ == "__main__":
#     print("🚀 Starting location capture with automatic firewall management...")
    
#     # Option to run as admin for better firewall control
#     choice = input("Run as administrator for automatic firewall management? (y/n): ").lower().strip()
    
#     if choice == 'y' and not is_admin():
#         if not run_as_admin():
#             print("🔄 Restarting as administrator...")
#             sys.exit()
    
#     lat, lon, acc = get_lat_lon()
    
#     if lat and lon:
#         print(f"\n📍 SUCCESS!")
#         print(f"📍 Latitude: {lat}")
#         print(f"📍 Longitude: {lon}")
#         print(f"📍 Accuracy: ±{acc} meters")
        
#         # Optional: Get address from coordinates
#         try:
#             from geopy.geocoders import Nominatim
#             geolocator = Nominatim(user_agent="location_finder")
#             location = geolocator.reverse(f"{lat}, {lon}")
#             print(f"🏠 Address: {location.address}")
#         except ImportError:
#             print("💡 Install geopy for address lookup: pip install geopy")
#         except:
#             pass
            
#     else:
#         print("\n❌ FAILED to get location")
#         print("💡 Common causes:")
#         print("   • Location permission denied in browser")
#         print("   • Browser doesn't support geolocation")
#         print("   • Still blocked by security software")
#         print("\n🔧 Manual solutions:")
#         print("   • Try running as administrator")
#         print("   • Temporarily disable antivirus")
#         print("   • Use a different browser")


import requests

def get_lat_lon():
    try:
        response = requests.get("http://127.0.0.1:5000/get-location")
        data = response.json()
        if data.get('status') == 'success':
            return data.get('lat'), data.get('lon')
    except Exception as e:
        print(f"Error fetching location: {e}")
    return None, None

if __name__ == "__main__":
    lat, lon = get_lat_lon()
    print(f"Latitude: {lat}, Longitude: {lon}")
