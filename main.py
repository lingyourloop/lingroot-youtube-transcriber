if __name__ != "__main__":
    exit()  # Render çalıştırıyorsa bu dosya hemen kapansın

import os
from utils import process_youtube_link, list_google_voices

def main():
    youtube_url = input("🎬 YouTube video linkini girin: ").strip()

    print("\n🎚️ Google TTS sesleri listeleniyor...")
    voice_name = list_google_voices()

    print("\n🚀 İşlem başlatılıyor...\n")
    result = process_youtube_link(youtube_url, voice_name)

    print("\n✅ İşlem tamamlandı.")
    print("📘 İngilizce transcript:\n")
    print(result["transcript"])
    print(f"\n🔊 Üretilen ses dosyası: {result['audio_url']}")
    print(f"📄 Kaydedilen transcript dosyası: {result['transcript_file']}\n")

if __name__ == "__main__":
    main()
