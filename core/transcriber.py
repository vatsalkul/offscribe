import mlx_whisper
import sounddevice as sd
import numpy as np
import threading
import time
import os
import tempfile
import wave
import sys
import pyperclip
from utils.audio_utils import SoundFeedback

try:
    from pynput import keyboard
    from pynput.keyboard import Key, Listener, Controller
    PYNPUT_AVAILABLE = True
except:
    PYNPUT_AVAILABLE = False

class EnhancedTranscriber:
    def __init__(self, model_name="mlx-community/whisper-large-v3-turbo"):
        print("🚀 Initializing Enhanced Transcriber with Audio + Visual Feedback...")
        
        self.model_name = model_name
        self.is_recording = False
        self.audio_data = []
        self.sample_rate = 16000
        self.recording_thread = None
        self.start_time = None
        
        # UI Components
        self.sound_feedback = SoundFeedback()
        
        # Double-click detection
        self.last_ctrl_press_time = 0
        self.double_click_threshold = 0.3
        self.ctrl_click_count = 0
        self.waiting_for_second_click = False
        
        # Statistics
        self.total_recordings = 0
        self.total_transcription_time = 0
        
        if not PYNPUT_AVAILABLE:
            print("⚠️  pynput not available. Using simple mode.")
            self.use_simple_mode = True
        else:
            self.use_simple_mode = False
            
        print("🎯 Control: Double-click Left Ctrl to start/stop recording")
        print("🔊 Sound: Audio feedback enabled")
        print("🎯 Quit: Ctrl+C")

    
    def start_listening(self):
        if self.use_simple_mode:
            self._simple_mode()
            return
            
        print(f"\n🎤 Enhanced Transcriber with Multi-Modal Feedback ready!")
        print("📍 Double-click Left Ctrl → Start/Stop recording")
        print("🔊 Listen for sounds + 📱 Watch for notifications + 📺 Terminal updates")
        print("Press Ctrl+C to quit\n")
        
        # Try to start listener with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 Starting listener (attempt {attempt + 1}/{max_retries})...")
                
                with Listener(
                    on_press=self.on_key_press,
                    on_release=self.on_key_release,
                    suppress=False
                ) as listener:
                    print("✅ Listener started successfully!")
                    listener.join()
                break
                
            except KeyError as e:
                if 'AXIsProcessTrusted' in str(e):
                    print(f"⚠️  Accessibility trust check failed (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        print("🔄 Retrying in 3 seconds...")
                        time.sleep(3)
                    else:
                        print("❌ Failed to start listener after retries")
                        print("🔄 Falling back to simple mode...")
                        self._simple_mode()
                else:
                    print(f"❌ Listener error: {e}")
                    self._simple_mode()
                    break
            except Exception as e:
                print(f"❌ Listener error: {e}")
                if attempt < max_retries - 1:
                    print("🔄 Retrying...")
                    time.sleep(2)
                else:
                    print("🔄 Falling back to simple mode...")
                    self._simple_mode()
                break
    
    def _simple_mode(self):
        """Enhanced simple mode with multi-modal feedback"""
        print(f"\n🎤 Simple Mode with Multi-Modal Feedback!")
        print("📍 Commands:")
        print("   's' + Enter → Start recording")
        print("   'q' + Enter → Stop recording & transcribe")
        print("   't' + Enter → Toggle sound feedback")
        print("   'stats' + Enter → Show statistics")
        print("   'x' + Enter → Quit")

        try:
            while True:
                command = input("\nCommand (s/q/t/stats/x): ").strip().lower()

                if command == 's':
                    if not self.is_recording:
                        self.start_recording()
                    else:
                        print("⚠️  Already recording...")
                        
                elif command == 'q':
                    if self.is_recording:
                        self.stop_recording()
                    else:
                        print("⚠️  Not recording...")
                
                elif command == 't':
                    enabled = self.sound_feedback.toggle()
                    status = "enabled" if enabled else "disabled"
                    print(f"🔊 Sound feedback {status}")
                    
                
                elif command == 'stats':
                    self._show_statistics()
                        
                elif command == 'x':
                    if self.is_recording:
                        self.is_recording = False
                    self.visual_feedback.cleanup()
                    print("👋 Goodbye!")
                    break
                    
                else:
                    print("❌ Invalid command. Use 's', 'q', 't', 'v', 'stats', or 'x'")
                    
        except KeyboardInterrupt:
            self.visual_feedback.cleanup()
            print("\n👋 Transcriber stopped")
    
    def _show_statistics(self):
        """Show usage statistics"""
        if self.total_recordings == 0:
            print("📊 No recordings yet")
        else:
            avg_time = self.total_transcription_time / self.total_recordings
            print(f"📊 Statistics:")
            print(f"   Total recordings: {self.total_recordings}")
            print(f"   Average transcription time: {avg_time:.2f}s")
            print(f"   Sound feedback: {'On' if self.sound_feedback.enabled else 'Off'}")
            print(f"   Visual feedback: Notifications + Terminal")
    
    def on_key_press(self, key):
        try:
            if key == Key.ctrl_l:
                current_time = time.time()
                
                if not self.waiting_for_second_click:
                    self.last_ctrl_press_time = current_time
                    self.waiting_for_second_click = True
                    self.ctrl_click_count = 1
                    threading.Thread(target=self._check_double_click, daemon=True).start()
                else:
                    time_diff = current_time - self.last_ctrl_press_time
                    if time_diff <= self.double_click_threshold:
                        self.ctrl_click_count = 2
                        self._handle_double_click()
                    else:
                        self.last_ctrl_press_time = current_time
                        self.ctrl_click_count = 1
        except Exception as e:
            print(f"Key press error: {e}")
    
    def on_key_release(self, key):
        try:
            if key == Key.esc:
                return False
        except Exception as e:
            print(f"Key release error: {e}")
    
    def _check_double_click(self):
        time.sleep(self.double_click_threshold)
        if self.ctrl_click_count == 1:
            self.waiting_for_second_click = False
            self.ctrl_click_count = 0
    
    def _handle_double_click(self):
        self.waiting_for_second_click = False
        self.ctrl_click_count = 0
        
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        print("🔴 Recording... (Double-click Left Ctrl to stop)")
        
        # Start multi-modal feedback
        self.sound_feedback.play_start_sound()
        
        self.is_recording = True
        self.audio_data = []
        self.start_time = time.time()
        
        self.recording_thread = threading.Thread(target=self._record_audio, daemon=True)
        self.recording_thread.start()
    
    def stop_recording(self):
        if not self.is_recording:
            return
        
        # Stop visual and play sound feedback
        self.sound_feedback.play_stop_sound()
            
        if time.time() - self.start_time < 0.3:
            print("⚠️  Recording too short")
            self.sound_feedback.play_error_sound()
            self.is_recording = False
            return
            
        print("⏹️  Processing...")
        self.is_recording = False
        
        
        if self.recording_thread:
            self.recording_thread.join(timeout=2.0)
        
        self._transcribe()
    
    def _record_audio(self):
        def audio_callback(indata, frames, time, status):
            if self.is_recording:
                self.audio_data.append(indata.copy())
        
        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.float32,
                callback=audio_callback,
                blocksize=1024
            ):
                while self.is_recording:
                    time.sleep(0.01)
        except Exception as e:
            print(f"❌ Recording error: {e}")
            self.sound_feedback.play_error_sound()
    
    def _transcribe(self):
        if not self.audio_data:
            print("❌ No audio recorded")
            self.sound_feedback.play_error_sound()
            return
        
        try:
            audio = np.concatenate(self.audio_data)
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                audio_int16 = (audio * 32767).astype(np.int16)
                
                with wave.open(temp_file.name, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(self.sample_rate)
                    wav_file.writeframes(audio_int16.tobytes())
                
                print("🧠 Transcribing with MLX...")
                start_time = time.time()
                
                result = mlx_whisper.transcribe(
                    temp_file.name,
                    path_or_hf_repo=self.model_name,
                    language="en"
                )
                
                transcription_time = time.time() - start_time
                os.unlink(temp_file.name)
                
                
                # Update statistics
                self.total_recordings += 1
                self.total_transcription_time += transcription_time
                
                text = result["text"].strip()
                
                if text:
                    pyperclip.copy(text)
                    print(f"✅ Transcribed in {transcription_time:.2f}s: '{text}' → Clipboard")
                    
                    # Play success sound
                    self.sound_feedback.play_success_sound()
                    
                    # Auto-paste using pynput
                    if PYNPUT_AVAILABLE and Controller:
                        try:
                            controller = Controller()
                            
                            print("🎯 Auto-pasting...")
                            time.sleep(0.5)
                            
                            controller.press(Key.cmd)
                            controller.press('v')
                            controller.release('v')
                            controller.release(Key.cmd)
                            
                            print("✅ Text pasted automatically!")
                            
                        except Exception as paste_error:
                            print(f"❌ Auto-paste failed: {paste_error}")
                            print("💡 Manually press Cmd+V to paste")
                            self.sound_feedback.play_error_sound()
                    else:
                        print("💡 Press Cmd+V to paste")
                        
                else:
                    print("❌ No speech detected")
                    self.sound_feedback.play_error_sound()
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            self.sound_feedback.play_error_sound()
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        if hasattr(self, 'visual_feedback'):
            self.visual_feedback.cleanup()

    