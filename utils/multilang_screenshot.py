#!/usr/bin/env python3
"""
Multi-Language Screenshot Capture

Automatically capture the same views in multiple languages in parallel
"""

import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


@dataclass
class ScreenshotTask:
    """Represents a screenshot to capture"""
    name: str
    url: str
    language: str
    selector: Optional[str] = None
    wait_time: int = 2000
    full_page: bool = False


@dataclass
class ScreenshotResult:
    """Result of a screenshot capture"""
    task: ScreenshotTask
    success: bool
    filepath: Optional[str] = None
    error: Optional[str] = None
    duration: float = 0


class MultiLanguageScreenshotCapturer:
    """Capture screenshots in multiple languages efficiently"""

    DEFAULT_LANGUAGES = ['en', 'fr']

    LANGUAGE_URLS = {
        'en': '/en/',
        'fr': '/fr/',
        'de': '/de/',
        'es': '/es/',
        'it': '/it/',
        'pt': '/pt/',
        'ja': '/ja/',
        'zh': '/zh/'
    }

    def __init__(self, base_url: str, output_dir: str = './output/screenshots',
                 languages: List[str] = None, parallel: bool = True):
        """
        Initialize the capturer

        Args:
            base_url: Base URL of the application
            output_dir: Directory to save screenshots
            languages: List of language codes (default: ['en', 'fr'])
            parallel: Whether to capture languages in parallel (default: True)
        """
        self.base_url = base_url.rstrip('/')
        self.output_dir = output_dir
        self.languages = languages or self.DEFAULT_LANGUAGES
        self.parallel = parallel
        os.makedirs(output_dir, exist_ok=True)

    def create_tasks_from_plan(self, screenshot_plan: List[Dict]) -> List[ScreenshotTask]:
        """
        Create screenshot tasks for all languages from a plan

        Args:
            screenshot_plan: List of dicts with 'name', 'url', etc.

        Returns:
            List of ScreenshotTask objects for all languages
        """
        tasks = []

        for item in screenshot_plan:
            name = item['name']
            url = item['url']
            selector = item.get('selector')
            wait_time = item.get('wait_time', 2000)
            full_page = item.get('full_page', False)

            for lang in self.languages:
                # Create language-specific task
                lang_name = f"{name}-{lang}" if len(self.languages) > 1 else name
                lang_url = self._localize_url(url, lang)

                task = ScreenshotTask(
                    name=lang_name,
                    url=lang_url,
                    language=lang,
                    selector=selector,
                    wait_time=wait_time,
                    full_page=full_page
                )
                tasks.append(task)

        return tasks

    def _localize_url(self, url: str, language: str) -> str:
        """
        Convert a URL to include language prefix

        Examples:
            /dashboard/training + 'fr' -> /fr/dashboard/training
            /en/dashboard/training + 'fr' -> /fr/dashboard/training
        """
        url = url.lstrip('/')

        # Remove existing language prefix if present
        for lang_code in self.LANGUAGE_URLS.keys():
            prefix = f"{lang_code}/"
            if url.startswith(prefix):
                url = url[len(prefix):]
                break

        # Add new language prefix
        lang_prefix = self.LANGUAGE_URLS.get(language, f"/{language}/")
        return f"{lang_prefix}{url}"

    def capture_tasks(self, tasks: List[ScreenshotTask]) -> List[ScreenshotResult]:
        """
        Capture all screenshot tasks

        Args:
            tasks: List of ScreenshotTask objects

        Returns:
            List of ScreenshotResult objects
        """
        if self.parallel:
            return self._capture_parallel(tasks)
        else:
            return self._capture_sequential(tasks)

    def _capture_parallel(self, tasks: List[ScreenshotTask]) -> List[ScreenshotResult]:
        """Capture screenshots in parallel"""
        results = []

        # Group by language to share sessions
        lang_groups = {}
        for task in tasks:
            if task.language not in lang_groups:
                lang_groups[task.language] = []
            lang_groups[task.language].append(task)

        print(f"📸 Capturing {len(tasks)} screenshots in {len(lang_groups)} languages (parallel mode)")

        # Capture each language group in parallel
        with ThreadPoolExecutor(max_workers=len(self.languages)) as executor:
            futures = []

            for lang, lang_tasks in lang_groups.items():
                future = executor.submit(self._capture_language_session, lang, lang_tasks)
                futures.append(future)

            # Collect results as they complete
            for future in as_completed(futures):
                try:
                    lang_results = future.result()
                    results.extend(lang_results)
                except Exception as e:
                    print(f"❌ Error in parallel capture: {e}")

        return results

    def _capture_sequential(self, tasks: List[ScreenshotTask]) -> List[ScreenshotResult]:
        """Capture screenshots sequentially"""
        results = []

        print(f"📸 Capturing {len(tasks)} screenshots (sequential mode)")

        for task in tasks:
            result = self._capture_single(task)
            results.append(result)

            # Progress indicator
            completed = len(results)
            total = len(tasks)
            print(f"  [{completed}/{total}] {result.task.name} - {'✅' if result.success else '❌'}")

        return results

    def _capture_language_session(self, language: str, tasks: List[ScreenshotTask]) -> List[ScreenshotResult]:
        """
        Capture all screenshots for a single language in one session

        This is more efficient as it reuses authentication and browser context
        """
        results = []

        print(f"\n🌐 Starting {language.upper()} session ({len(tasks)} screenshots)")

        # TODO: Initialize capturer with proper auth for this language
        # For now, simulate capture
        for task in tasks:
            result = self._capture_single(task)
            results.append(result)

            status = "✅" if result.success else "❌"
            print(f"  {status} {task.name}")

        return results

    def _capture_single(self, task: ScreenshotTask) -> ScreenshotResult:
        """Capture a single screenshot"""
        start_time = time.time()

        try:
            # Build full URL
            full_url = f"{self.base_url}{task.url}"

            # Generate output filename
            filename = f"{task.name}.png"
            filepath = os.path.join(self.output_dir, filename)

            # TODO: Actual screenshot capture logic
            # For now, simulate
            # capturer.navigate(full_url)
            # capturer.wait(task.wait_time)
            # if task.selector:
            #     capturer.capture(filepath, selector=task.selector)
            # else:
            #     capturer.capture(filepath, full_page=task.full_page)

            duration = time.time() - start_time

            return ScreenshotResult(
                task=task,
                success=True,
                filepath=filepath,
                duration=duration
            )

        except Exception as e:
            duration = time.time() - start_time
            return ScreenshotResult(
                task=task,
                success=False,
                error=str(e),
                duration=duration
            )

    def capture_multilang_views(self, views: List[Dict], languages: List[str] = None) -> Dict:
        """
        Convenience method to capture multiple views in multiple languages

        Args:
            views: List of view definitions (name, url, etc.)
            languages: Optional override for languages

        Returns:
            Dict with results summary and file paths
        """
        if languages:
            self.languages = languages

        # Create tasks
        tasks = self.create_tasks_from_plan(views)

        # Capture
        results = self.capture_tasks(tasks)

        # Summarize
        summary = {
            'total': len(results),
            'success': sum(1 for r in results if r.success),
            'failed': sum(1 for r in results if not r.success),
            'languages': self.languages,
            'results': results,
            'files': [r.filepath for r in results if r.success]
        }

        return summary

    def print_summary(self, summary: Dict):
        """Print a formatted summary of capture results"""
        print("\n" + "=" * 70)
        print("📊 Screenshot Capture Summary")
        print("=" * 70)

        print(f"\n✅ Success: {summary['success']}/{summary['total']}")
        if summary['failed'] > 0:
            print(f"❌ Failed: {summary['failed']}")

        print(f"\n🌐 Languages: {', '.join(summary['languages'])}")
        print(f"📁 Output: {self.output_dir}")

        # Group by language
        lang_results = {}
        for result in summary['results']:
            lang = result.task.language
            if lang not in lang_results:
                lang_results[lang] = {'success': 0, 'failed': 0, 'files': []}

            if result.success:
                lang_results[lang]['success'] += 1
                lang_results[lang]['files'].append(result.task.name + '.png')
            else:
                lang_results[lang]['failed'] += 1

        print(f"\n📸 By Language:")
        for lang, stats in lang_results.items():
            print(f"  {lang.upper()}: {stats['success']} success, {stats['failed']} failed")
            for filename in stats['files'][:5]:  # Show first 5
                print(f"    • {filename}")
            if len(stats['files']) > 5:
                print(f"    ... and {len(stats['files']) - 5} more")

        print("\n" + "=" * 70)


def demo():
    """Demo multi-language screenshot capture"""

    # Define views to capture
    views = [
        {
            'name': 'dashboard-overview',
            'url': '/dashboard',
            'wait_time': 2000
        },
        {
            'name': 'leaderboard',
            'url': '/dashboard/leaderboard',
            'wait_time': 3000
        },
        {
            'name': 'training-overview',
            'url': '/dashboard/training',
            'selector': '.training-overview',
            'wait_time': 2000
        }
    ]

    # Create capturer
    capturer = MultiLanguageScreenshotCapturer(
        base_url='https://admin.eu.elba.security',
        languages=['en', 'fr'],
        parallel=True
    )

    # Capture all views in all languages
    summary = capturer.capture_multilang_views(views)

    # Print summary
    capturer.print_summary(summary)


if __name__ == '__main__':
    demo()
