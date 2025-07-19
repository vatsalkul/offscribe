from core.transcriber import EnhancedTranscriber

if __name__ == "__main__":
    transcriber = EnhancedTranscriber("mlx-community/whisper-large-v3-turbo")
    
    try:
        transcriber.start_listening()
    except KeyboardInterrupt:
        print("\n👋 Enhanced Transcriber stopped")