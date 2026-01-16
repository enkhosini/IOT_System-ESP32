https://towardsaws.com/how-to-build-a-three-tier-end-to-end-devsecops-pipeline-from-code-to-production-with-zero-3af51213161b# ESP32 WebSocket + HTTP: Problems & Causes

This document summarizes the main issues encountered while developing an ESP32 WebSocket + HTTP + JSON project, along with their possible causes.

---

## 1. Guru Meditation / LoadProhibited Crash
- **Symptom:** ESP32 crashes after connecting to Wi-Fi or WebSocket; backtrace shows invalid memory address (`EXCVADDR`)
- **Possible Causes:**  
  - Writing directly to WebSocket `payload`  
  - Using `deserializeJson()` without passing the correct `length`  
  - Blocking operations (HTTP POST, Serial prints) inside WebSocket callback  

---

## 2. HTTP POST Failures
- **Symptom:** HTTP requests fail or do not reach the esp backend  
- **Possible Causes:**  
  - Calling `HTTPClient` inside WebSocket callback  
  - Incorrect URL, IP, or port  
  - Server unreachable  

---

## 3. ESP32 Memory / Heap Issues
- **Symptom:** Sporadic crashes, unstable behavior, Serial output stops responding  
- **Possible Causes:**  
  - Excessive `String` usage without `.reserve()` → heap fragmentation  
  - `StaticJsonDocument` too small → JSON overflow  
  - Blocking operations inside callbacks  

---

## 4. JSON Parsing / Serialization Errors
- **Symptom:** LED does not toggle according to `desired_state`  
- **Possible Causes:**  
  - Payload not null-terminated; `length` not provided  
  - Accessing JSON keys without checking `containsKey()`  
  - JSON document too small for data  

---

## 5. LED / GPIO Inconsistencies
- **Symptom:** LED state does not match desired state from server  
- **Possible Causes:**  
  - Toggling GPIO inside a blocking callback  
  - Race conditions with network tasks / memory fragmentation  

---

## Notes / Key Takeaways
- Never write into WebSocket `payload`; always copy data into a `String` or buffer  
- Always provide `length` when deserializing WebSocket payloads  
- Avoid blocking HTTP requests inside callbacks; defer to `loop()`  
- Pre-allocate Strings with `.reserve()` and ensure JSON documents are large enough  
- Ensure proper user permissions for serial upload on Ubuntu  
