import yt_dlp
import os

class VideoDownloader:
    def __init__(self):
        self.default_opts = {
            # Speed optimization: Prefer MP4 to avoid re-encoding, use aria2c for multi-connection
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            # Use aria2c only for direct files, use native for HLS/DASH to avoid "Invalid range header" errors
            'external_downloader': {
                'default': 'aria2c',
                'm3u8': 'native',
                'm3u8_native': 'native',
                'dash': 'native',
            },
            'external_downloader_args': {
                'aria2c': ['-x', '8', '-k', '1M', '-s', '8']
            },
            'concurrent_fragment_downloads': 5,
            # Anti-bot evasion: Let impersonate handle UA, add Referer
            'extractor_args': {'generic': ['impersonate']},
            'http_headers': {
                'Referer': 'https://filemoon.to/',
            },
            'nocheckcertificate': True,
        }

    def get_info(self, url):
        """Fetches video information without downloading."""
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown Title'),
                    'thumbnail': info.get('thumbnail', None),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'formats': info.get('formats', [])
                }
            except Exception as e:
                print(f"Error fetching info: {e}")
                return None

    def download(self, url, output_path, custom_filename=None, progress_hook=None, completion_hook=None):
        """Downloads the video."""
        
        # Ensure output directory exists
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        opts = self.default_opts.copy()
        
        if custom_filename:
            # Use custom filename
            opts['outtmpl'] = os.path.join(output_path, f"{custom_filename}.%(ext)s")
        else:
            opts['outtmpl'] = os.path.join(output_path, '%(title)s.%(ext)s')
        
        if progress_hook:
            opts['progress_hooks'] = [progress_hook]
            opts['postprocessor_hooks'] = [progress_hook]

        # Post-processor to ensure mp4
        opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]

        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                ydl.download([url])
                if completion_hook:
                    completion_hook(True, None)
            except Exception as e:
                if completion_hook:
                    completion_hook(False, str(e))

if __name__ == "__main__":
    # Test
    dl = VideoDownloader()
    info = dl.get_info("https://www.youtube.com/watch?v=BaW_jenozKc")
    print(f"Title: {info['title']}")
