import subprocess
import threading

class SoundFeedback:
    """Handle audio feedback for recording events"""
    
    def __init__(self):
        self.enabled = True
        
    def play_start_sound(self):
        """Play sound when recording starts"""
        if self.enabled:
            threading.Thread(target=self._play_system_sound, args=("Blow",), daemon=True).start()
    
    def play_stop_sound(self):
        """Play sound when recording stops"""
        if self.enabled:
            threading.Thread(target=self._play_system_sound, args=("Pop",), daemon=True).start()
    
    def play_success_sound(self):
        """Play sound when transcription completes"""
        if self.enabled:
            threading.Thread(target=self._play_system_sound, args=("Glass",), daemon=True).start()
    
    def play_error_sound(self):
        """Play sound when error occurs"""
        if self.enabled:
            threading.Thread(target=self._play_system_sound, args=("Basso",), daemon=True).start()
    
    def _play_system_sound(self, sound_name):
        """Play macOS system sound"""
        try:
            subprocess.run(['afplay', f'/System/Library/Sounds/{sound_name}.aiff'], 
                         check=False, capture_output=True)
        except:
            pass  # Fail silently if sound can't play
    
    def toggle(self):
        """Toggle sound feedback on/off"""
        self.enabled = not self.enabled
        return self.enabled